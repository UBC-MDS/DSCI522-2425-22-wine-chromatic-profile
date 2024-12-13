# Authors: Farhan Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# Date: 2024-12-10

# This Makefile automates the analysis pipeline for wine-chromatic-profile data.
# It handles data acquisition, splitting, validation, exploratory data analysis (EDA),
# model building, model evaluation, and finally, report generation in both HTML and PDF.
#
# Example usage:
#   make all

## SCRIPTS
SC_DOWN = scripts/download.py
SC_CLEAN = scripts/clean_n_split_data.py
SC_VAL = scripts/validation_before_split.py
SC_EDA = scripts/eda_n_correlation_check.py
SC_MOD = scripts/preprocessing.py
SC_EVAL = scripts/model_evaluation_wine_predictor.py

## MARKERS
SPLIT = data/proc/wine_train.csv data/proc/wine_test.csv
VALIDATE = results/markers/.validate_done
EDA = \
	results/tables/feature_datatypes.csv \
	results/tables/summary_statistics.csv  \
	results/figures/feature_correlation.png \
	results/figures/feature_densities_by_class.png

MODEL = results/models/wine_pipeline.pickle
EVAL = \
	results/models/wine_random_search.pickle \
	results/tables/cross_validation.csv \
	results/tables/drift_score.csv \
	results/tables/random_search.csv \
	results/tables/test_scores.csv \
	results/figures/confusion_matrix.png \
	results/figures/pr_curve.png

## INTERPRETER
P = python


all: quarto

./data/raw/wine.csv: ${SC_DOWN}
	${P} ${SC_DOWN} --id 186 --save_to ./data/raw/wine.csv

${SPLIT}: ${SC_CLEAN} data/raw/wine.csv
	${P} ${SC_CLEAN} --raw-data ./data/raw/wine.csv
   
${VALIDATE}: ${SC_VAL} data/raw/wine.csv
	${P} ${SC_VAL} --file_name wine.csv --data_path ./data/raw
	touch ${VALIDATE}

${EDA}: ${SC_EDA} ${VALIDATE} ${SPLIT}
	${P} ${SC_EDA} \
    --train-file ./data/proc/wine_train.csv \
    --output-img ./results/figures --output-table ./results/tables

${MODEL}: ${SC_MOD} ${SPLIT}
	${P} ${SC_MOD} --pipe-to ./results/models

${EVAL}: ${SC_EVAL} ${MODEL}
	${P} ${SC_EVAL} \
	--train-data ./data/proc/wine_train.csv --test-data ./data/proc/wine_test.csv \
	--pipeline-path ./results/models/wine_pipeline.pickle \
	--table-to ./results/tables \
	--plot-to ./results/figures

quarto: report/report.qmd ${EDA} ${EVAL}
	quarto render report/report.qmd --to html
	quarto render report/report.qmd --to pdf
	cp report/* docs/
	mv docs/report.html docs/index.html


## CLEAN
clean-tables :
	rm -f results/tables/*

clean-figures :
	rm -f results/figures/*

clean-models :
	rm -f results/models/*

clean-data :
	rm -f data/raw/*
	rm -f data/proc/*

clean-markers :
	rm -f ${VALIDATE}

clean : clean-data clean-tables clean-figures clean-models clean-markers
	rm -f report/report.html
	rm -f report/report.pdf
	rm -f docs/*


.PHONY: \
	all quarto \
	clean-data clean-tables clean-figures clean-models clean-markers clean