#!/usr/bin/env python3
"""fsk — Fullstack Skills Kit CLI.

Ferramenta executável do kit curado. Cross-platform (Windows/macOS/Linux).

Comandos:
  validate               Valida o schema do manifest (campos, ids duplicados, áreas, trust).
  doctor [--links]       Diagnóstico: itens #VERIFY, telemetria, confiança. --links checa HTTP dos sources.
  detect [--path .]      Detecta a stack do projeto (tokens) a partir dos arquivos-sinal.
  plan   [--path .]      Monta o plano de ferramentas opcionais que casam com a stack. NÃO instala.
  core   [--target claude|codex|opencode|cursor|gemini|antigravity|copilot] [--home ~] [--project .] [--dry-run]
                         Instala núcleo + skills fsk-* no alvo. SKILL.md serve 5 provedores; copilot gera
                         prompt files (--project obrigatório). Núcleo: import (claude) ou bloco (demais).
  check-map [--path .]   Confere que todo caminho citado no AGENTS.md, nos `paths` das rules e nos
                         how-to existe. Sai com erro se houver ponteiro quebrado (rodável em hook/CI).
  worktree NAME [--path .] [--branch B]
                         Cria uma worktree em .worktrees/NAME e copia os não-versionados (artefatos de
                         agente, .env) que o `git worktree add` não leva.
  git-hooks [--path .] [--local-mode]
                         Instala hooks git (respeita husky; senão .git/hooks): post-checkout copia
                         não-versionados p/ worktree nova; pre-commit barra segredo + roda check-map.
                         --local-mode adiciona bloco no .gitignore p/ não versionar artefatos de agente.
  check-proof [--base REF] [--block]
                         Freio da prova: se a mudança tem código de produção mas não há evidencias.md
                         com canal real (navegador/API), avisa (ou bloqueia com --block, p/ CI de merge).

Uso:
  python install/fsk.py validate
  python install/fsk.py core
  python install/fsk.py check-map --path .
Requisito: PyYAML (pip install pyyaml).
"""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path

# Windows-safe: força UTF-8 na saída (console cp1252 quebra acento/emoji).
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    import yaml
except ImportError:
    sys.exit("Falta PyYAML. Instale: pip install pyyaml")

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.yaml"
REQUIRED = ["id", "name", "area", "phase", "type", "cost", "scope", "load", "stack_match"]
KIT = ROOT.parent  # raiz do repo do kit (install/ fica dentro)


def load():
    with open(MANIFEST, encoding="utf-8") as f:
        return yaml.safe_load(f)


def trust_of(item, data):
    tiers = data.get("trust_tiers", {}) or {}
    for tier in ("official", "self", "unverified"):
        if item["id"] in (tiers.get(tier) or []):
            return tier
    return "community"


# ---------------------------------------------------------------- validate
def cmd_validate(data):
    items = data["items"]
    areas = set(data["areas"])
    errs, warns = [], []
    seen = set()
    for it in items:
        iid = it.get("id", "?")
        for k in REQUIRED:
            if k not in it:
                errs.append(f"{iid}: falta campo obrigatório '{k}'")
        if iid in seen:
            errs.append(f"id duplicado: {iid}")
        seen.add(iid)
        if it.get("area") not in areas:
            errs.append(f"{iid}: área '{it.get('area')}' não está no índice areas")
        if it.get("cost") not in ("low", "high"):
            errs.append(f"{iid}: cost inválido")
        if it.get("scope") not in ("global", "project"):
            errs.append(f"{iid}: scope inválido")
        if it.get("type") == "mcp" and it.get("cost") != "high":
            warns.append(f"{iid}: MCP deveria ter cost:high")
        if "VERIFY" in str(it.get("source", "")) or "VERIFY" in str(it.get("install", "")):
            warns.append(f"{iid}: link #VERIFY pendente")
    print(f"itens: {len(items)} | áreas: {len(areas)} | scope_focus: {data.get('scope_focus')}")
    for w in warns:
        print("  ! " + w)
    if errs:
        for e in errs:
            print("  ✗ " + e)
        print(f"\nFALHOU: {len(errs)} erro(s), {len(warns)} aviso(s)")
        return 1
    print(f"\nOK: schema válido ({len(warns)} aviso(s))")
    return 0


