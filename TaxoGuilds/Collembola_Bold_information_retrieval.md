## Load BOLDconnectR package for interfacing with BOLD database
Allows retrieval, transformation and analysis of the Barcode of Life Data systems data
``` r
library(BOLDconnectR)
```


## Retrieve all public records associated with the taxon Collembola


- This function returns only the process IDs and associated marker codes (marker_code) for each record
- These identifiers will be used to fetch the full dataset including taxonomy, metadata, and DNA sequences


``` r
seq.data.ids <- bold.public.search(taxonomy = list("Collembola"))
```

## Set personal BOLD API key to enable authenticated requests


- The API key is stored in the .Renviron file and retrieved here as an environment variable
- Improves stability, increases allowable request volume, and ensures traceable access


``` r
bold.apikey(Sys.getenv("BOLD_APIKEY"))
```

## Download full records from BOLD using the process IDs obtained

**Parameters:**

- `get_by = "processid"`: Retrieve records using unique process identifiers
- `identifiers = seq.data.ids$processid`
- `cols = NULL`: Retrieve all available metadata and sequences
- `export = "~/Desktop/collembola.tsv"`
- `na.rm = FALSE`: Retain records with missing values
- `filt_geography = c(...)`: Restrict dataset to selected European countries
- `filt_marker = "COI-5P"`: Select COI-5P sequences only


``` r
bold.fetch(
  get_by = "processid",
  identifiers = seq.data.ids$processid,
  cols = NULL,
  export = "~/Desktop/collembola.tsv",
  na.rm = FALSE,
  filt_geography = c(
    "Italy","France","Germany","Spain","Portugal","United Kingdom",
    "Ireland","Netherlands","Belgium","Luxembourg","Switzerland",
    "Austria","Poland","Czech Republic","Slovakia","Hungary",
    "Slovenia","Croatia","Bosnia and Herzegovina","Serbia",
    "Montenegro","Albania","North Macedonia","Greece","Bulgaria",
    "Romania","Moldova","Ukraine","Belarus","Lithuania","Latvia",
    "Estonia","Denmark","Norway","Sweden","Finland","Iceland",
    "Malta","Cyprus"
  ),
  filt_marker = "COI-5P"
)
```

## Import the exported TSV file into R as a data frame
read.delim reads tab-delimited files; header = TRUE ensures first row is interpreted as column names


``` r
collembola <- read.delim("collembola.tsv", header = TRUE)
```

## Load dplyr package for column selection and data manipulation


``` r
library(dplyr)
```

## Remove columns not relevant for downstream analyses


``` r
collembola <- collembola %>% select(
  -insdc_acs, -specimenid, -taxid, -short_note, -identification_method,
  -museumid, -fieldid, -collection_code, -processid_minted_date, -inst,
  -funding_src, -reproduction, -collectors, -site_code, -specimen_linkout,
  -collection_event_id, -tissue_type, -collection_time, -associated_taxa,
  -associated_specimens, -voucher_type, -taxonomy_notes, -collection_notes,
  -identification, -identification_rank, -species_reference, -identified_by,
  -sequence_run_site, -sequence_upload_date, -bin_uri, -bin_created_date,
  -depth, -coord_accuracy, -elev_accuracy, -depth_accuracy,
  -bold_recordset_code_arr, -collection_date_end
)
```

## Remove entries without at least genus-level identification


``` r
collembola_no_genus <- collembola[!is.na(collembola$genus), ]
```

## Remove entries with missing species only when other species exist within the same genus


- If the genus contains at least one fully identified species, entries with NA in the species column are removed
- If the genus contains only entries with NA species, the genus-level record is retained
- This ensures that genus-level identifications are preserved only when no more specific species-level identifications exist


``` r
collembola_no_genus$genus_only <- is.na(collembola_no_genus$species)

collembola_step1 <- do.call(rbind, lapply(
  split(collembola_no_genus, collembola_no_genus$genus),
  function(df) {
    if(any(!df$genus_only)) df[!df$genus_only, ] else df
  }
))
```

## Apply the same filtering logic to entries labeled as "sp." or uncertain species annotations (e.g., sp.xx)


