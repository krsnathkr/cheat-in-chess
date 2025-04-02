import gdown
import zipfile
import os

url = "https://drive.google.com/uc?id=YOUR_FILE_ID"
output = "datasets.zip"

# Download from Google Drive
gdown.download(url, output, quiet=False)

# Unzip
with zipfile.ZipFile(output, 'r') as zip_ref:
    zip_ref.extractall("datasets")

# Optionally remove zip
os.remove(output)