# ---------------------------------------------------------------- doctor
def cmd_doctor(data, check_links):
    items = data["items"]
    verify = [i["id"] for i in items if "VERIFY" in str(i.get("source", "")) + str(i.get("install", ""))]
    telem = [(i["id"], i["telemetry"]) for i in items if i.get("telemetry") not in (None, "none")]
    unverified = [i["id"] for i in items if trust_of(i, data) == "unverified"]
    print(f"#VERIFY pendentes ({len(verify)}): {', '.join(verify) or '—'}")
    print(f"confiança 'unverified' ({len(unverified)}): {', '.join(unverified) or '—'}")
    print("telemetria (revisar em contexto corporativo):")
    for iid, t in telem:
        print(f"  - {iid}: {t}")
    if check_links:
        import urllib.request
        print("\nchecando sources (HTTP)...")
        for it in items:
            src = str(it.get("source", ""))
            if not src.startswith("http") or "VERIFY" in src:
                continue
            url = src.split()[0].split("(")[0]
            try:
                req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "fsk"})
                code = urllib.request.urlopen(req, timeout=10).status
                print(f"  {'ok ' if code < 400 else code} {it['id']}")
            except Exception as e:
                print(f"  ERRO {it['id']}: {type(e).__name__}")
    return 0


# ---------------------------------------------------------------- detect
SIGNALS = {
    "package.json": lambda p: _pkg_json(p),
    "pyproject.toml": lambda p: ["python"],
    "requirements.txt": lambda p: ["python"],
    "go.mod": lambda p: ["go"],
    "pom.xml": lambda p: ["java"],
    "build.gradle": lambda p: ["java"],
    "Cargo.toml": lambda p: ["rust"],
    "Dockerfile": lambda p: ["docker"],
    "docker-compose.yml": lambda p: ["docker", "compose"],
    "compose.yaml": lambda p: ["docker", "compose"],
    ".gitlab-ci.yml": lambda p: ["gitlab"],
}
GLOB_SIGNALS = {
    "*.tf": ["terraform"], "*.sql": ["*.sql"],
    "*.openapi.yaml": ["openapi"], "*.swagger.json": ["swagger"],
}


def _pkg_json(path):
    toks = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        m = {"react": "react", "next": "next", "vue": "vue", "svelte": "svelte",
             "@angular/core": "angular", "tailwindcss": "tailwind", "@playwright/test": "web",
             "pg": "postgres", "mysql2": "mysql", "mongodb": "mongodb", "@shadcn/ui": "react"}
        for dep, tok in m.items():
            if dep in deps:
                toks.append(tok)
        if any(k in deps for k in ("react", "vue", "svelte", "@angular/core")):
            toks.append("web")
    except Exception:
        pass
    return toks or ["node"]


def detect(path: Path):
    toks = set()
    for name, fn in SIGNALS.items():
        if (path / name).exists():
            toks.update(fn(path / name))
    for glob, t in GLOB_SIGNALS.items():
        if any(path.rglob(glob)):
            toks.update(t)
    if (path / ".circleci").exists():
        toks.add("circleci")
    if any(path.rglob("*.yaml")) and (path / "kustomization.yaml").exists():
        toks.add("kubernetes")
    return sorted(toks)


def cmd_detect(path):
    toks = detect(path)
    print("stack detectada:", ", ".join(toks) or "(nenhum sinal)")
    return 0


# ---------------------------------------------------------------- plan
def matches(item, toks):
    sm = item.get("stack_match") or []
    if "*" in sm:
        return "any"
    return "stack" if any(t in sm for t in toks) else None


COSTMARK = {"low": "[barato]", "high": "[ MCP  ]"}
TRUSTMARK = {"official": "oficial", "self": "proprio", "community": "comunidade", "unverified": "NAO-VERIFICADO"}


