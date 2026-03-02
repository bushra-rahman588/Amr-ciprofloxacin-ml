import os
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.ensemble import RandomForestClassifier


print("STEP 7B — POPULATION AWARE ML")


genome_dir = "data/interim/genomes"
dataset_path = "data/processed/ml_dataset_advanced.csv"


# -------------------------
# 1. Mash sketch
# -------------------------

print("Running Mash sketch...")

subprocess.run(
    f"mash sketch {genome_dir}/*.fna -o mash_db",
    shell=True,
    check=True
)


# -------------------------
# 2. Mash distance
# -------------------------

print("Computing distances...")

subprocess.run(
    "mash dist mash_db.msh mash_db.msh > mash_dist.tsv",
    shell=True,
    check=True
)


# -------------------------
# 3. Create clusters
# -------------------------

dist = pd.read_csv(
    "mash_dist.tsv",
    sep="\t",
    header=None,
    usecols=[0, 1, 2],
    names=["g1", "g2", "dist"]
)

dist["g1"] = dist["g1"].apply(lambda x: os.path.basename(x).replace(".fna", ""))
dist["g2"] = dist["g2"].apply(lambda x: os.path.basename(x).replace(".fna", ""))


threshold = 0.01

clusters = {}
cluster_id = 0

for _, row in dist.iterrows():

    if row["dist"] < threshold:

        a = row["g1"]
        b = row["g2"]

        if a not in clusters and b not in clusters:
            clusters[a] = cluster_id
            clusters[b] = cluster_id
            cluster_id += 1

        elif a in clusters:
            clusters[b] = clusters[a]

        elif b in clusters:
            clusters[a] = clusters[b]


cluster_df = pd.DataFrame(
    list(clusters.items()),
    columns=["Assembly", "Group"]
)

print("Clusters:", cluster_df["Group"].nunique())


# -------------------------
# 4. Load dataset
# -------------------------

df = pd.read_csv(dataset_path)
# df = df.drop["mutation_count_y"]

df = df.merge(cluster_df, on="Assembly", how="left")

df["Group"] = df["Group"].fillna(-1)


# -------------------------
# 5. Prepare ML
# -------------------------

features = [
    "qnr", "aac6", "oqx", "qep",
    "gyrA_mut", "parC_mut",
    "GenomeSize", "Contigs",
    "total_amr_genes", "mutation_count_x",
    "quinolone_gene_count"
]

X = df[features]
y = df["Label"]
groups = df["Group"]


# -------------------------
# 6. GroupKFold training
# -------------------------

gkf = GroupKFold(n_splits=5)

aucs = []

for train_idx, test_idx in gkf.split(X, y, groups):

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model = RandomForestClassifier(n_estimators=200, random_state=42)

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, probs)

    aucs.append(auc)


print("Group CV AUROC:", np.mean(aucs))


# -------------------------
# 7. ROC Plot
# -------------------------

fpr, tpr, _ = roc_curve(y_test, probs)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC={auc:.3f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve (Group-aware)")
plt.legend()
plt.savefig("results/figures/roc_curve.png", dpi=300)
plt.close()


# -------------------------
# 8. Feature Importance Plot
# -------------------------

importances = model.feature_importances_

plt.figure()
plt.barh(features, importances)
plt.xlabel("Importance")
plt.title("Feature Importance")
plt.savefig("results/figures/feature_importance.png", dpi=300)
plt.close()


print("Plots saved in results/figures")