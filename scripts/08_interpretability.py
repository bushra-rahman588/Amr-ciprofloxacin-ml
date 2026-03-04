import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier


print("STEP 8 — INTERPRETABILITY ANALYSIS")


# -------------------------
# Load dataset
# -------------------------

df = pd.read_csv("data/processed/ml_dataset_advanced.csv")


# -------------------------
# Group check (SAFE)
# -------------------------

if "Group" in df.columns:
    print("\nGroup label distribution:")
    print(df.groupby("Group")["Label"].mean().head())
else:
    print("No Group column found — skipping group analysis")


# -------------------------
# Fix mutation column if needed
# -------------------------

if "mutation_count_x" in df.columns:
    df["mutation_count"] = df["mutation_count_x"]

elif "mutation_count_y" in df.columns:
    df["mutation_count"] = df["mutation_count_y"]

df = df.drop(
    columns=[c for c in df.columns if c.endswith("_x") or c.endswith("_y")],
    errors="ignore"
)


# -------------------------
# Feature Selection (BASE + VARIANTS)
# -------------------------

base_features = [
    "qnr", "aac6", "oqx", "qep",
    "gyrA_mut", "parC_mut",
    "GenomeSize", "Contigs",
    "total_amr_genes", "mutation_count",
    "quinolone_gene_count"
]

variant_cols = [
    col for col in df.columns
    if col.startswith("gyrA_") or col.startswith("parC_")
]

features = base_features + variant_cols
features = list(dict.fromkeys(features))

X = df[features]
y = df["Label"]


# -------------------------
# Train model (NO GROUP HERE)
# -------------------------

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X, y)


# -------------------------
# Feature Importance
# -------------------------

importance = model.feature_importances_

imp_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
}).sort_values("Importance", ascending=False)

print("\nTop Features:")
print(imp_df.head(15))


plt.figure(figsize=(7,5))
plt.barh(imp_df["Feature"][:15][::-1],
         imp_df["Importance"][:15][::-1])
plt.xlabel("Importance")
plt.title("Feature Importance")
plt.tight_layout()

plt.savefig("results/figures/feature_importance_interpret.png", dpi=300)
plt.close()


# -------------------------
# Mutation vs Phenotype
# -------------------------

print("\nMutation vs Resistance:")

print("\ngyrA_mut:")
print(pd.crosstab(df["gyrA_mut"], df["Label"]))

print("\nparC_mut:")
print(pd.crosstab(df["parC_mut"], df["Label"]))


# -------------------------
# Correlation Matrix
# -------------------------

corr = df[features + ["Label"]].corr()

plt.figure(figsize=(8,6))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(corr)), corr.columns, rotation=90)
plt.yticks(range(len(corr)), corr.columns)
plt.title("Feature Correlation")
plt.tight_layout()
plt.savefig("results/figures/correlation_matrix.png", dpi=300)
plt.close()


print("\nInterpretation plots saved.")