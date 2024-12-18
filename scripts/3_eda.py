# 3_eda.py
# author: Hui Tang
# date: 2024-12-07
# Usage: python scripts/3_eda.py  --train data/processed/train_df.csv --write-to results

import sys
import os

# Dynamically add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if src_path not in sys.path:
    sys.path.append(src_path)
import warnings
from altair.utils.deprecation import AltairDeprecationWarning
# Suppress 
warnings.filterwarnings("ignore", category=AltairDeprecationWarning)

import click
import pandas as pd
from eda_utils import (
    create_numeric_distributions,
    create_categorical_distributions,
    create_correlation_heatmap,
    save_high_correlations
)


@click.command()
@click.option(
    '--train',
    default='data/processed/train_df.csv',
    type=click.Path(exists=True),
    help='Path to the input training CSV file.'
)
@click.option(
    '--write-to',
    default='results',
    type=click.Path(),
    help='Directory where output figures will be saved.'
)
def main(train, write_to):
    # Ensure output directories exist
    output_dir = os.path.join(write_to, "figures")
    table_dir = os.path.join(write_to, "tables")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(table_dir, exist_ok=True)

    print("Generating EDA outputs...")
    
    # Load data
    train_df = pd.read_csv(train)

    # Define numeric and categorical columns
    numeric_columns = [
        'Age (in years)',
        'Resting blood pressure (in mm Hg on admission to the hospital)',
        'Serum cholesterol (in mg/dl)',
        'Maximum heart rate achieved',
        'ST depression induced by exercise relative to rest',
        'Number of major vessels (0–3) colored by fluoroscopy'
    ]
    categorical_columns = [
        'Sex',
        'Chest pain type',
        'Fasting blood sugar > 120 mg/dl',
        'Resting electrocardiographic results',
        'Exercise-induced angina',
        'Slope of the peak exercise ST segment',
        'Thalassemia'
    ]

    # Handle nulls for categorical columns
    train_df = train_df.dropna(subset=categorical_columns)

    # Call EDA functions
    create_numeric_distributions(train_df, numeric_columns, output_dir)
    create_categorical_distributions(train_df, categorical_columns, output_dir)
    create_correlation_heatmap(train_df, numeric_columns, output_dir)
    save_high_correlations(train_df, numeric_columns, table_dir)

    print("EDA outputs generated.")

if __name__ == "__main__":
    main()