def cmd_plan(data, path):
    toks = detect(path)
    items = data["items"]
    globals_ = [i for i in items if i["scope"] == "global"]
    proj_stack = [i for i in items if i["scope"] == "project" and matches(i, toks) == "stack"]
    proj_any = [i for i in items if i["scope"] == "project" and matches(i, toks) == "any"]

    print(f"# Plano de instalação — stack: {', '.join(toks) or '(nenhum sinal)'}")
    print(f"# scope_focus: {data.get('scope_focus')} | fora de escopo: {', '.join(data.get('out_of_scope', []))}\n")

    def render(title, group, note=""):
        if not group:
            return
        print(f"## {title} {note}")
        for i in sorted(group, key=lambda x: (x["area"], x["id"])):
            tr = trust_of(i, data)
            tele = "" if i.get("telemetry") in (None, "none") else f" · telemetria:{i['telemetry']}"
            gate = "  ⟵ AUDITAR ANTES" if tr in ("unverified",) else ""
            print(f"  {COSTMARK[i['cost']]} [{i['area']}] {i['name']} — {TRUSTMARK[tr]}{tele}{gate}")
            print(f"       install: {i.get('install','?')}")
        print()

    render("Núcleo global (uma vez)", globals_)
    render("Casam com a stack detectada", proj_stack)
    render("Sugeridos para qualquer projeto web (opcional)", proj_any)

    print("## Gate de confiança (regra #4)")
    print("  - fsk NÃO instala nada: este é um plano. Instale com propor-e-confirmar.")
    print("  - Itens '⚠ NÃO verificado' ou de baixa adoção: AUDITE o código/fonte antes de confiar.")
    print("  - Itens com telemetria: avalie antes de ligar em contexto corporativo sensível.")
    return 0


# ---------------------------------------------------------------- core (instala multi-alvo)
# Portabilidade: SKILL.md é o mesmo formato em 5 provedores; Copilot usa prompt files.
# O núcleo vai no arquivo de memória de cada alvo (import no Claude, bloco nos demais);
# onde não há memória global (cursor/copilot), ele entra no AGENTS.md do projeto (via /fsk-setup).
TARGETS = {
    "claude":      {"skills": "~/.claude/skills",         "mem": "~/.claude/CLAUDE.md",         "mem_mode": "import", "fmt": "skill"},
    "codex":       {"skills": "~/.codex/skills",          "mem": "~/.codex/AGENTS.md",          "mem_mode": "block",  "fmt": "skill"},
    "opencode":    {"skills": "~/.config/opencode/skills","mem": "~/.config/opencode/AGENTS.md","mem_mode": "block",  "fmt": "skill"},
    "cursor":      {"skills": "~/.cursor/skills",         "mem": None,                          "mem_mode": "project","fmt": "skill"},
    "gemini":      {"skills": "~/.gemini/skills",         "mem": "~/.gemini/GEMINI.md",         "mem_mode": "block",  "fmt": "skill"},
    "antigravity": {"skills": "~/.gemini/config/skills",  "mem": "~/.gemini/config/AGENTS.md",  "mem_mode": "block",  "fmt": "skill"},
    "copilot":     {"skills": None,                       "mem": None,                          "mem_mode": "project","fmt": "prompt"},
}
FSK_START, FSK_END = "<!-- fsk:start -->", "<!-- fsk:end -->"


def _expand(p, base):
    return base / p[2:] if p.startswith("~/") else Path(p)


def _write_block(path, body):
    """Escreve/atualiza o bloco fsk delimitado, idempotente."""
    block = f"{FSK_START}\n{body.rstrip()}\n{FSK_END}\n"
    txt = path.read_text(encoding="utf-8") if path.exists() else ""
    if FSK_START in txt and FSK_END in txt:
        pre = txt.split(FSK_START)[0]
        post = txt.split(FSK_END, 1)[1].lstrip("\n")
        txt = pre.rstrip("\n") + ("\n\n" if pre.strip() else "") + block + ("\n" + post if post.strip() else "")
    else:
        txt = (txt.rstrip("\n") + "\n\n" if txt.strip() else "") + block
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(txt, encoding="utf-8")


