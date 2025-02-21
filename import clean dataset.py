import os
import zipfile
import kaggle

# Set dataset name from Kaggle
dataset = 'maharshipandya/-spotify-tracks-dataset'
data_dir = 'data'

# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

# Download dataset using Kaggle API
kaggle.api.dataset_download_files(dataset, path=data_dir, unzip=True)

print('Dataset downloaded and extracted to:', data_dir)