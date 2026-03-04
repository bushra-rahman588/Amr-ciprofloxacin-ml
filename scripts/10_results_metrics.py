import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import GroupKFold
from sklearn.metrics import (
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve
)

from sklearn.ensemble import RandomForestClassifier


print("STEP 9 — MODEL METRICS & RESULTS TABLE")


# -------------------------
# Load dataset
# -------------------------

df = pd.read_csv("data/processed/ml_dataset_advanced.csv")


# -------------------------
# Features
# -------------------------

features = [
    "qnr", "aac6", "oqx", "qep",
    "gyrA_mut", "parC_mut",
    "GenomeSize", "Contigs",
    "total_amr_genes",
    "mutation_count_x",
    "quinolone_gene_count"
]

X = df[features]
y = df["Label"]

# Use population group if exists
if "Group" in df.columns:
    groups = df["Group"]
else:
    groups = df["Assembly"]


# -------------------------
# Group CV Training
# -------------------------

gkf = GroupKFold(n_splits=5)

metrics = []

all_probs = []
all_true = []


for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups)):

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42
    )

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)[:, 1]
    preds = (probs > 0.5).astype(int)

    auc = roc_auc_score(y_test, probs)
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)

    metrics.append([fold, auc, acc, prec, rec, f1])

    all_probs.extend(probs)
    all_true.extend(y_test)


# -------------------------
# Metrics Table
# -------------------------

metrics_df = pd.DataFrame(
    metrics,
    columns=["Fold", "AUROC", "Accuracy", "Precision", "Recall", "F1"]
)

summary = metrics_df.mean().to_frame(name="Mean")
summary["SD"] = metrics_df.std()


print("\nFold Metrics:")
print(metrics_df)

print("\nSummary:")
print(summary)


# Save tables
metrics_df.to_csv("results/metrics_folds.csv", index=False)
summary.to_csv("results/metrics_summary.csv")


# -------------------------
# Confusion Matrix
# -------------------------

cm = confusion_matrix(all_true, (np.array(all_probs) > 0.5).astype(int))

plt.figure()
plt.imshow(cm, cmap="Blues")
plt.title("Confusion Matrix")
plt.colorbar()

plt.xlabel("Predicted")
plt.ylabel("True")

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.savefig("results/confusion_matrix.png", dpi=300)
plt.close()


# -------------------------
# ROC Curve
# -------------------------

fpr, tpr, _ = roc_curve(all_true, all_probs)
auc_total = roc_auc_score(all_true, all_probs)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {auc_total:.3f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig("results/metrics/roc_curve_final.png", dpi=300)
plt.close()


print("\nResults saved in metrics/")