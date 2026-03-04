import os
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier

print("STEP 9 — SHAP EXPLAINABILITY (FIXED)")


# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("data/processed/ml_dataset_advanced.csv")

# Fix mutation_count naming if merge artifacts exist
if "mutation_count_x" in df.columns:
    df["mutation_count"] = df["mutation_count_x"]
elif "mutation_count_y" in df.columns:
    df["mutation_count"] = df["mutation_count_y"]

df = df.drop(columns=[c for c in df.columns if c.endswith("_x") or c.endswith("_y")], errors="ignore")


# -------------------------
# Features
# -------------------------
features = [
    "qnr", "aac6", "oqx", "qep",
    "gyrA_mut", "parC_mut",
    "GenomeSize", "Contigs",
    "total_amr_genes", "mutation_count",
    "quinolone_gene_count"
]

X = df[features].copy()
y = df["Label"].astype(int).copy()

# Make sure everything is numeric
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

print("X shape:", X.shape)
print("y shape:", y.shape)


# -------------------------
# Train model
# -------------------------
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X, y)


# -------------------------
# SHAP computation (robust across versions)
# -------------------------
print("Calculating SHAP values...")

explainer = shap.TreeExplainer(model)

# Newer SHAP preferred API
try:
    sv = explainer(X)  # Explanation object
    # For binary classification, sv.values can be:
    # (n, p) OR (n, p, 2)
    vals = sv.values
    if vals.ndim == 3:
        shap_matrix = vals[:, :, 1]   # class 1
    else:
        shap_matrix = vals            # already (n, p)
except Exception:
    # Older SHAP API
    sv = explainer.shap_values(X)
    if isinstance(sv, list):
        shap_matrix = sv[1]           # class 1
    else:
        # could be (n, p) or (n, p, 2)
        if sv.ndim == 3:
            shap_matrix = sv[:, :, 1]
        else:
            shap_matrix = sv

# Final sanity check
print("SHAP matrix shape:", shap_matrix.shape)
assert shap_matrix.shape == X.shape, f"Mismatch: SHAP {shap_matrix.shape} vs X {X.shape}"


# -------------------------
# Save plots
# -------------------------
os.makedirs("results/figures", exist_ok=True)

# Summary plot
plt.figure()
shap.summary_plot(shap_matrix, X, show=False)
plt.savefig("results/figures/shap_summary.png", dpi=300, bbox_inches="tight")
plt.close()

# Bar importance plot
plt.figure()
shap.summary_plot(shap_matrix, X, plot_type="bar", show=False)
plt.savefig("results/figures/shap_importance.png", dpi=300, bbox_inches="tight")
plt.close()

print("Saved:")
print(" - results/figures/shap_summary.png")
print(" - results/figures/shap_importance.png")