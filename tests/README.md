Run each test one by one in the `tests/` directory
```
pytest -v test_random_search.py \
    --train_data=../data/proc/wine_train.csv \
    --test_data=../data/proc/wine_test.csv \
    --pipeline_path=../results/models/wine_pipeline.pickle

pytest test_validate_column_names.py 

pytest test_split_data.py

pytest test_evaluation.py
```

Run all tests at once in the root directory with the command below: 
```
pytest -v \
    --train_data=data/proc/wine_train.csv \
    --test_data=data/proc/wine_test.csv \
    --pipeline_path=results/models/wine_pipeline.pickle
```
