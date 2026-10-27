# Scripturi GitHub

Toate scripturile sunt **idempotente**: le poți rula din nou fără efecte duble. Rulează-le din rădăcina repository-ului, în Git Bash, cu `gh` autentificat.

| Script | Ce face | Când |
|---|---|---|
| `setup.sh` | creează repository-ul privat, apoi `develop` și ramurile personale, setările (doar merge commit), protecția pentru `main`/`develop`, etichetele, milestone-urile S0–S4, issue-urile și invitațiile; opțional, board-ul Project | o dată (deja rulat la bootstrap) |
| `build_issues.py` | regenerează `issues.json` din ghiduri (`docs/team/*.md`) și din backlog | după ce modifici task-urile din ghiduri |
| `create_issues.py` | creează issue-urile lipsă din `issues.json` (apelat de `setup.sh`) | după `build_issues.py` |
| `add-members.sh` | invită colegii (`M=user K=user …` sau din `team.env`) și afișează liniile de activat în CODEOWNERS | când afli username-urile |
| `assign-issues.sh` | atribuie fiecare issue proprietarului lui, după eticheta `owner:<ID>` | după ce colegii acceptă invitațiile |

```bash
bash scripts/github/add-members.sh M=<user> K=<user> A=<user> R=<user>
# ... colegii acceptă invitațiile ...
bash scripts/github/assign-issues.sh
```

**Board-ul Project:** token-ul `gh` are nevoie de scope-ul `project`. Rulează `gh auth refresh -s project`, apoi din nou `bash scripts/github/setup.sh`.
