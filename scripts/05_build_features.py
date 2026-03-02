import pandas as pd

print("STEP 5 — FEATURE BUILDING")


# -----------------------
# Load files
# -----------------------

amr = pd.read_csv("data/interim/amr_merged.csv", dtype=str)
qc = pd.read_csv("data/interim/genome_qc.csv")

print("Columns in AMR file:")
print(amr.columns.tolist())


# -----------------------
# Column names
# -----------------------

gene_col = "Element symbol"
subtype_col = "Subtype"


# -----------------------
# Keep QC PASS genomes
# -----------------------

qc_pass = qc[qc["PassQC"] == True]["Assembly"]

amr = amr[amr["Assembly"].isin(qc_pass)]

print("Assemblies after QC:", amr["Assembly"].nunique())


# -----------------------
# Feature extraction
# -----------------------

feature_rows = []

assemblies = amr["Assembly"].unique()

for acc in assemblies:

    df = amr[amr["Assembly"] == acc]

    genes = df[gene_col].astype(str).str.lower().tolist()

    # mutation rows
    mut_df = df[df[subtype_col].astype(str).str.upper() == "POINT"]

    mut_genes = mut_df[gene_col].astype(str).str.lower().tolist()

    row = {
        "Assembly": acc,

        # plasmid quinolone genes
        "qnr": int(any("qnr" in g for g in genes)),

        # acetyltransferase
        "aac6": int(any("aac" in g for g in genes)),

        # efflux pumps
        "oqx": int(any("oqx" in g for g in genes)),
        "qep": int(any("qep" in g for g in genes)),

        # target mutations
        "gyrA_mut": int(any("gyra" in g for g in mut_genes)),
        "parC_mut": int(any("parc" in g for g in mut_genes)),

        # mutation count
        "mutation_count": len(mut_genes)
    }

    feature_rows.append(row)


features = pd.DataFrame(feature_rows)


# -----------------------
# Save
# -----------------------

features.to_csv("data/processed/features.csv", index=False)

print("Features saved → data/processed/features.csv")
print("Total samples:", len(features))
print(features.head())