def _skill_to_prompt(skill_md):
    """Converte um SKILL.md em .prompt.md (Copilot/VS Code)."""
    text = skill_md.read_text(encoding="utf-8")
    name, desc, body = skill_md.parent.name, "", text
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if m:
        fm, body = m.group(1), m.group(2)
        for line in fm.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip()
    return name, f"---\nmode: agent\ndescription: {desc}\n---\n{body.lstrip()}"


def cmd_core(target, home, dry, project):
    import shutil
    if target not in TARGETS:
        print(f"alvo inválido: {target}. Use: {', '.join(TARGETS)}")
        return 1
    t = TARGETS[target]
    base = Path(home) if home else Path.home()
    core_src = KIT / "global" / "fsk-workflow.md"
    core_body = core_src.read_text(encoding="utf-8")
    skills = sorted(p for p in (KIT / "skills").glob("fsk-*") if p.is_dir())
    proj = Path(project).resolve() if project else None
    print(f"alvo: {target}")

    # 1) skills
    if t["fmt"] == "skill" and t["skills"]:
        sdst = _expand(t["skills"], base)
        print(f"skills ({len(skills)}): {sdst}")
    elif t["fmt"] == "prompt":
        if not proj:
            print("copilot precisa de --project <repo> (gera .github/prompts/).")
            return 1
        print(f"prompt files ({len(skills)}): {proj / '.github' / 'prompts'}")

    # 2) núcleo
    if t["mem_mode"] == "import":
        print(f"núcleo: fsk-workflow.md + @import em {_expand(t['mem'], base)}")
    elif t["mem_mode"] == "block":
        print(f"núcleo: bloco fsk em {_expand(t['mem'], base)}")
    else:
        tgt = (proj / ("AGENTS.md" if target != "copilot" else ".github/copilot-instructions.md")) if proj else "AGENTS.md do projeto (via /fsk-setup)"
        print(f"núcleo: bloco fsk em {tgt}")

    if dry:
        print("\n(dry-run: nada escrito)")
        return 0

    # --- escrita ---
    if t["fmt"] == "skill" and t["skills"]:
        sdst = _expand(t["skills"], base)
        sdst.mkdir(parents=True, exist_ok=True)
        for sk in skills:
            d = sdst / sk.name
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(sk, d)
    elif t["fmt"] == "prompt":
        pdst = proj / ".github" / "prompts"
        pdst.mkdir(parents=True, exist_ok=True)
        for sk in skills:
            name, content = _skill_to_prompt(sk / "SKILL.md")
            (pdst / f"{name}.prompt.md").write_text(content, encoding="utf-8")

    if t["mem_mode"] == "import":
        dest = _expand(t["mem"], base).parent
        shutil.copy2(core_src, dest / "fsk-workflow.md")
        claude_md = _expand(t["mem"], base)
        txt = claude_md.read_text(encoding="utf-8") if claude_md.exists() else ""
        if "@fsk-workflow.md" not in txt:
            claude_md.parent.mkdir(parents=True, exist_ok=True)
            claude_md.write_text((txt.rstrip("\n") + "\n\n" if txt.strip() else "") + "@fsk-workflow.md\n", encoding="utf-8")
    elif t["mem_mode"] == "block":
        _write_block(_expand(t["mem"], base), core_body)
    elif proj:
        mem = proj / (".github/copilot-instructions.md" if target == "copilot" else "AGENTS.md")
        _write_block(mem, core_body)

    print("OK: instalado (idempotente).")
    return 0


# ---------------------------------------------------------------- check-map
def _candidate_paths(text):
    """Caminhos plausíveis citados em backticks: contêm '/' e casam um caminho de projeto."""
    out = []
    for tok in re.findall(r"`([^`]+)`", text):
        cand = tok.strip().split()[0].split(":")[0] if tok.strip() else ""
        if "/" not in cand or "*" in cand:
            continue
        if cand.startswith(("http", "https", "@", "/", "~", ".claude/skills/how-to-<")):
            continue
        if not re.match(r"^[\w./\-]+$", cand):
            continue
        if not re.search(r"\.\w{1,6}$", cand):  # só arquivos com extensão
            continue
        out.append(cand)
    return out


