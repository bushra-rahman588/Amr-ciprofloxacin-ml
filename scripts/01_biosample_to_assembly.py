import subprocess
import pandas as pd
import yaml
from pathlib import Path
from tqdm import tqdm


def get_assembly_from_biosample(biosample):
    """
    Map BioSample to Assembly using NCBI Entrez
    """

    try:
        cmd = f'esearch -db assembly -query {biosample} | esummary | xtract -pattern DocumentSummary -element AssemblyAccession'
        out = subprocess.check_output(cmd, shell=True, text=True).strip()

        if out:
            return out.split("\n")[0]

    except subprocess.CalledProcessError:
        return None

    return None


# Load config
cfg = yaml.safe_load(open("configs/config.yaml"))

df = pd.read_csv(cfg["phenotype_csv"])

biosamples = (
    df[cfg["biosample_col"]]
    .dropna()
    .astype(str)
    .unique()
)

print("Total BioSamples:", len(biosamples))


rows = []

for bs in tqdm(biosamples, desc="Mapping BioSample → Assembly"):

    acc = get_assembly_from_biosample(bs)

    if acc:
        rows.append([bs, acc])


map_df = pd.DataFrame(rows, columns=[cfg["biosample_col"], "Assembly"])

out_file = Path(cfg["mapping_out"])
out_file.parent.mkdir(parents=True, exist_ok=True)

map_df.to_csv(out_file, index=False)

print("\nMapping complete")
print("Mapped:", len(map_df))
print("Unique assemblies:", map_df["Assembly"].nunique())