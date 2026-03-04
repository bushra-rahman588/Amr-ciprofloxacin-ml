import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score


print("MODEL VALIDATION / BIAS CHECK")


# Load dataset


df = pd.read_csv("data/processed/ml_dataset_advanced.csv")


# Fix mutation column if duplicated

if "mutation_count_x" in df.columns:
    df["mutation_count"] = df["mutation_count_x"]

elif "mutation_count_y" in df.columns:
    df["mutation_count"] = df["mutation_count_y"]


# Feature set (same as Step 7B)


features = [
    "qnr",
    "aac6",
    "oqx",
    "qep",
    "gyrA_mut",
    "parC_mut",
    "GenomeSize",
    "Contigs",
    "total_amr_genes",
    "mutation_count",
    "quinolone_gene_count"
]

X = df[features]
y = df["Label"]



# Handle groups


if "Group" in df.columns:
    groups = df["Group"].values
else:
    groups = np.arange(len(df))


# 1. Label balance check


print("\nLABEL DISTRIBUTION")
print(df["Label"].value_counts())

print("Resistance ratio:", df["Label"].mean())


# 2. Group leakage check

print("\nGROUP LEAKAGE CHECK")

gkf = GroupKFold(n_splits=5)

for train_idx, test_idx in gkf.split(X, y, groups):

    train_groups = set(groups[train_idx])
    test_groups = set(groups[test_idx])

    overlap = train_groups.intersection(test_groups)

    print("Train size:", len(train_idx))
    print("Test size:", len(test_idx))

    print("Unique train groups:", len(train_groups))
    print("Unique test groups:", len(test_groups))

    print("Group overlap:", len(overlap))

    break


# 3. Group-aware CV

print("\nRUNNING GROUP-AWARE CV")

aucs = []

for train_idx, test_idx in gkf.split(X, y, groups):

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X.iloc[train_idx], y.iloc[train_idx])

    probs = model.predict_proba(X.iloc[test_idx])[:,1]

    auc = roc_auc_score(y.iloc[test_idx], probs)

    aucs.append(auc)


print("GROUP CV AUROC:", np.mean(aucs))

# 4. Permutation Test

print("\nRUNNING PERMUTATION TEST")

y_perm = y.sample(frac=1, random_state=42).reset_index(drop=True)

perm_aucs = []

for train_idx, test_idx in gkf.split(X, y_perm, groups):

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X.iloc[train_idx], y_perm.iloc[train_idx])

    probs = model.predict_proba(X.iloc[test_idx])[:,1]

    auc = roc_auc_score(y_perm.iloc[test_idx], probs)

    perm_aucs.append(auc)


print("PERMUTATION AUROC:", np.mean(perm_aucs))


print("\nMODEL VALIDATION COMPLETE")