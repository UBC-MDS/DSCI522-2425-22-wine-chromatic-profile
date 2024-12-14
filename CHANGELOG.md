### Milestone 1 Feedback

#### Data analysis project file and directory structure
- **Issue 1:** CHANGELOG.md, the email under "enforcement" should be tied to the team <br>
**Fix 1:**: changed email from daniel.chen@stat.ubc.ca (insstructor) to adrian72@student.ubc.ca (group member) <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/6e6b8ab327995610366721fcbc5ccc8a811e0949)

- **Issue 2:** data/ Raw and processed/intermediate data are mixed in the data directory (they should be in subfolders, or at least clearly labelled)  <br>
**Fix 2:**: changes data/ directory organization to raw and proc for raw and processed data <br>
[Repo Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/tree/main/data)

- **Issue 3:** environment.yaml, versions are missing from environment files(s) for some R or Python packages  <br>
**Fix 3:**: all packagaes now contain versions <br>
[Repo Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/blob/main/environment.yaml)

#### Data analysis
- **Issue 4:** Abstract/Summary (1) Does not clearly report the major findings.(2) Does not discuss importance and limitations of findings <br>
**Fix 4:**: added necessary information to the Abstract section in the report <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/8fbb5e7b869f735298af7b2d4becdaef04406de7)

- **Issue 5:** Introduction did not reference the data set when referring to it. <br>
**Fix 5:**: added necessary information to the Introduction section in the report <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/pull/42/commits/d1027594cdc0eb64a6454a6d5f974d3d47322d24#diff-fa254b0baa203c4613b5d7f41b686e1e167c0c4a04337d13198e397607cff187)

- **Issue 6:** Discussion (1) Findings from project are not linked back to the application domain. (2) Assumptions and limitations of methods and findings are not discussed. <br>
**Fix 6:**: added necessary information to the Discussion section in the report <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/pull/71/commits/6e5a2095e6c59f07a0d8a1f634e6fe2252d87c6a)

- **Issue 7:** Spelling and grammar, there were just a couple spelling or grammatical errors. <br>
**Fix 7:**: Report editted and reviewed for grammar and spelling <br>
[Repo Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/pull/71/commits/8b0f2dfc62164104e4e451de992fe53184a53fe1)

### Milestone 2 Feedback

#### Reproducibility
- **Issue 1:** Latest tag was used for docker. This is not ideal because if the user has latest locally, but there is a newer version on the container registry, then Docker will not pull it.<br>
**Fix 1:**: ??? <br>
[Commit Link](INSERT)


#### Peer Review Feedback
- **Issue 1:** .gitignore needs to be updated<br>
**Fix 1:**: Updated docker compose file <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/8298ca39f9a149c78408b036c89eb7eed3649f39#diff-e45e45baeda1c1e73482975a664062aa56f20c03dd9d64a827aba57775bed0d3)

- **Issue 2:** docker URL takes you to a screen with just a 'data' folder.  <br>
**Fix 2:**: Updated to not track ipynb_checkpoints <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/119e66c9c678f4fb7c6465323f793a482b5baaf2)