def cmd_check_map(path):
    base = Path(path).resolve()
    sources = []
    if (base / "AGENTS.md").exists():
        sources.append(base / "AGENTS.md")
    rdir = base / ".claude" / "rules"
    if rdir.exists():
        sources += sorted(rdir.glob("*.md"))
    sdir = base / ".claude" / "skills"
    if sdir.exists():
        sources += sorted(sdir.glob("how-to-*/**/*.md"))
    if not sources:
        print(f"check-map: nada para checar em {base} (sem AGENTS.md/rules/how-to).")
        return 0
    broken, checked = [], 0
    for src in sources:
        text = src.read_text(encoding="utf-8", errors="ignore")
        rel = src.relative_to(base)
        for g in re.findall(r'^\s*-\s*["\']?([^"\'\n]*\*[^"\'\n]*)["\']?\s*$', text, re.M):
            g = g.strip()
            checked += 1
            if not any(base.glob(g)):
                broken.append((rel, g, "glob não casa nenhum arquivo"))
        for cand in _candidate_paths(text):
            checked += 1
            if not (base / cand).exists():
                broken.append((rel, cand, "não existe"))
    print(f"check-map: {checked} ponteiro(s) em {len(sources)} fonte(s).")
    if broken:
        for rel, p, why in broken:
            print(f"  ✗ {rel}: `{p}` — {why}")
        print(f"\nFALHOU: {len(broken)} ponteiro(s) quebrado(s).")
        return 1
    print("OK: todo caminho citado existe.")
    return 0


# ---------------------------------------------------------------- git-utils
import subprocess, shutil

GIT_ARTIFACTS = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".claude", ".cursor", ".agents",
                 ".github/copilot-instructions.md", ".github/prompts", ".github/instructions"]
WT_COPY_DEFAULT = GIT_ARTIFACTS + [".env", ".env.local", ".env.development"]
GI_START, GI_END = "# fsk:gitignore:start", "# fsk:gitignore:end"


def _run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def _load_fsk_json(base):
    f = base / ".claude" / "fsk.json"
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _copy_untracked(src, dst, items):
    copied = []
    for it in items:
        s, d = src / it, dst / it
        if s.exists() and not d.exists():
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(s, d) if s.is_dir() else shutil.copy2(s, d)
            copied.append(it)
    return copied


def _is_secret_path(p):
    base = os.path.basename(p)
    if re.match(r"^\.env(\.|$)", base) and not re.search(r"\.(example|sample|template|dist)$", base):
        return True
    return bool(re.search(r"\.(pem|key|p12|pfx)$", base) or re.search(r"(secret|credential)s?\.(json|ya?ml|txt)$", base, re.I))


def _write_block_file(path, body, start, end):
    block = f"{start}\n{body.rstrip()}\n{end}\n"
    txt = path.read_text(encoding="utf-8") if path.exists() else ""
    if start in txt and end in txt:
        txt = txt.split(start)[0].rstrip("\n") + "\n\n" + block + txt.split(end, 1)[1].lstrip("\n")
    else:
        txt = (txt.rstrip("\n") + "\n\n" if txt.strip() else "") + block
    path.write_text(txt, encoding="utf-8")


def cmd_worktree(name, path, branch):
    base = Path(path).resolve()
    items = _load_fsk_json(base).get("worktree_copy", WT_COPY_DEFAULT)
    br, wt = branch or name, base / ".worktrees" / name
    r = _run(["git", "-C", str(base), "worktree", "add", "-b", br, str(wt)])
    if r.returncode != 0:
        r = _run(["git", "-C", str(base), "worktree", "add", str(wt), br])
        if r.returncode != 0:
            print("falha no git worktree add:\n" + r.stderr.strip())
            return 1
    _copy_untracked(base, wt, items)  # redundante se o hook post-checkout já copiou; idempotente
    present = [it for it in items if (wt / it).exists()]
    print(f"worktree: {wt}  (branch {br})")
    print(f"não-versionados no worktree ({len(present)}): {', '.join(present) or '—'}")
    print("prepare deps/portas pela receita de worktree do AGENTS.md.")
    return 0


