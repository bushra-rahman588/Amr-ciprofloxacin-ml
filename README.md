
# Predicting Ciprofloxacin Resistance from Bacterial Genomic Biomarkers
 

Antimicrobial resistance has become one of the major challenges in infectious disease research. **Fluoroquinolones** such as *ciprofloxacin* are widely used antibiotics, but resistance against them is increasingly observed in bacterial populations. Understanding the genomic factors that contribute to this resistance is important for surveillance and for studying how resistance evolves.

This project was developed to explore how **bacterial genomic information*** can be used to **predict** *ciprofloxacin resistance phenotypes* The goal was not only to build a predictive model but also to examine which genomic features are most strongly associated with resistance. By combining genomic feature extraction, machine learning, and mutation-level analysis, the pipeline aims to provide a structured way to study resistance-associated genomic patterns.

## Overview of the Pipeline
The workflow starts from curated antimicrobial susceptibility testing(AST) phenotype data and progresses through resistance gene detection, feature engineering, and machine learning analysis. Each stage of the pipeline is implemented as an individual script so that the entire analysis can be reproduced step by step.
The main stages of the pipeline are summarised below.

### 1. Phenotype Curation and Biosample to Assembly Mapping
```bash
scripts/01_biosample_to_assembly.py
```

Phenotypic resistance information was manually curated from NCBI **antimicrobial susceptibility testing (AST)** metadata associated with biosample records.
Biosample identifiers were then mapped to their corresponding genome assemblies so that resistance phenotypes could be linked with genomic sequences.
This step produces the metadata table used for downstream genome download and analysis.

### 2. Genome Download
```bash
scripts/02_download_genomes.py
```

Genome assemblies are downloaded based on the mapped assembly accessions. These genomes serve as the starting point for all downstream analyses.
### 3. AMR Gene Detection
```bash
scripts/03_run_amrfinder.py
```
AMRFinderPlus is used to screen each genome for antimicrobial resistance genes and known resistance mutations.
This step identifies:
plasmid-mediated quinolone resistance genes
mutations in quinolone resistance-determining regions (QRDR)

### 4. Quality Control and Data Integration
```bash
scripts/04_qc_and_merge_amr.py
```
The AMR detection results are merged with genome metadata and phenotype labels. Genomes with incomplete or inconsistent information are filtered out before further analysis.

### 5. Feature Construction
```bash
scripts/05_build_features.py
```

Genomic information is converted into structured features suitable for machine learning.
Examples of features include:
presence of qnr genes
aac(6')-Ib-cr
oqx and qep efflux genes
  mutation indicators for gyrA and parC
  genome assembly statistics

### 6. Dataset Creation
```bash
scripts/06_create_dataset.py
```

All engineered genomic features are combined with phenotype labels to produce the final machine learning dataset.

Output dataset:
data/processed/ml_dataset_advanced.csv


### 7. Feature Engineering and Population-aware Machine Learning
```bash
Feature upgrades
```

scripts/07a_upgrade_features.py

Additional summary features are created, including:
mutation_count
total AMR genes
quinolone resistance gene counts

Population-aware ML model(7b)


```bash
scripts/07b_population_ml.py
```
A Random Forest classifier is trained to predict ciprofloxacin resistance.
To reduce bias caused by closely related genomes, evaluation is performed using GroupKFold cross-validation, in which genomes within the same similarity cluster are kept in the same fold.

### 8. Model Interpretation
```bash
scripts/08_interpretability.py
```
Feature importance analysis is performed to identify which genomic variables contribute most strongly to resistance prediction.

### 9. SHAP Analysis
```bash
scripts/09_shap_analysis.py
```
SHAP values quantify the contribution of individual features to model predictions. This helps explain why the model classifies a genome as resistant or susceptible.

### 10. Model Performance Metrics
```bash
scripts/10_results_metrics.py
```
Evaluation results from cross-validation are summarised and stored in the metrics directory. Performance statistics such as AUROC and confusion matrices are generated.

### 11. Variant Evolution Analysis
```bash
scripts/11_variant_evolution_analysis.py
```

* This step examines mutation patterns in the quinolone resistance-determining region.

* Mutation frequencies are calculated and visualised to identify common substitutions across genomes.

* Frequent mutations observed include variants at:

* **gyrA position 83**

* **gyrA position 87**

* **parC position 80**

* These positions are known to play a role in fluoroquinolone resistance.


### Key Genomic Features Used

The model incorporates a range of genomic biomarkers:

* QRDR mutations in gyrA and parC
* Plasmid-mediated quinolone resistance genes
* Total AMR gene count
* Quinolone gene counts
* Mutation accumulation features
* Genome assembly statistics



## Biological Interpretation

* The analysis highlights the importance of genomic variation within the quinolone resistance-determining region (QRDR) in shaping ciprofloxacin resistance phenotypes. Mutations detected in the gyrA and parC genes appear consistently across resistant isolates and emerge as strong predictors during the machine learning analysis.<br><br>
* In particular, substitutions at conserved QRDR positions such as gyrA S83, gyrA D87, and parC S80 were frequently observed in the dataset. These mutations are known to alter the interaction between fluoroquinolone antibiotics and the bacterial type II topoisomerases DNA gyrase and topoisomerase IV. Changes at these residues reduce the binding affinity of ciprofloxacin, thereby decreasing drug susceptibility.<br><br>
* Another notable observation is the relationship between mutation accumulation and resistance prediction. Genomes carrying multiple QRDR mutations tend to have higher predicted resistance probabilities compared to genomes with fewer or no mutations. This pattern is consistent with the well-established evolutionary pathway of fluoroquinolone resistance, where sequential mutations in target genes progressively increase resistance levels.<br><br>
* Interpretability analysis further supports these findings. Features related to mutation count, gyrA mutations, and parC mutations showed strong contributions to model predictions, indicating that the model captures biologically meaningful signals rather than relying on unrelated genomic properties. Plasmid-mediated quinolone resistance genes such as qnr, oqx, and qep were detected in some isolates but generally contributed less to prediction compared to chromosomal QRDR mutations. <br><br>
* Overall, the genomic features identified by the model align with established mechanisms of ciprofloxacin resistance in Escherichia coli, supporting the biological relevance of the predictive framework.



## Conclusion



* This project presents a **reproducible pipeline** that integrates curated **antimicrobial susceptibility testing (AST)** data with **bacterial genome assemblies** to investigate genomic determinants of **ciprofloxacin resistance**. <br><br>
* The workflow combines **genome retrieval, resistance gene detection, mutation profiling, feature engineering**, and **machine learning analysis** into a single computational framework. **Population-aware** ***cross-validation*** was used to minimise potential bias caused by closely related genomes, ensuring that the model evaluation reflects true predictive ability. <br><br>
* The results demonstrate that **genomic biomarkers**, particularly **QRDR** mutations in ***gyrA*** and ***parC***, provide strong signals for predicting ciprofloxacin resistance phenotypes. Mutation accumulation patterns further reinforce the evolutionary nature of resistance development. <br><br>
* Beyond predictive modelling, the pipeline provides a structured approach for exploring how genomic variation contributes to antimicrobial resistance. By integrating mutation-level analysis with machine learning interpretation, the framework offers insights into the genomic signals underlying resistance phenotypes. The workflow can potentially be extended to other antibiotics or larger genomic datasets to further investigate antimicrobial resistance mechanisms. 


