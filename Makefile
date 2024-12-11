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
SPLIT = results/markers/.split_done
VALIDATE = results/markers/.validate_done
EDA = results/markers/.EDA_done
MODEL = results/markers/.model_done
EVAL = results/markers/.eval_done

## INTERPRETER
P = python


all: quarto

./data/raw/wine.csv: ${SC_DOWN}
	${P} ${SC_DOWN} --id 186 --save_to ./data/raw/wine.csv


${SPLIT}: ${SC_CLEAN} data/raw/wine.csv
	${P} ${SC_CLEAN} --raw-data ./data/raw/wine.csv
	touch ${SPLIT}
   

${VALIDATE}: ${SC_VAL} data/raw/wine.csv
	${P} ${SC_VAL} --file_name wine.csv --data_path ./data/raw
	touch ${VALIDATE}


${EDA}: ${SC_EDA} ${VALIDATE} ${SPLIT}
	${P} ${SC_EDA} \
    --train-file ./data/proc/wine_train.csv \
    --output-img ./results/figures --output-table ./results/tables
	touch ${EDA}


${MODEL}: ${SC_MOD} ${EDA}
	${P} ${SC_MOD} --pipe-to ./results/models
	touch ${MODEL}


${EVAL}: ${SC_EVAL} ${MODEL}
	${P} ${SC_EVAL} \
	--train-data ./data/proc/wine_train.csv --test-data ./data/proc/wine_test.csv \
	--pipeline-path ./results/models/wine_pipeline.pickle \
	--table-to ./results/tables \
	--plot-to ./results/figures
	touch ${EVAL}


quarto: report/report.qmd ${EVAL}
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
	rm -f results/markers/*

clean : clean-data clean-tables clean-figures clean-models clean-markers
	rm -f report/report.html
	rm -f report/report.pdf
	rm -f docs/index.html


.PHONY: \
	all quarto \
	clean-data clean-tables clean-figures clean-models clean-markers clean