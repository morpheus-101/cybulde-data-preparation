import pandas as pd

train_df = pd.read_parquet("gs://rbd-mlflow/data/processed/rebalanced_splits/train.parquet")
print(train_df.head())
print(train_df.shape)
print(60 * "#")