# Import libraries
library(dplyr)
library(reticulate)
library(tidyr)

# Declare global variables
BASE_DIR <- "E:/THIENDHB_GOOGLEDRIVE/MASTER TILBURG/THESIS/"
INPUT_DIR <- paste0(BASE_DIR, "DATASET/INPUT/")
OUTPUT_DIR <- paste0(BASE_DIR, "DATASET/OUTPUT/")
OUTPUT_DIR
SEED <- 6886

# import numpy and specify no automatic Python to R conversion
np <- import("numpy", convert = FALSE)

# Read numpy format to r dataframe
emb_file_name <- paste0(OUTPUT_DIR, "skill_long_embeddings_with_ids.npy")
embeddings_npy <- np$load(emb_file_name)

embeddings_matrix <- py_to_r(embeddings_npy)
skill_long_embeddings <- as.data.frame(embeddings_matrix)

# Set tmp df to Null to release memory
emb_file_name <- NULL
embeddings_npy <- NULL
embeddings_matrix <- NULL

# Read file to obtain job_id and types
df <- read.csv(paste0(OUTPUT_DIR, 'clean_skill_db.csv'), stringsAsFactors = F)
job_type <- df$type
skill_ids <- df$skill_id

# Create new column names
desc_cols <- paste0('desc_', 0:299)
req_cols <- paste0('req_', 0:299)
qual_cols <- paste0('qual_', 0:299)
new_cols <- c(desc_cols, req_cols, qual_cols)
old_cols <- paste0('V', 2:301)

tmp_embeddings <- skill_long_embeddings %>%
  mutate(type = job_type, skill_id = skill_ids)
#   group_by(V1) %>%
#   mutate(rownum = 1:n()) %>%
#   ungroup()
#
tmp_embeddings <- tmp_embeddings %>%
#   mutate(col_name = paste0(job_type, '_', rownum)) %>%
#   select(-rownum) %>%
  select(skill_id, job_id = V1, type, everything())

tmp2 <- pivot_wider(data = tmp_embeddings, id_cols = job_id, names_from = type, values_from = old_cols)

