import os
import zipfile
import kaggle


def ensure_dataset():
    dataset_path = '../src/data/dataset.csv'
    if os.path.isfile(dataset_path):
        print('Dataset exists, skipping import.')
        return
    else:
        print('No dataset found. Importing dataset.')

        # Set dataset name from Kaggle
        dataset = 'maharshipandya/-spotify-tracks-dataset'
        data_dir = 'src/data'

        # Ensure the data directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Download dataset using Kaggle API
        kaggle.api.dataset_download_files(dataset, path=data_dir, unzip=True)

        print('Dataset downloaded and extracted to:', data_dir)

if __name__ == "__main__":
    ensure_dataset()