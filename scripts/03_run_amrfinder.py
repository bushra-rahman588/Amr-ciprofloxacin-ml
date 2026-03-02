import subprocess
from pathlib import Path

print("STEP 3 — RUNNING AMRFINDER WITH MUTATION DETECTION")


genome_dir = Path("data/interim/genomes")
output_dir = Path("data/interim/amrfinder")

output_dir.mkdir(parents=True, exist_ok=True)


genomes = list(genome_dir.glob("*.fna"))

print("Genomes found:", len(genomes))


success = 0
failed = 0


for genome in genomes:

    assembly = genome.stem
    out_file = output_dir / f"{assembly}.tsv"

    cmd = [
        "amrfinder",
        "-n", str(genome),
        "--organism", "Escherichia",
        "-o", str(out_file)
    ]

    try:
        subprocess.run(cmd, check=True)
        success += 1

    except subprocess.CalledProcessError:
        print("Failed:", assembly)
        failed += 1


print("\nDONE")
print("TSV outputs:", success)
print("Failed genomes:", failed)
