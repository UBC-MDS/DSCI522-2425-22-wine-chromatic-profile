# Wine Chromatic Profile Classification
Authors: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang

DSCI 522 (Data Science Workflows) Project

# About
Here we attempt to build a classification model to predict the class of wine (red or white) based on the physiochemical properties (e.g. acidity, sulphates, citric acid, etc.). We used logistic regression model for our predictions, with our classifier performing well on unseen data with 0.99 test score, misclassifying 15 out 1950 instances.
<br> <br>
The data set we used in this project was created by By P. Cortez, A. Cerdeira, Fernando Almeida, Telmo Matos, J. Reis. 2009 as part of Decision Support Systems publication, and is available on UCI Machine Learning Repository [here](https://archive.ics.uci.edu/dataset/186/wine+quality). 

# Report
The final report can be found [here](https://ubc-mds.github.io/DSCI522-2425-22-wine-chromatic-profile/).

# Usage and Dependencies
The conda environment file wine_environment.yaml contains all library dependencies used in this project. To reproduce the repot, follow these steps:
1. Clone this repository `git clone`
2. Create the environment (you only need to do this once): run 
    `conda env create -f environment.yaml`   
        or  
    `conda-lock install --name WINE conda-lock.yml`  

    Note if using conda lock, need to install these two packages as well:  
    `conda install -c conda-forge conda-lock`  
    `conda install -c conda-forge mamba`  
3. Launch Jupyter Lab from your base environment, and select the `wine` kernel from within Jupyter.

# References
Cortez P, Cerdeira A, Almeida F, Matos T, Reis J. Wine Quality [dataset]. 2009. UCI Machine Learning Repository. Available from: https://doi.org/10.24432/C56S3T.

