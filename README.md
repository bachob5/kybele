# kybele

KYBELE project is part of **Biodiversity, Food Security and Pathogens** (2024-SCIENCE-BFSP) of **ELIXIR** programme 2024-2028. 

The initial goal of KYBELE is to build an AI-powered, FAIR-compliant, and user-friendly system for extracting, integrating, and exploring biodiversity knowledge, by connecting genomic resources with ecological and taxonomic information. 
Currently, KYBELE focuses on a selected target group, namely the **springtails - Collembola class**. Importantly, once the pipeline is established it can be expanded to other taxonomic groups and ultimately serve as a reference standard for EU-based biodiversity monitoring.

The project encompasses four main activities with several tasks each. This repository regards the activity 1 entitled "Data harvesting, synthesis and FAIRification" where data related to the target organism group (Collembola), only taxa listed in Fauna Europaea for which reference DNA sequences are available in BOLD has been harvested. 
For these taxa, structured catalogues of **species names, habitats, and ecological traits** were compiled from existing accurate resources to annotate **BiodiversityPMC** with domain-specific vocabularies, ensuring **FAIR compliance**.

The repositary shares specific scripts regarding the original dataset retrieval, taxonomic information extraction from **NCBI taxonomy** and **Catalogue of Life** (CoL) backbones including taxa synonyms. Sharing such material fulfill the open-science requirements ensuring code re-usability as well as the possibility to expand the pipeline to additional and wider taxonomic groups.  


**TaxoGuilds** folder contains the main scripts to retrieve the original data and the corresponding Taxonomic information from several taxonomy backbones:

- **Collembola_Bold_information_retrieval.md** workflow retrieves Collembola taxa from BOLD using several exclusion and inclusion parameters, which are detailed within the script.\
<p>Input data from BOLD: results/collembola_unique_n_occurence.txt
- **get_ColSynonyms_std.py** provides a standardized Python code to retrieve taxonomic information per taxa including taxa Synonyms from Catalogue of Life (https://www.catalogueoflife.org/) backbone.\
       See CoL output in results/collembola_unique_n_occurence_ColSynonyms.tsv
- **get_NCBISynonyms_std.py** provides a standardized Python code to retrieve taxonomic paths, TaxIDs paths and taxon synonyms per taxa from NCBI Taxonomy (https://www.ncbi.nlm.nih.gov/taxonomy) backbone.\
       this script produced three outputs in results/ folder:\
          - collembola_unique_n_occurence_ncbiSynonyms.tsv: all synonyms, taxonomy paths and TaxIDs paths\
          - collembola_unique_n_occurence_ncbi_ConflictingTaxonomies.tsv: conflicting taxonomies between BOLD and NCBI where at least one taxonomic rank is different\
          - collembola_unique_n_occurence_ncbi_TaxaNotFound.tsv: taxa absent from NCBI taxonomy
