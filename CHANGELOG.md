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
**Fix 1:**: No Fix. In our readme, we explicitly tell the user to remove the existing local files first. Therefore, we do not run into this issue. <br>

### Milestone 2 Feedback
- N/A

### Peer Review Feedback
- **Issue 1:** docker URL takes you to a screen with just a 'data' folder.  <br>
**Fix 1:**: Updated docker compose file <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/blob/d37bba2193b7e2b15fde5d52fc55361c8232dd0d/docker-compose.yml)

- **Issue 2:** The directory contains cache files, such as .ipynb_checkpoints, that are being pushed to GitHub.  <br>
**Fix 2:**: Updated .gitignore to not track ipynb_checkpoints <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/d37bba2193b7e2b15fde5d52fc55361c8232dd0d)

- **Issue 3:** Include a license section with links directly in the README.  <br>
**Fix 3:**: Updated README with a small license section <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/d37bba2193b7e2b15fde5d52fc55361c8232dd0d)

- **Issue 4:** The introduction and conclusion lack details regarding the potential use cases of the data and the broader impact of the model..  <br>
**Fix 4:**: Updated Introduction and Summary to emphasize more on use cases and broader importance <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/1ea412b46c309bede9839263c5b273db046533cd)

- **Issue 5:** A little more flushed-out explanation of the figures.  <br>
**Fix 5:**: More flushed out explanation added <br>
[Commit Link](https://github.com/UBC-MDS/DSCI522-2425-22-wine-chromatic-profile/commit/29e1e5b9427cc202c8119da2a91e5e656b47063e#diff-059ae229d14bfbf15abe1e3587fcff94884f9497fffa3b5bdf6c2ff3e94f44d4R113)

- **Issue 6:** The PDF link in Other Formats under the html report is not working.  <br>
**Fix 6:**: Not Fixed. Not within scope of this project <br>