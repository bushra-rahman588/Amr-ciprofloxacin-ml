import os
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

print("STEP — VARIANT EVOLUTION ANALYSIS")

folder = "data/interim/amrfinder"
files = glob(os.path.join(folder, "*.tsv"))

records = []

# --------------------------------------------------
#  QRDR mutations
# --------------------------------------------------

for f in files:

    assembly = os.path.basename(f).replace(".tsv", "")
    df = pd.read_csv(f, sep="\t", dtype=str)

    if "Subtype" not in df.columns:
        continue

    df = df[df["Subtype"] == "POINT"]

    if "Element symbol" not in df.columns:
        continue

    mutations = df["Element symbol"].dropna().unique()

    for mut in mutations:
        if "gyrA" in mut or "parC" in mut:
            records.append([assembly, mut])

variant_df = pd.DataFrame(records, columns=["Assembly", "Mutation"])

if variant_df.empty:
    print("No gyrA/parC mutations detected.")
    exit()

# --------------------------------------------------
# Create variant matrix
# --------------------------------------------------

variant_matrix = pd.crosstab(
    variant_df["Assembly"],
    variant_df["Mutation"]
)

variant_matrix = (variant_matrix > 0).astype(int)
variant_matrix.reset_index(inplace=True)

os.makedirs("data/processed", exist_ok=True)

variant_matrix.to_csv(
    "data/processed/variant_features.csv",
    index=False
)

print("Variant features saved.")
print("Mutation columns:", variant_matrix.columns.tolist())


# --------------------------------------------------
#  Merge with phenotype dataset
# --------------------------------------------------

dataset = pd.read_csv("data/processed/ml_dataset_advanced.csv")

merged = dataset.merge(variant_matrix, on="Assembly", how="left").fillna(0)

variant_cols = [c for c in variant_matrix.columns if c != "Assembly"]

merged["num_QRDR_mut"] = merged[variant_cols].sum(axis=1)


# --------------------------------------------------
# Print Evolution Summary
# --------------------------------------------------

print("\nMutation count distribution:")
print(merged["num_QRDR_mut"].value_counts())

print("\nMutation count vs Resistance:")
print(pd.crosstab(merged["num_QRDR_mut"], merged["Label"]))



# Generate Plots


os.makedirs("results/figures", exist_ok=True)

# Plot 1: Mutation distribution
plt.figure()
merged["num_QRDR_mut"].value_counts().sort_index().plot(kind="bar")
plt.xlabel("Number of QRDR Mutations")
plt.ylabel("Number of Genomes")
plt.title("QRDR Mutation Distribution")
plt.savefig("results/figures/qrdr_mutation_distribution.png", dpi=300)
plt.close()


# Plot 2: Mutation vs Resistance
ct = pd.crosstab(merged["num_QRDR_mut"], merged["Label"])

ct.plot(kind="bar")
plt.xlabel("Number of QRDR Mutations")
plt.ylabel("Number of Genomes")
plt.title("QRDR Mutations vs Resistance")
plt.legend(["Susceptible", "Resistant"])
plt.savefig("results/figures/qrdr_vs_resistance.png", dpi=300)
plt.close()


# Plot 3: Individual mutation frequency
mutation_freq = merged[variant_cols].sum().sort_values(ascending=False)

plt.figure()
mutation_freq.plot(kind="bar")
plt.xlabel("Mutation")
plt.ylabel("Frequency")
plt.title("QRDR Mutation Frequencies")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("results/figures/qrdr_individual_frequency.png", dpi=300)
plt.close()

print("Evolutionary plots saved.")