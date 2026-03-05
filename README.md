
# Predicting Ciprofloxacin Resistance from Bacterial Genomic Biomarkers
 

Antimicrobial resistance has become one of the major challenges in infectious disease research. **Fluoroquinolones** such as *ciprofloxacin* are widely used antibiotics, but resistance against them is increasingly observed in bacterial populations.

Understanding the genomic determinants of antibiotic resistance is essential for:
* Surveillance of resistant strains
* Studying the evolutionary pathways of resistance
* Developing predictive models linking genotype to phenotype

This project investigates whether **bacterial genomic features can be used to predict ciprofloxacin resistance phenotypes in Escherichia coli** using a reproducible computational framework.

The study integrates **genomic biomarker extraction, mutation profiling, and machine learning** to identify genomic signals associated with resistance and evaluate their predictive power.

## Biological Interpretation

The analysis highlights the importance of genomic variation within the quinolone resistance-determining region (QRDR) in shaping ciprofloxacin resistance phenotypes.<br><br>
Mutations detected in the gyrA and parC genes appear consistently across resistant isolates and emerge as strong predictors during the machine learning analysis.<br><br>

Particularly frequent substitutions were observed at:
* gyrA S83
* gyrA D87
* parC S80

These residues are located within the QRDR of bacterial type II topoisomerases (DNA gyrase and topoisomerase IV), the primary molecular targets of fluoroquinolone antibiotics. Mutations at these positions reduce drug binding affinity and therefore decrease ciprofloxacin susceptibility.

* Another notable observation is the relationship between mutation accumulation and resistance prediction. Genomes carrying multiple QRDR mutations tend to have higher predicted resistance probabilities compared to genomes with fewer or no mutations, ***(as seen in the graph below)***. This pattern is consistent with the well-established evolutionary pathway of fluoroquinolone resistance, where sequential mutations in target genes progressively increase resistance levels.<br><br> 

