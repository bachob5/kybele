# kybele

KYBELE project is part of **Biodiversity, Food Security and Pathogens** (2024-SCIENCE-BFSP) of **ELIXIR** programme 2024-2028. 

The initial goal of KYBELE is to build an AI-powered, FAIR-compliant, and user-friendly system for extracting, integrating, and exploring biodiversity knowledge, by connecting genomic resources with ecological and taxonomic information. 
Currently, KYBELE focuses on a selected target group, the springtails (**Collembola class**). Importantly, once the pipeline is established it can be expanded to other taxonomic groups and ultimately serve as a reference standard for EU-based biodiversity monitoring.

The project encompasses four main activities with several tasks each. This repository regards the activity 1 entitled "Data harvesting, synthesis and FAIRification" where data related to the target organism group (Collembola), only taxa listed in Fauna Europaea for which reference DNA sequences are available in BOLD has been harvested. 
For these taxa, structured catalogues of **species names, habitats, and ecological traits** were compiled from existing accurate resources to annotate **BiodiversityPMC** with domain-specific vocabularies, ensuring **FAIR compliance**.

The repository shares specific scripts regarding the original dataset retrieval, taxonomic information extraction from **NCBI taxonomy** and **Catalogue of Life** (CoL) backbones including taxa synonyms. Sharing such material fulfill the open-science requirements ensuring code re-usability as well as the possibility to expand the pipeline to additional and wider taxonomic groups.  


**TaxoGuilds** folder contains the main scripts to retrieve the original data and the corresponding Taxonomic information from several taxonomy backbones:

- **Collembola_Bold_information_retrieval.md** workflow retrieves Collembola taxa from BOLD using several exclusion and inclusion parameters, which are detailed within the script.\
&nbsp;&nbsp;- Input data from BOLD: results/collembola_unique_n_occurence.txt
  
- **get_ColSynonyms_std.py** provides a standardized Python code to retrieve taxonomic information per taxa including taxa Synonyms from Catalogue of Life (https://www.catalogueoflife.org/) backbone.\
&nbsp;&nbsp;- See CoL output in results/collembola_unique_n_occurence_ColSynonyms.tsv

- **get_NCBISynonyms_std.py** provides a standardized Python code to retrieve taxonomic paths, TaxIDs paths and taxon synonyms per taxa from NCBI Taxonomy (https://www.ncbi.nlm.nih.gov/taxonomy) backbone.\
	this script produced three outputs in results/ folder:\
&nbsp;&nbsp;&nbsp;&nbsp;- collembola_unique_n_occurence_ncbiSynonyms.tsv: all synonyms, taxonomy paths and TaxIDs paths\
&nbsp;&nbsp;&nbsp;&nbsp;- collembola_unique_n_occurence_ncbi_ConflictingTaxonomies.tsv: conflicting taxonomies between BOLD and NCBI where at least one taxonomic rank is different\
&nbsp;&nbsp;&nbsp;&nbsp;- collembola_unique_n_occurence_ncbi_TaxaNotFound.tsv: taxa absent from NCBI taxonomy

**Catalogue of Collembola ecological traits**

The catalogue is located in the `results/` folder. It brings together taxonomic information, COI barcode sequences, ecological traits, supporting literature, and specimen metadata for European Collembola.

The catalogue version described in the accompanying documentation contains **317 species**, representing **21 families** and **97 genera**. Each row represents a taxon and links its taxonomic identity to an associated BOLD record, COI barcode sequence, and available ecological information.

**1. Taxonomy and identifiers**

| Field | Description |
|---|---|
| `species` | Scientific name of the species represented by the record. |
| `genus` | Genus to which the species belongs. |
| `family` | Family assigned to the taxon. |
| `ncbi_taxid` | NCBI Taxonomy identifier (TaxID) matched to the taxon at the lowest available taxonomic rank. |
| `taxid_matched_rank` | Taxonomic rank at which `ncbi_taxid` was matched (e.g. species, genus, or family). |
| `Bold_processid` | BOLD Process ID, a unique identifier automatically generated for a record added to a BOLD project. |
| `Bold_sampleid` | Sample identifier supplied by the collector when the specimen was submitted to BOLD. |

**2. Trophic-guild information**

| Field | Description |
|---|---|
| `trophic_guild` | Trophic-guild assignment supported by direct evidence for the target species. |
| `trophic_guild_indirect` | Trophic-guild assignment supported by indirect, qualified, or less taxonomically specific evidence. |
| `trophic_evidence_type` | Indicates the evidence type associated with the trophic-guild assignment. |
| `trophic_note` | Notes explaining the assignment, evidence, or reason for treating it as indirect. |

**3. Body-size information**

| Field | Description |
|---|---|
| `body_size_mm` | Body-size value in millimetres, where supported by direct evidence. |
| `body_size_indirect_mm` | Body-size value in millimetres retained from indirect or less specific evidence. |
| `body_size_note` | Notes about the body-size value, its source, or the reason for treating it as indirect. |

**4. Habitat information**

| Field | Description |
|---|---|
| `habitat` | Habitat assignment supported by direct evidence for the target species. |
| `habitat_indirect` | Habitat assignment based on indirect or less specific evidence. |
| `habitat_evidence_type` | Indicates the evidence type associated with the habitat assignment. |
| `habitat_note` | Notes explaining the habitat assignment, evidence, or reason for treating it as indirect. |

**5. Literature sources and QA outputs**

Fields matching the following patterns document the literature-mining and question-answering (QA) process:

| Field pattern | Description |
|---|---|
| `*_sources` | Retrieved literature sources associated with the relevant trait or extraction task. |
| `*_n_docs` | Number of documents considered for the relevant trait or extraction task. |
| `*_qa_answer` | Answer generated by the QA workflow for the relevant trait or extraction task. |

The `*` represents a trait- or task-specific prefix. These fields support traceability by recording the sources considered, the number of documents retrieved, and the QA output. The source documentation describes these field patterns but does not list every complete field name individually.

**6. BOLD specimen and collection metadata**

| Field | Description |
|---|---|
| `Bold_life_stage` | Life stage recorded for the specimen in BOLD. |
| `Bold_habitat` | Habitat information recorded in the BOLD specimen metadata. |
| `Bold_sampling_protocol` | Sampling protocol recorded for the BOLD record. |
| `Bold_country` | Country associated with the BOLD record. |
| `Bold_province` | Province or equivalent subnational location recorded in BOLD. |
| `Bold_coordinates` | Geographic coordinates associated with the BOLD record. |
| `Bold_elev` | Elevation recorded for the collection locality. |
| `Bold_collection_date` | Collection date recorded in BOLD. |
| `Bold_ecoregio` | Ecoregion metadata associated with the BOLD record. |
| `Bold_biome` | Biome metadata associated with the BOLD record. |

**7. COI barcode sequence**

| Field | Description |
|---|---|
| `Sequence` | COI barcode sequence associated with the record, provided in the 5′ → 3′ direction. |

**Evidence interpretation**

Trait assignments should be interpreted according to the distinction between direct and indirect evidence:

- **Direct evidence:** a source sentence explicitly states the trait for the target species.
- **Indirect evidence:** the evidence is qualified or uncertain, refers to a congeneric species or to Collembola more generally, or infers a trait from the collection substrate or locality.
