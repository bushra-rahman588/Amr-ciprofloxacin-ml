cat > README.md << 'EOF'
# AMR Ciprofloxacin ML Pipeline

End-to-end pipeline to predict ciprofloxacin resistance using:
- phenotype MIC data (real)
- BioSample → Assembly mapping (NCBI datasets)
- genome download (NCBI datasets)
- AMR annotation (AMRFinderPlus)
- feature engineering + population-structure-aware ML evaluation

## Structure
- data/raw/phenotype: input phenotype CSV
- data/interim: downloaded genomes + AMRFinder outputs (ignored by git)
- data/processed: ML-ready features/labels (ignored by git)
- src/: reusable code
- scripts/: runnable pipeline scripts
- notebooks/: step-by-step notebooks
EOF