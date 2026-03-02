from pathlib import Path
import pandas as pd
from tqdm import tqdm
import yaml

print("STEP 4 SCRIPT STARTED")

# Load config
cfg = yaml.safe_load(open("configs/config.yaml"))

genomes_dir = Path(cfg["genomes_dir"])
amr_dir = Path(cfg["amrfinder_dir"])

print("Genomes dir:", genomes_dir)
print("AMR dir:", amr_dir)

genomes = list(genomes_dir.glob("*.fna"))
print("Genomes found:", len(genomes))


# -------------------------
# Genome QC
# -------------------------

qc_rows = []

for g in tqdm(genomes, desc="Reading FASTA"):

    acc = g.stem
    size = 0
    contigs = 0

    with open(g) as f:
        for line in f:
            if line.startswith(">"):
                contigs += 1
            else:
                size += len(line.strip())

    qc_rows.append([acc, size, contigs])


qc_df = pd.DataFrame(qc_rows, columns=["Assembly", "GenomeSize", "Contigs"])

qc_df["PassQC"] = (
    (qc_df["GenomeSize"] > 4_000_000) &
    (qc_df["GenomeSize"] < 6_500_000) &
    (qc_df["Contigs"] < 500)
)

qc_df.to_csv("data/interim/genome_qc.csv", index=False)

print("QC saved")


# -------------------------
# Merge AMRFinder
# -------------------------

records = []

for file in tqdm(amr_dir.glob("*.tsv"), desc="Merging AMR"):

    acc = file.stem

    try:
        df = pd.read_csv(file, sep="\t", dtype=str)

        if df.empty:
            continue

        df["Assembly"] = acc
        records.append(df)

    except Exception:
        continue


if records:
    amr_all = pd.concat(records, ignore_index=True)
else:
    amr_all = pd.DataFrame()


amr_all.to_csv("data/interim/amr_merged.csv", index=False)

print("AMR merged saved")

print("DONE")