# Cum contribui

Regulile de lucru cu Git și GitHub pentru echipa Live Auction App. Sunt obligatorii, pentru că ne țin ramurile integrabile până la final.

## 1. Ramuri

| Ramură | Rol | Cine scrie în ea |
|---|---|---|
| `main` | Stabilă, gata de demo. Primește doar PR-uri din `develop`, la final de sprint. D face merge-ul și pune tag-ul `v0.<sprint>.0`. | nimeni direct |
| `develop` | Integrare. Primește doar PR-uri din ramurile personale. | nimeni direct |
| `d/user-gateway` | D: `user-service`, `api-gateway` | D |
| `m/bidding` | M: `bidding-service`, contracte, arhitectură | M |
| `k/auction` | K: `auction-service`, baza de date | K |
| `a/frontend` | A: `frontend`, backlog | A |
| `r/devops` | R: `notification-service`, Docker, CI/CD, Postman | R |

- **Ramurile personale sunt de lungă durată.** Proprietarul face push liber în ele, fără PR.
- **Protecția pentru `main` și `develop`:** e nevoie de PR cu o aprobare, aprobările vechi se anulează la un push nou, iar force-push și ștergerea sunt interzise.
- **Merge doar cu merge commit.** Fără squash sau rebase, ca ramurile de lungă durată să rămână ușor de sincronizat.
- **Ramurile nu se șterg** după merge.

## 2. Cine ce modifică

- **Folderele tale:** modifici doar folderele pe care le deții (vezi tabelul din [README.md](README.md#echipa) și ghidul tău din `docs/team/`).
- **Fișierele comune** se schimbă doar prin PR, cu proprietarul lor ca reviewer:
  - `docker-compose*.yml`, `.github/`, `db/`, `postman/`: R
  - `docs/api-contracts.md`, `docs/architecture.md`: M
  - fișierele din rădăcină, `docs/team/`: D
- **`CODEOWNERS`** cere automat review-ul proprietarului. Setarea „Require review from Code Owners” rămâne dezactivată intenționat, altfel un proprietar unic și-ar bloca propriile PR-uri.

**Cine face review (autor → reviewer):** D → M · M → D · K → M · A → K · R → D.

## 3. Comenzi zilnice

```bash
# dimineața: actualizează-te cu develop
git checkout <ramura-ta>
git fetch origin
git merge origin/develop

# lucrezi, apoi salvezi des, în pași mici
git status
git add <fișiere>
git commit -m "feat(auction): add auction status filter"
git push origin <ramura-ta>
```

**Prima dată după clonare:** `git checkout <ramura-ta>`. Git creează automat ramura locală care urmărește `origin/<ramura-ta>`.

## 4. Pull request către `develop`

1. Verifică local:
   - backend: `./mvnw -B verify` în folderul serviciului;
   - front-end: `npm run build` în `frontend/`.
2. Fă push pe ramura ta și deschide PR-ul:
   ```bash
   gh pr create --base develop --head <ramura-ta> --fill
   ```
   Sau din interfața GitHub: **Compare & pull request**, cu baza `develop`.
3. Completează șablonul. Corpul PR-ului conține `Closes #<număr-issue>`.
4. Adaugă reviewer-ul din harta de mai sus. CI-ul trebuie să fie verde.
5. După aprobare, autorul face **Merge pull request** (merge commit).
6. **Toți membrii** se sincronizează: `git fetch origin && git merge origin/develop`.

## 5. Conflicte de merge

Un conflict apare când două ramuri au modificat aceleași linii. Pașii:

```bash
git fetch origin
git merge origin/develop          # Git raportează: CONFLICT (content): Merge conflict in <fișier>
git status                        # lista fișierelor în conflict ("both modified")
```

Deschide fiecare fișier în conflict. În IntelliJ folosește **Git → Resolve Conflicts…** (vizualizare pe 3 coloane). Manual, caută marcajele:

```text
<<<<<<< HEAD
versiunea ta
=======
versiunea din develop
>>>>>>> origin/develop
```

Păstrează combinația corectă, șterge marcajele, apoi:

```bash
git add <fișier>
git commit                        # mesajul de merge e propus automat
./mvnw -B verify                  # sau npm run build: verifică că totul compilează
git push origin <ramura-ta>
```

Dacă te-ai încurcat, rulează `git merge --abort` ca să revii la starea dinainte. Apoi cere ajutor pe chat. **Nu folosi `push --force`.**

## 6. Convenții pentru commit-uri (Conventional Commits)

Formatul este `tip(scop): descriere scurtă, în engleză, la imperativ`.

- **Tipuri:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`, `style`.
- **Scopuri:** `gateway`, `user`, `auction`, `bidding`, `notification`, `frontend`, `infra`, `db`, `docs`, `postman`.
- **Exemple:**
  - `feat(bidding): reserve funds before bid-placed call`
  - `fix(frontend): sync countdown with serverTime`
  - `docs(database): add ER diagram for auction_db`

Un commit face un singur lucru logic. Nu face commit cu cod care nu compilează pe ramura ta, dacă poți evita asta.

## 7. Definition of Done

Un task e „gata” când:

- [ ] codul compilează și testele trec local: `./mvnw -B verify` / `npm run build`;
- [ ] criteriile „Gata când…” din ghid sau din issue sunt îndeplinite;
- [ ] există teste pentru logica nouă (unit și, unde e cazul, de integrare);
- [ ] `docs/api-contracts.md` e actualizat dacă s-a schimbat un contract (aprobat de M);
- [ ] colecția Postman e actualizată pentru endpoint-urile noi sau modificate;
- [ ] nu există secrete în cod, iar configurația vine din variabile de mediu cu valori implicite de dezvoltare;
- [ ] PR-ul spre `develop` e aprobat, CI-ul e verde, iar issue-ul se închide prin `Closes #…`;
- [ ] funcționalitatea merge în stack-ul complet: `docker compose up -d --build`.

## 8. Issues și board

- **Un issue per task.** Fiecare task din ghiduri are un issue `[<ID>-S<n>-<nn>] <titlu>`, cu etichete `owner:*`, `area:*`, `type:*`, `priority:*` și milestone-ul sprintului.
- **Bug-uri și user stories:** folosește șabloanele din **New issue**.
- **Board:** Scrum Master-ul (K) ține board-ul la zi. Tu muți cardul tău în **In progress** și apoi în **Done**.
