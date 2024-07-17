from dvc.api import get_url
import os

def get_remote_data_url(dataset_path: str) -> str:
    dvc_remote_repo = "https://github.com/morpheus-101/cybulde-data.git"
    version = "v2"
    dataset_url: str = get_url(path=dataset_path, repo=dvc_remote_repo, rev=version)
    return dataset_url

train_tsv_path = "./data/raw/ghc/ghc_train.tsv"
train_tsv_url = get_remote_data_url(train_tsv_path)
print(train_tsv_url)
