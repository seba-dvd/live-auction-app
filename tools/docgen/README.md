# docgen: documente Word în formatul șablonului UNITBV

Generează documente `.docx` (și PDF) din surse Markdown. Șablonul este [docs/templates/unitbv-template.docx](../../docs/templates/unitbv-template.docx), derivat din `Documentatie_Licenta.docx` cu `make_template.py`.

Documentul generat are:
- copertă cu sigla facultății;
- cuprins și liste de figuri, tabele și coduri;
- capitole numerotate automat;
- legende cu numerotare automată;
- antet diferit pe paginile pare și impare.

```bash
bash tools/docgen/build.sh               # toate: charter, raport, guides
bash tools/docgen/build.sh charter       # doar carta proiectului
NO_WORD=1 bash tools/docgen/build.sh     # doar .docx, fără Word (apoi F9 pe cuprins în Word)
```

- **Prima rulare:** creează `tools/docgen/.venv` și instalează python-docx.
- **Pe Windows cu Microsoft Word:** `update_fields.ps1` actualizează cuprinsul și listele și exportă PDF-ul.
- **Echipa de pe copertă:** se editează în [team.toml](team.toml).
- **Convențiile Markdown** sunt descrise în [docs/raport-tehnic/README.md](../../docs/raport-tehnic/README.md):
  - legendele de tabel (`Tabelul: ...` înaintea tabelului);
  - legendele de cod (`Codul: ...` după bloc);
  - figurile pe pagină orizontală (`{landscape}`);
  - titlurile nenumerotate (`{-}`).
