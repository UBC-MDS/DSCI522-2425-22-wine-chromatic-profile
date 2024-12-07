# eda_n_correlation_check.py
# author: Farhan Bin Faisal, Daria Khon, Adrian Leung, Zhiwei Zhang
# date: 2024-12-05

import os
import click
import pandas as pd
import altair as alt
import altair_ally as aly
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureLabelCorrelation, FeatureFeatureCorrelation

@click.command()
@click.option('--train-file', type=click.Path(exists=True), help='Path to the training dataset CSV file.', required=True)
@click.option('--output-img', type=click.Path(), help='Path to the directory to save images.', required=True)
@click.option('--output-table', type=click.Path(), help='Path to the directory to save table.', required=True)
def main(train_file, output_img, output_table):
    """Process EDA and save tables and plots combined with feature correlation check."""

    if not os.path.exists(output_img):
        os.makedirs(output_img)

    if not os.path.exists(output_table):
        os.makedirs(output_table)

    # Load datasets
    train_df = pd.read_csv(train_file)

    # Save feature datatypes and summary statistics
    datatype_path = os.path.join(output_table, "feature_datatypes.csv")
    train_df.info(buf=open(datatype_path, 'w'))
    print(f"Feature datatypes saved at: {datatype_path}")

    summary_path = os.path.join(output_table, "summary_statistics.csv")
    train_df.describe().to_csv(summary_path)
    print(f"Summary statistics saved at: {summary_path}")

    # Enable Altair VegaFusion
    alt.data_transformers.enable('vegafusion')

    # Figure 1: Distribution of Features per Target Class
    dist_plot = aly.dist(train_df, color = "color").properties(
        title="Distribution of Features per Target Class"
    )
    dist_plot_path = os.path.join(output_img, "feature_densities_by_class.png")
    dist_plot.save(dist_plot_path, scale_factor=2.0)
    print(f"Feature distribution plot saved at: {dist_plot_path}")

    # Figure 2: Correlation between Features
    corr_matrix = train_df.drop(columns=['color']).corr()
    corr_plot = aly.corr(corr_matrix).properties(
        title="Correlation between Wine Color Prediction Features"
    )
    corr_plot_path = os.path.join(output_img, "feature_correlation.png")
    corr_plot.save(corr_plot_path, scale_factor=2.0)
    print(f"Feature correlation plot saved at: {corr_plot_path}")

    # Deepchecks correlation validations
    wine_train_ds = Dataset(train_df, label="color", cat_features=[])

    # Feature-label correlation check
    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.8)
    check_feat_lab_corr_result = check_feat_lab_corr.run(dataset=wine_train_ds)

    if check_feat_lab_corr_result.passed_conditions():
        print("Feature-Label Correlation: PASSED")
    else:
        print("Feature-Label Correlation: FAILED")
        raise ValueError("Feature-Label correlation exceeds the maximum acceptable threshold.")

    # Feature-feature correlation check
    check_feat_feat_corr = FeatureFeatureCorrelation().add_condition_max_number_of_pairs_above_threshold(
        threshold=0.8, n_pairs=0
    )
    check_feat_feat_corr_result = check_feat_feat_corr.run(dataset=wine_train_ds)

    if check_feat_feat_corr_result.passed_conditions():
        print("Feature-Feature Correlation: PASSED")
    else:
        print("Feature-Feature Correlation: FAILED")
        raise ValueError("Feature-feature correlation exceeds the maximum acceptable threshold.")


if __name__ == '__main__':
    main()