![Alt text](https://github.com/bushra-rahman588/Amr-ciprofloxacin-ml/blob/main/results/figures/qrdr_vs_resistance.png)<br><br>

* Interpretability analysis further supports these findings. Features related to mutation count, gyrA mutations, and parC mutations showed strong contributions to model predictions, indicating that the model captures biologically meaningful signals rather than relying on unrelated genomic properties ***(as seen in the graph below)***. Plasmid-mediated quinolone resistance genes such as qnr, oqx, and qep were detected in some isolates but generally contributed less to prediction compared to chromosomal QRDR mutations. <br><br>

![Alt text](https://github.com/bushra-rahman588/Amr-ciprofloxacin-ml/blob/main/results/figures/shap_summary.png) <br><br>

* Overall, the genomic features identified by the model align with established mechanisms of ciprofloxacin resistance in Escherichia coli, supporting the biological relevance of the predictive framework.

#### Graph showing genes were mutation appears among resistant isolates showing frequent substitution at **gyrA S83** **gyrA D87** **parC S80**
![Alt text](https://github.com/bushra-rahman588/Amr-ciprofloxacin-ml/blob/main/results/figures/qrdr_individual_frequency.png)

## Dataset Description

This study integrates genomic data and antimicrobial susceptibility testing (AST) phenotypes to investigate genomic determinants of ciprofloxacin resistance.

### Species

Escherichia coli

### Antibiotic

Ciprofloxacin (fluoroquinolone class)

### Phenotype Data Source

Phenotypic resistance data were curated from NCBI BioSample antimicrobial susceptibility testing (AST) metadata.

### The phenotype dataset includes isolates annotated as:

* Resistant
* Susceptible

based on ciprofloxacin susceptibility testing.

### Genomic Data

Genome assemblies corresponding to BioSample records were retrieved from the NCBI Assembly database.

Each genome is associated with:

* Assembly accession
* BioSample identifier
* Ciprofloxacin phenotype label


## Overview of the Computational Pipeline
The pipeline links phenotypic antimicrobial susceptibility data with bacterial genome assemblies and transforms genomic information into machine learning model for resistance prediction.

```bash
AST Phenotype Data
        │
        ▼
BioSample → Genome Assembly Mapping
        │
        ▼
Genome Download
        │
        ▼
AMR Gene Detection (AMRFinderPlus)
        │
        ▼
Mutation Profiling (QRDR regions)
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning Dataset Creation
        │
        ▼
Population-aware ML Model (Random Forest)
        │
        ▼
Model Evaluation & Interpretation
        │
        ▼
Mutation Evolution Analysis
```

Each stage is implemented as a standalone script to ensure reproducibility and transparency.

### 1. Phenotype curation and genome mapping
```bash
scripts/01_biosample_to_assembly.py
```
Curated antimicrobial susceptibility testing (AST) phenotypes from NCBI BioSample metadata and linked them to corresponding genome assemblies.

### 2. Genome retrieval
```bash
scripts/02_download_genomes.py
```
Automatically downloaded bacterial genome assemblies based on mapped accession identifiers.

### 3. Resistance gene detection
```bash
scripts/03_run_amrfinder.py
```
Screened genomes using AMRFinderPlus to detect:
* Plasmid-mediated quinolone resistance genes
* Mutations in QRDR regions

### 4. Quality control and metadata integration
```bash
scripts/04_qc_and_merge_amr.py
```
Filtered incomplete records and merged resistance detection outputs with phenotype metadata.

### 5. Genomic feature construction
```bash
scripts/05_build_features.py
```

Engineered structured genomic biomarkers including:

* QRDR mutation indicators (gyrA, parC)
* Plasmid-mediated resistance genes
* Mutation accumulation features
* Genome assembly statistics

### 6. Dataset generation
```bash
scripts/06_create_dataset.py
```

Combined genomic features with resistance phenotypes to create the final machine learning dataset.

**Output dataset:**
```bash
data/processed/ml_dataset_advanced.csv
```


### 7. Feature Engineering
```bash
scripts/07a_upgrade_features.py
```

Additional summary features are created, including:
* Mutation_count
* Total AMR genes
* Quinolone resistance gene counts

## Population-aware ML model(7b)

```bash
scripts/07b_population_ml.py
```

A **Random Forest classifier** was trained to predict ciprofloxacin resistance from genomic biomarkers.

To avoid overestimating model performance due to closely related genomes, a **population-aware validation strategy** was implemented:

* Genome similarity clusters were generated using Mash
* **GroupKFold cross-validation** ensured genomes within the same cluster remained in the same fold

This approach reduces phylogenetic bias and provides a more realistic estimate of predictive performance.




## 8. Model Interpretation
```bash
scripts/08_interpretability.py
```
Feature importance analysis was performed to identify genomic determinants contributing to resistance prediction.

Interpretability analysis revealed that the strongest predictors included:

* gyrA mutations
* parC mutations
* mutation count features

SHAP analysis was used to quantify the contribution of each genomic feature to model predictions, allowing interpretation at both the global and individual genome level***(as seen in the graph below)***.

![Alt text](https://github.com/bushra-rahman588/Amr-ciprofloxacin-ml/blob/main/results/figures/shap_importance.png)

```bash
scripts/09_shap_analysis.py
```


### 10. Model Performance Metrics
```bash
scripts/10_results_metrics.py
```
Evaluation results from cross-validation are summarised and stored in the metrics directory. Performance statistics such as AUROC and confusion matrices are generated.

**Below is the graph showing ROC curve for the classifier.**
![Alt text](https://github.com/bushra-rahman588/Amr-ciprofloxacin-ml/blob/main/results/metrics/roc_curve_final.png)

## 11. Variant Evolution Analysis
```bash
scripts/11_variant_evolution_analysis.py
```

Mutation patterns within QRDR regions were analysed to investigate evolutionary trends.

Frequent substitutions were observed at:

* **gyrA position 83**
* **gyrA position 87**
* **parC position 80**

These mutations represent key evolutionary steps in the development of ciprofloxacin resistance.


## Key Genomic Features Used

The model incorporates a range of genomic biomarkers:

* QRDR mutations in gyrA and parC
* Plasmid-mediated quinolone resistance genes
* Total AMR gene count
* Quinolone gene counts
* Mutation accumulation features
* Genome assembly statistics

## Conclusion
* This project presents a **reproducible pipeline** that integrates curated **antimicrobial susceptibility testing (AST)** data with **bacterial genome assemblies** to investigate genomic determinants of **ciprofloxacin resistance**. <br><br>
* By integrating **phenotypic antimicrobial susceptibility data, bacterial genomes, resistance gene detection**, and **machine learning**, the workflow demonstrates how genomic biomarkers can be used to predict resistance phenotypes. <br><br>
* The results confirm that **QRDR mutations** in **gyrA** and **parC** are dominant signals driving ciprofloxacin resistance prediction. <br><br>
* Beyond prediction, the pipeline provides a structured framework for exploring genotype–phenotype relationships in antimicrobial resistance. The workflow can be extended to **other antibiotics**,**additional bacterial species** and **larger genomic surveillance datasets**. Such approaches may contribute to genomic surveillance and predictive modelling of antimicrobial resistance evolution.

## Operating System

Tested on:
```bash
Linux (Ubuntu 20.04+)
```
The pipeline may also run on macOS environments with compatible dependencies.

## Citation

If you use this pipeline, please cite:

Rahman B. Amr-ciprofloxacin-ml: Predicting Ciprofloxacin Resistance from Bacterial Genomic Biomarkers.
GitHub, 2026.