HOOK_EVENTS = {"post-checkout": 'python "{fsk}" _hook post-checkout "$@"',
               "pre-commit": 'python "{fsk}" _hook pre-commit'}


def cmd_git_hooks(path, local_mode):
    base = Path(path).resolve()
    if not (base / ".git").exists():
        print("não é um repo git.")
        return 1
    fsk = str((ROOT / "fsk.py").resolve())
    installed = []
    if (base / ".husky").exists():
        for hook, tmpl in HOOK_EVENTS.items():
            f = base / ".husky" / hook
            line = tmpl.format(fsk=fsk)
            txt = f.read_text(encoding="utf-8") if f.exists() else "#!/bin/sh\n"
            if line not in txt:
                f.write_text(txt.rstrip("\n") + "\n" + line + "\n", encoding="utf-8")
            installed.append(f".husky/{hook}")
    else:
        hd = base / ".git" / "hooks"
        hd.mkdir(parents=True, exist_ok=True)
        for hook, tmpl in HOOK_EVENTS.items():
            f = hd / hook
            f.write_text(f"#!/bin/sh\n{tmpl.format(fsk=fsk)}\n", encoding="utf-8")
            try:
                os.chmod(f, 0o755)
            except Exception:
                pass
            installed.append(f".git/hooks/{hook}")
        lf = base / "lefthook.yml"
        if lf.exists() or (base / ".lefthook.yml").exists():
            print("aviso: repo usa lefthook — adicione ao lefthook.yml:\n"
                  f"  post-checkout:\n    commands:\n      fsk: {{run: 'python \"{fsk}\" _hook post-checkout {{0}} {{1}} {{2}}'}}\n"
                  f"  pre-commit:\n    commands:\n      fsk: {{run: 'python \"{fsk}\" _hook pre-commit'}}")
    print(f"hooks instalados: {', '.join(installed)}")
    if local_mode:
        _write_block_file(base / ".gitignore", "\n".join(GIT_ARTIFACTS), GI_START, GI_END)
        print(".gitignore: bloco do modo local (artefatos de agente fora do git)")
    return 0


def cmd_hook(event, args):
    cwd = Path(".").resolve()
    if event == "post-checkout":
        common = _run(["git", "rev-parse", "--git-common-dir"]).stdout.strip()
        gdir = _run(["git", "rev-parse", "--absolute-git-dir"]).stdout.strip()
        if not common or not gdir:
            return 0
        common = (cwd / common).resolve() if not os.path.isabs(common) else Path(common).resolve()
        if common == Path(gdir).resolve():
            return 0  # worktree principal: nada a copiar
        main_top = common.parent
        items = _load_fsk_json(cwd).get("worktree_copy", WT_COPY_DEFAULT)
        copied = _copy_untracked(main_top, cwd, items)
        if copied:
            print(f"fsk: copiados para o worktree ({len(copied)}): {', '.join(copied)}")
        return 0
    if event == "pre-commit":
        staged = _run(["git", "diff", "--cached", "--name-only"]).stdout.split()
        bad = [f for f in staged if _is_secret_path(f)]
        if bad:
            print("fsk: NÃO commite segredo: " + ", ".join(bad) + "\n(remova do stage; use variável de ambiente.)")
            return 1
        _warn_unproven(staged)  # aviso, não bloqueia o commit local
        return cmd_check_map(".")
    return 0


# ---------------------------------------------------------------- check-proof (freio da prova)
CODE_EXT = (".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".java", ".rb", ".php", ".cs", ".rs",
            ".kt", ".swift", ".vue", ".svelte", ".scala", ".c", ".cpp")


def _is_prod_code(f):
    if not f.endswith(CODE_EXT):
        return False
    if re.search(r"(\.(test|spec)\.|/__tests__/|/tests?/|\.d\.ts$|\.stories\.)", f):
        return False
    return not f.startswith(("docs/", ".claude/", ".github/", "hooks/", "install/"))


