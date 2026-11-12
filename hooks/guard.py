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
        _pre("ask", "fsk: push publica — confirme (destrutivo só com 'ok').")
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


def main():
    if len(sys.argv) < 2:
        sys.exit(0)
    data = _input()
    {"git": mode_git, "env": mode_env, "core": mode_core}.get(sys.argv[1], lambda d: sys.exit(0))(data)


if __name__ == "__main__":
    main()
