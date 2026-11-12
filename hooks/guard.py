#!/usr/bin/env python3
"""fsk guardrails — hooks do Claude Code (cross-platform, sem dependências).

Modos (argv[1]):
  git   PreToolUse/Bash  — nega o irreversível (--no-verify, --force, reset --hard);
                           pede confirmação em git push normal.
  env   PreToolUse/Read|Edit — nega ler/editar arquivos .env (segredo não entra no contexto).
  core  SessionStart     — injeta o núcleo fsk-workflow.md como contexto da sessão.

Decisão via stdout JSON (hookSpecificOutput.permissionDecision: deny|ask); exit 0 sempre.
Sem match, não imprime nada (deixa o fluxo normal).
"""
import sys, json, re, os
from pathlib import Path


def _input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def _pre(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


DENY_GIT = [
    (r"--no-verify", "hook/gate não pode ser contornado (--no-verify proibido)"),
    (r"\bpush\b.*(--force\b|--force-with-lease\b|\s-f\b)", "push forçado é destrutivo"),
    (r"\breset\s+--hard\b", "reset --hard apaga trabalho"),
    (r"\bclean\s+-[a-wyz]*f", "git clean -f apaga arquivos não rastreados"),
    (r"\bcheckout\s+--\s+\S", "checkout -- descarta mudanças locais"),
]


def mode_git(data):
    cmd = str((data.get("tool_input") or {}).get("command", ""))
    if not cmd.strip():
        sys.exit(0)
    for pat, why in DENY_GIT:
        if re.search(pat, cmd):
            _pre("deny", f"fsk: {why}. Faça diferente ou confirme fora do agente.")
    if re.search(r"\bgit\s+push\b", cmd):
        _pre("ask", "fsk: push publica. Passe pelo fsk-ship (dossiê + evidência + check-map) antes — confirme.")
    if re.search(r"\bgit\s+merge\b", cmd) and not re.search(r"--abort|--continue|--quit", cmd):
        _pre("ask", "fsk: merge entrega trabalho. Passe pelo fsk-review/fsk-ship antes — confirme.")
    sys.exit(0)


def mode_env(data):
    tool = data.get("tool_name", "")
    if tool not in ("Read", "Edit"):
        sys.exit(0)
    ti = data.get("tool_input") or {}
    path = str(ti.get("file_path") or ti.get("path") or "")
    base = os.path.basename(path)
    if re.match(r"^\.env(\.|$)", base) and not re.search(r"\.(example|sample|template|dist)$", base):
        _pre("deny", "fsk: .env tem segredo — não leia no contexto (use variável de ambiente ou peça o valor).")
    sys.exit(0)


def mode_core(_data):
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    core = Path(root) / "global" / "fsk-workflow.md" if root else Path(__file__).resolve().parent.parent / "global" / "fsk-workflow.md"
    if not core.exists():
        sys.exit(0)
    text = core.read_text(encoding="utf-8")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": text,
    }}))
    sys.exit(0)


_CODE_EXT = (".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".java", ".rb", ".php", ".cs", ".rs",
             ".kt", ".swift", ".vue", ".svelte")


def _git(args):
    import subprocess
    try:
        return subprocess.run(["git"] + args, capture_output=True, text=True).stdout
    except Exception:
        return ""


def _prod(f):
    return (f.endswith(_CODE_EXT)
            and not re.search(r"\.(test|spec)\.|/__tests__/|/tests?/|\.d\.ts$", f)
            and not f.startswith(("docs/", ".claude/", ".github/")))


def _proven():
    import glob
    for ev in glob.glob(".claude/specs/*/evidencias.md"):
        try:
            t = open(ev, encoding="utf-8", errors="ignore").read().lower()
        except Exception:
            continue
        if re.search(r"navegador|api real|integra|end-to-end|e2e|tentei subir", t):
            return True
    return False


def mode_stop(_data):
    # Reengate: turno mexeu em código de produção sem prova real → lembra (não bloqueia).
    files = _git(["diff", "--name-only", "HEAD"]).split()
    if [f for f in files if _prod(f)] and not _proven():
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "Stop", "additionalContext":
            "fsk: mexeu em código de produção sem prova real registrada. Antes de dizer 'pronto', invoque "
            "o fsk-prove no canal real (navegador/API) — suíte verde é checagem, não prova — e dê uma linha "
            "ao usuário sobre o estado (não encadeie tool calls em silêncio)."}}))
    sys.exit(0)


def main():
    if len(sys.argv) < 2:
        sys.exit(0)
    data = _input()
    {"git": mode_git, "env": mode_env, "core": mode_core, "stop": mode_stop}.get(
        sys.argv[1], lambda d: sys.exit(0))(data)


if __name__ == "__main__":
    main()