def _proof_is_real(base):
    specs = base / ".claude" / "specs"
    if not specs.exists():
        return False
    for ev in specs.glob("*/evidencias.md"):
        t = ev.read_text(encoding="utf-8", errors="ignore").lower()
        if re.search(r"navegador|api real|integra[çc][ãa]o|end-to-end|e2e|não executado end-to-end|tentei subir", t):
            return True
    return False


def _warn_unproven(files):
    prod = [f for f in files if _is_prod_code(f)]
    if prod and not _proof_is_real(Path(".").resolve()):
        print(f"fsk (aviso): {len(prod)} arquivo(s) de produção sem prova real registrada em "
              ".claude/specs/*/evidencias.md (canal navegador/API). Suíte verde é checagem, não prova.")


def cmd_check_proof(base_ref, block):
    base = Path(".").resolve()
    if base_ref:
        files = _run(["git", "diff", "--name-only", f"{base_ref}...HEAD"]).stdout.split()
    else:
        files = _run(["git", "diff", "--cached", "--name-only"]).stdout.split()
    prod = [f for f in files if _is_prod_code(f)]
    if not prod:
        print("check-proof: sem código de produção na mudança — nada a provar.")
        return 0
    if _proof_is_real(base):
        print(f"check-proof: ok — evidencias.md com canal real ({len(prod)} arquivo(s) de produção).")
        return 0
    msg = (f"{len(prod)} arquivo(s) de produção mudaram sem .claude/specs/*/evidencias.md declarando canal "
           "real (navegador/API/integração) nem justificativa de prova degradada. Rode o fsk-prove no canal real.")
    print(("check-proof BLOQUEADO — " if block else "check-proof AVISO — ") + msg)
    return 1 if block else 0


def main():
    ap = argparse.ArgumentParser(prog="fsk", description="Fullstack Skills Kit CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    d = sub.add_parser("doctor"); d.add_argument("--links", action="store_true")
    de = sub.add_parser("detect"); de.add_argument("--path", default=".")
    pl = sub.add_parser("plan"); pl.add_argument("--path", default=".")
    co = sub.add_parser("core")
    co.add_argument("--target", default="claude")
    co.add_argument("--home", default=None)
    co.add_argument("--project", default=None)
    co.add_argument("--dry-run", action="store_true")
    cm = sub.add_parser("check-map"); cm.add_argument("--path", default=".")
    wt = sub.add_parser("worktree"); wt.add_argument("name"); wt.add_argument("--path", default="."); wt.add_argument("--branch", default=None)
    gh = sub.add_parser("git-hooks"); gh.add_argument("--path", default="."); gh.add_argument("--local-mode", action="store_true")
    hk = sub.add_parser("_hook"); hk.add_argument("event"); hk.add_argument("rest", nargs="*")
    cp = sub.add_parser("check-proof"); cp.add_argument("--base", default=None); cp.add_argument("--block", action="store_true")
    args = ap.parse_args()
    if args.cmd == "core":
        sys.exit(cmd_core(args.target, args.home, args.dry_run, args.project))
    if args.cmd == "check-map":
        sys.exit(cmd_check_map(args.path))
    if args.cmd == "worktree":
        sys.exit(cmd_worktree(args.name, args.path, args.branch))
    if args.cmd == "git-hooks":
        sys.exit(cmd_git_hooks(args.path, args.local_mode))
    if args.cmd == "_hook":
        sys.exit(cmd_hook(args.event, args.rest))
    if args.cmd == "check-proof":
        sys.exit(cmd_check_proof(args.base, args.block))
    data = load()
    if args.cmd == "validate":
        sys.exit(cmd_validate(data))
    if args.cmd == "doctor":
        sys.exit(cmd_doctor(data, args.links))
    if args.cmd == "detect":
        sys.exit(cmd_detect(Path(args.path).resolve()))
    if args.cmd == "plan":
        sys.exit(cmd_plan(data, Path(args.path).resolve()))


if __name__ == "__main__":
    main()
