import pandas as pd

dev_df = pd.read_parquet("./data/processed/dev.parquet")
print(dev_df.head())
print(dev_df.shape)
print(60 * "#")

test_df = pd.read_parquet("./data/processed/test.parquet")
print(test_df.head())
print(test_df.shape)
print(60 * "#")

train_df = pd.read_parquet("./data/processed/train.parquet")
print(train_df.head())
print(train_df.shape)
print(60 * "#")