- Entries with such labels are treated as genus-level identifications
- Within each genus, these entries are removed if any fully identified species exists
- If no fully identified species exist for the genus, the "sp." entry is retained


``` r
collembola_step1$sp_only <- grepl("\\bsp\\.?\\b", collembola_step1$species)

collembola_step2 <- do.call(rbind, lapply(
  split(collembola_step1, collembola_step1$genus),
  function(df) {
    if(any(!df$sp_only)) df[!df$sp_only, ] else df
  }
))
```

## Remove uncertain annotations (cf., aff., nr.)


``` r
collembola_step3 <- collembola_step2[!grepl("cf\\.|aff\\.|nr\\.", collembola_step2$species), ]
```

## Standardize species names: convert "sp.xx" to "sp." and remove stage identifiers (L1, L2, ...)


``` r
collembola_step3$species <- sub("(\\bsp\\.).*", "sp.", collembola_step3$species)
collembola_step3$species <- gsub(" L[0-9]+", "", collembola_step3$species)
```

## Remove temporary columns used for filtering


``` r
collembola_step3 <- collembola_step3 %>% select(-genus_only, -sp_only)
```

## Remove entries without DNA sequence


``` r
collembola_step3 <- collembola_step3[
  !is.na(collembola_step3$nuc) & nchar(trimws(collembola_step3$nuc)) > 0,
]
```

## Standardise species names 
Species names are trimmed to remove leading and trailing whitespace

``` r
collembola_data <- collembola_step3 %>%
  mutate(species = trimws(as.character(species)))
```

## Split geographic coordinates 
Coordinates are separated into latitude and longitude


``` r
coord_parts <- strsplit(
  ifelse(
    is.na(collembola_data$coord),
    "",
    as.character(collembola_data$coord)
  ),
  ",",
  fixed = TRUE
)
```
## Extract latitude 
The first coordinate value is converted to numeric; invalid values are assigned NA

``` r
latitude <- vapply(coord_parts, function(x) {
  if (length(x) != 2) return(NA_real_)
  suppressWarnings(as.numeric(trimws(x[1])))
}, numeric(1))
```

## Extract longitude 
The first coordinate value is converted to numeric; invalid values are assigned NA


``` r
longitude <- vapply(coord_parts, function(x) {
  if (length(x) != 2) return(NA_real_)
  suppressWarnings(as.numeric(trimws(x[2])))
}, numeric(1))
```

## Validate coordinates 
Coordinates are checked against the valid geographic ranges for latitude and longitude


``` r
valid_coordinates <-
  is.finite(latitude) &
  is.finite(longitude) &
  latitude >= -90 & latitude <= 90 &
  longitude >= -180 & longitude <= 180
```

## Select one record per species
Records are ranked by coordinate validity, sequence length, locality information

``` r
collembola_unique <- collembola_data %>%
  mutate(
    # Indicate whether geographic coordinates pass the validity checks.
    has_coordinates = valid_coordinates,

    # Read nuc_basecount as a numeric sequence length in base pairs.
    sequence_length = suppressWarnings(
      as.numeric(as.character(nuc_basecount))
    ),

    # Indicate whether at least one locality field is populated.
    has_locality =
      (!is.na(site) & trimws(as.character(site)) != "") |
      (!is.na(province.state) &
         trimws(as.character(province.state)) != "")
  ) %>%

  # Rank records within each species according to the following
  # priorities, from highest to lowest:
  # 1. Valid geographic coordinates.
  # 2. Greater sequence length.
  # 3. Available locality information.
  # 4. PROCESSID in ascending order as the final tie-breaker.
  arrange(
    species,
    desc(has_coordinates),
    desc(sequence_length),
    desc(has_locality)
  ) %>%

  # Retain the highest-ranked record for each species.
  group_by(species) %>%
  slice(1) %>%
  ungroup() %>%

  # Remove temporary variables used for record ranking.
  select(-sequence_length, -has_coordinates, -has_locality)
```

## Export cleaned dataset to TSV

``` r
write.table(
  collembola_unique,
  file = "collembola_official.tsv",
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)
```

