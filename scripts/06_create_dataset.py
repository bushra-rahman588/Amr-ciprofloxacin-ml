import pandas as pd

print("STEP 6 — DATASET CREATION")


# -----------------------
# Load files
# -----------------------

features = pd.read_csv("data/processed/features.csv")

pheno = pd.read_csv("data/raw/phenotype/ecoli_cipro.csv")

mapping = pd.read_csv("data/interim/mapping/biosample_to_assembly.csv")


print("Features:", len(features))
print("Phenotype:", len(pheno))
print("Mapping:", len(mapping))


# -----------------------
# Keep one assembly per biosample
# -----------------------

mapping = mapping.drop_duplicates("#BioSample")


# -----------------------
# Merge phenotype with assembly
# -----------------------

pheno = pheno.merge(
    mapping,
    on="#BioSample",
    how="inner"
)

print("After mapping:", len(pheno))


# -----------------------
# Convert MIC
# -----------------------

pheno["MIC"] = pd.to_numeric(pheno["MIC (mg/L)"], errors="coerce")


# -----------------------
# Label definition
# Resistant ≥ 1 mg/L
# -----------------------

pheno["Label"] = (pheno["MIC"] >= 1).astype(int)


# -----------------------
# Merge with features
# -----------------------

df = features.merge(
    pheno,
    on="Assembly",
    how="inner"
)

print("Final samples:", len(df))


# -----------------------
# Save dataset
# -----------------------

df.to_csv("data/processed/ml_dataset.csv", index=False)

print("Saved → data/processed/ml_dataset.csv")