import pandas as pd

print("STEP 7A — ADVANCED FEATURE ENGINEERING")


# Load files
df = pd.read_csv("data/processed/ml_dataset.csv")
qc = pd.read_csv("data/interim/genome_qc.csv")
amr = pd.read_csv("data/interim/amr_merged.csv", dtype=str)

print("Dataset samples:", len(df))
print("AMR columns:", amr.columns.tolist())


# -----------------------
# Merge genome QC features
# -----------------------

qc_small = qc[["Assembly", "GenomeSize", "Contigs"]]

df = df.merge(qc_small, on="Assembly", how="left")


# -----------------------
# Total AMR genes
# -----------------------

burden = (
    amr.groupby("Assembly")
    .size()
    .reset_index(name="total_amr_genes")
)

df = df.merge(burden, on="Assembly", how="left")


# -----------------------
# Mutation count
# Use Subtype column (contains mutation info)
# -----------------------

mut = amr[amr["Subtype"].astype(str).str.contains("mutation", case=False, na=False)]

mut_count = (
    mut.groupby("Assembly")
    .size()
    .reset_index(name="mutation_count")
)

df = df.merge(mut_count, on="Assembly", how="left")


# -----------------------
# Quinolone gene count
# -----------------------

genes = amr["Element symbol"].astype(str).str.lower()

quin = amr[genes.str.contains("qnr|aac|oqx|qep", na=False)]

quin_count = (
    quin.groupby("Assembly")
    .size()
    .reset_index(name="quinolone_gene_count")
)

df = df.merge(quin_count, on="Assembly", how="left")


# Fill NA values
df = df.fillna(0)


# Save upgraded dataset
df.to_csv("data/processed/ml_dataset_advanced.csv", index=False)

print("Saved → data/processed/ml_dataset_advanced.csv")
print("Total samples:", len(df))