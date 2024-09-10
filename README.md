# Cyberbullying Detection

## 📚 Project Overview
This project is focused on developing a deep learning model to detect and classify hate speech, toxic comments, and cyberbullying content on online platforms. The key goal is to create a robust, scalable, and reproducible MLOps pipeline for building and serving deep learning projects to the cloud.

The project is divided into four parts(each in its own repo). Refer to [Part 1](https://github.com/morpheus-101/cybulde-data) for details on project overview.
- Part 1: [Data collection and versioning](https://github.com/morpheus-101/cybulde-data)
- Part 2: [Distributed data processing](https://github.com/morpheus-101/cybulde-data-preparation)
- Part 3: [Distributed model training and evaluation](https://github.com/morpheus-101/cybulde-model)
- Part 4: [Deployment and web app](https://github.com/morpheus-101/cybulde-web-app)

This repository includes code for Part 2 only. 

---

# Part 2:
In Part 1, the datasets were versioned using DVC and stored in a Google Cloud Storage (GCS) bucket. In this section, the raw datasets are retrieved and transformed for cleaning and preprocessing. The transformed datasets are then stored in a new directory within GCS, tagged appropriately to indicate both the dataset version and the details of the transformations applied.

This processed dataset is later used to build a tokenizer using the tokenizers library from Huggingface (tokenizer construction was done on my local machine).

## Key Tools and Technologies
- **Dask**: Dask distributed used for setting up a dask scheduler and worker compute nodes.
- **GCS**: GCS bucket to retrieve raw dataset and store processed dataset.
- **GCP artifact registry**: To store docker images. 
- **HuggingFace tokenizers**: Tokeniziers library from huggingface was used to build a BPE tokenizer. 

## Distributed data processing setup
- A Docker image, containing the configuration file (managed with Hydra-core), required code, environment, dataset version, and transformation functions, is uploaded to the GCP Artifact Registry. Packaging these components together ensures seamless experiment reproducibility.
- A GCP instance group is created for Dask schedulers and worker nodes, with each VM instance in the group loaded with a Docker container built from the uploaded image.
- The configuration file specifies the dataset version to be used, enabling the appropriate raw dataset to be pulled from the GCS bucket into the Dask cluster nodes.
- Transformation functions defined in the configuration are applied to the raw dataset, and the processed data is stored in the same GCS bucket under a new directory.
- This setup enhances reproducibility by packaging the transformation functions and dataset version within the Docker container. Experiments can be traced back to the Docker image used to deploy the Dask cluster, providing detailed information on the configuration used for data processing.

<div style="text-align: center;">
  <img src="pictures/dask_setup.png" alt="My Image" width="100%" height="auto">
</div>