import subprocess
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import shutil
import yaml


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


# -------------------------
# Load config
# -------------------------

cfg = yaml.safe_load(open("configs/config.yaml"))

mapping_file = cfg["mapping_out"]

df = pd.read_csv(mapping_file)

assemblies = df["Assembly"].dropna().astype(str).unique().tolist()

print("Total assemblies:", len(assemblies))


# -------------------------
# Output folder
# -------------------------

genome_dir = Path(cfg["genomes_dir"])
genome_dir.mkdir(parents=True, exist_ok=True)


# -------------------------
# Download genomes
# -------------------------

for acc in tqdm(assemblies, desc="Downloading genomes"):

    fna_file = genome_dir / f"{acc}.fna"

    # Skip if already downloaded
    if fna_file.exists():
        continue

    zip_file = genome_dir / f"{acc}.zip"

    try:
        # Download genome package
        run(f"datasets download genome accession {acc} --include genome --filename {zip_file}")

        # Unzip
        run(f"unzip -o {zip_file} -d {genome_dir}/{acc}")

        # Locate genomic fasta
        extracted = list(Path(genome_dir / acc).glob("ncbi_dataset/data/*/*genomic.fna"))

        if extracted:
            shutil.copy(extracted[0], fna_file)

    except Exception as e:
        print("Failed:", acc, e)


print("\nDownload complete")

print("Total genomes downloaded:", len(list(genome_dir.glob("*.fna"))))