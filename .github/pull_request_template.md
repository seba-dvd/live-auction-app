## Ce face acest PR

<!-- 1–3 propoziții: ce s-a schimbat și de ce. -->

Closes #

## Tip

- [ ] feat · [ ] fix · [ ] docs · [ ] test · [ ] refactor · [ ] chore/ci/build

## Cum se testează

<!-- Comenzi, cereri Postman, pași în UI. -->

## Definition of Done

- [ ] Compilează și testele trec local (`./mvnw -B verify` / `npm run build`)
- [ ] Criteriile „Gata când…” ale task-ului sunt îndeplinite
- [ ] Teste pentru logica nouă
- [ ] `docs/api-contracts.md` actualizat, dacă s-a schimbat un contract (aprobare M)
- [ ] Colecția Postman actualizată pentru endpoint-uri noi sau modificate
- [ ] Fără secrete în cod; configurație prin variabile de mediu
- [ ] Am modificat doar folderele mele (sau am cerut review proprietarului)
- [ ] Merge în stack-ul complet (`docker compose up -d --build`)
