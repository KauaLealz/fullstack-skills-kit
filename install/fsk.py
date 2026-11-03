#!/usr/bin/env python3
"""fsk — Fullstack Skills Kit CLI.

Ferramenta executável do kit curado. Cross-platform (Windows/macOS/Linux).

Comandos:
  validate            Valida o schema do manifest (campos, ids duplicados, áreas, trust).
  doctor [--links]    Diagnóstico: itens #VERIFY, telemetria, confiança. --links checa HTTP dos sources.
  detect [--path .]   Detecta a stack do projeto (tokens) a partir dos arquivos-sinal.
  plan   [--path .]   Monta o plano de instalação: núcleo global + opcionais que casam com a stack,
                      com custo, confiança e telemetria. NÃO instala nada (propor-e-confirmar).

Uso:
  python install/fsk.py validate
  python install/fsk.py plan --path .
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
REQUIRED = ["id", "name", "area", "type", "cost", "scope", "load", "stack_match"]


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


def main():
    ap = argparse.ArgumentParser(prog="fsk", description="Fullstack Skills Kit CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    d = sub.add_parser("doctor"); d.add_argument("--links", action="store_true")
    de = sub.add_parser("detect"); de.add_argument("--path", default=".")
    pl = sub.add_parser("plan"); pl.add_argument("--path", default=".")
    args = ap.parse_args()
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
