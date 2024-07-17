from hydra.utils import instantiate
from dask.distributed import Client
import dask.dataframe as dd
from cybulde.config_schemas.data_processing.dataset_cleaners_schema import DatasetCleanerManagerConfig
from cybulde.config_schemas.data_processing_config_schema import DataProcessingConfig
from cybulde.utils.config_utils import get_pickle_config, custom_instantiate, get_config
from cybulde.utils.data_utils import get_raw_data_with_version, filter_based_on_minimum_number_of_words
from cybulde.utils.gcp_utils import access_secret_version
from cybulde.utils.utils import get_logger
from cybulde.utils.io_utils import write_yaml_file
from pathlib import Path
import os


def process_raw_data(
    df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManagerConfig
) -> dd.core.Series:
    return df_partition["text"].apply(dataset_cleaner_manager)


@get_pickle_config(config_path="cybulde/configs/automatically_generated", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")
    processed_data_save_dir = config.processed_data_save_dir

    cluster = custom_instantiate(config.dask_cluster)
    client = Client(cluster)

    try:
        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)

        df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)

        logger.info("Cleaning data...")
        df = df.assign(
            cleaned_text=df.map_partitions(
                process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager, meta=("text", "object")
            )
        )
        df = df.compute()
        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        train_df = df[df["split"] == "train"]
        dev_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        train_df = filter_based_on_minimum_number_of_words(train_df, min_nrof_words=config.min_nrof_words)
        dev_df = filter_based_on_minimum_number_of_words(dev_df, min_nrof_words=config.min_nrof_words)
        test_df = filter_based_on_minimum_number_of_words(test_df, min_nrof_words=config.min_nrof_words)

        train_df.to_parquet(train_parquet_path)
        dev_df.to_parquet(dev_parquet_path)
        test_df.to_parquet(test_parquet_path)

        docker_info = {"docker_image": config.docker_image_name, "docker_tag": config.docker_image_tag}
        docker_info_save_path = os.path.join(processed_data_save_dir, "docker_info.yaml")

        write_yaml_file(docker_info_save_path, docker_info)

        logger.info("Data processing finished!")

    finally:
        logger.info("Closing dask client and cluster...")
        client.close()
        cluster.close()


if __name__ == "__main__":
    process_data()  # type: ignore
