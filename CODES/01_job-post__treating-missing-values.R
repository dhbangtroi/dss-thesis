###############################################
## Code: 01_job-post__treating-missing-values
## Purpose: Treating missing data
## Author: Thien Dao
## Creation date: 2021-04-09
## Update date: 2021-04-22
###############################################

########################
# Loading libraries
########################

library(dplyr)
library(stringr)
library(DT)
library(naniar)
library(ggplot2)

########################
# Importing raw data
########################

base_path <- "E:\\THIENDHB_GOOGLEDRIVE\\MASTER TILBURG\\THESIS\\DATASET\\INPUT"
df <- read.csv(file.path(base_path, "online-job-postings.csv"))
df <- df %>% mutate(job_id = 1:n())
refined_df <- df

########################
# Functions
########################

# Helper function to detect missing values
detect_na <- function(x) {
  is.na(x) | x == "NA" | x == "N/A" | x == "na" | x == "NaN" | x == ""
}

########################
# Visualizing missing data
########################

# Detect and convert all considered "missing" values to NA
refined_df[detect_na(refined_df)] <- NA

# Visualize missing data
vis_miss(refined_df[c('Title', 'JobDescription', 'JobRequirment', 'RequiredQual')]) +
  labs(title = "Row-wise missingness of Online Job Posts data")

try(gg_miss_upset(refined_df[c('Title', 'JobDescription', 'JobRequirment', 'RequiredQual')],
              matrix.color = "#ff9800", main.bar.color = "#900c3f", sets.bar.color = "#009933",
              empty.intersections = T, set_size.show = T),
    silent = T
)

########################
# Treating missing data
# Method:
# - Find corresponding section in column jobpost
# - Extract that section into new section column
# - Only treat sections of Job title, description, requirement, and qualification required
########################

# Dealing with missing job title
#==============================================

titles <- refined_df %>% filter(is.na(Title))

start_str <- str_locate(titles$jobpost, '(?<=TITLE:)')[,1]
end_str <- str_locate(str_sub(titles$jobpost, start=start_str), '\n[A-Z/\\ ]{1,}:')[,1] + start_str - 2
end_str <- ifelse(!is.na(start_str) & is.na(end_str), str_length(job_desc$jobpost), end_str)

extract_title <- str_trim(str_sub(titles$jobpost, start_str, end_str))
titles <- titles %>%
  mutate(new_title = extract_title)
datatable(titles[c('jobpost', 'Title', 'new_title')], escape=T)

refined_df <- left_join(refined_df, select(titles, job_id, new_title), by = "job_id")
refined_df <- refined_df %>%
  mutate(Title = case_when(!is.na(new_title) ~ new_title, TRUE ~ Title))

# Dealing with missing job description
#==============================================

job_desc <- refined_df %>% filter(is.na(JobDescription))

start_str <- str_locate(job_desc$jobpost, '(?<=DESCRIPTION:|NEWS DETAILS:)')[,1]
end_str <- str_locate(str_sub(job_desc$jobpost, start=start_str), '\n[A-Z/\\ ]{1,}:')[,1] + start_str - 2
end_str <- ifelse(!is.na(start_str) & is.na(end_str), str_length(job_desc$jobpost), end_str)

extract_desc <- str_trim(str_sub(job_desc$jobpost, start_str, end_str))
job_desc <- job_desc %>%
  mutate(new_desc = extract_desc, start_desc = start_str, end_desc = end_str)
# datatable(job_desc[c('jobpost', 'JobDescription', 'new_desc', 'start_desc', 'end_desc

refined_df <- left_join(refined_df, select(job_desc, job_id, new_desc), by = "job_id")
refined_df <- refined_df %>%
  mutate(JobDescription = case_when(!is.na(new_desc) ~ new_desc, TRUE ~ JobDescription))

# Dealing with missing job requirement
#==============================================

job_req <- refined_df %>% filter(is.na(JobRequirment))

start_str <- str_locate(job_req$jobpost, '(?<=RESPONSIBILITIES:)')[,1]
end_str <- str_locate(str_sub(job_req$jobpost, start=start_str), '\n[A-Z/\\ ]{1,}:')[,1] + start_str - 2
end_str <- ifelse(!is.na(start_str) & is.na(end_str), str_length(job_req$jobpost), end_str)

extract_req <- str_trim(str_sub(job_req$jobpost, start_str, end_str))
job_req <- job_req %>%
  mutate(new_req = extract_req)
refined_df <- left_join(refined_df, select(job_req, job_id, new_req), by = "job_id")
refined_df <- refined_df %>%
  mutate(JobRequirment = case_when(!is.na(new_req) ~ new_req, TRUE ~ JobRequirment))

# Dealing with missing required qualification
#==============================================

job_qual <- refined_df %>% filter(is.na(RequiredQual))

start_str <- str_locate(job_qual$jobpost, '(?<=QUALIFICATIONS:)')[,1]
end_str <- str_locate(str_sub(job_qual$jobpost, start=start_str), '\n[A-Z/\\ ]{1,}:')[,1] + start_str - 2
end_str <- ifelse(!is.na(start_str) & is.na(end_str), str_length(job_qual$jobpost), end_str)

extract_qual <- str_trim(str_sub(job_qual$jobpost, start_str, end_str))
job_qual <- job_qual %>%
  mutate(new_qual = extract_qual)
refined_df <- left_join(refined_df, select(job_qual, job_id, new_qual), by = "job_id")
refined_df <- refined_df %>%
  mutate(RequiredQual = case_when(!is.na(new_qual) ~ new_qual, TRUE ~ RequiredQual))

########################
# Visualizing after-retrieval missing data
########################

vis_miss(refined_df[c('Title', 'JobDescription', 'JobRequirment', 'RequiredQual')]) +
  labs(title = "Row-wise missingness of Retrieval Online Job Posts data")

try(gg_miss_upset(refined_df[c('Title', 'JobDescription', 'JobRequirment', 'RequiredQual')],
                  matrix.color = "#ff9800", main.bar.color = "#900c3f", sets.bar.color = "#009933",
                  empty.intersections = T, set_size.show = T),
    silent = T
)

########################
# Remove useless rows
# (missing all description, requirement, and qualification)
########################

# tmp_df <- refined_df %>%
#   filter(check_na(Title) & check_na(JobDescription) & check_na(JobRequirment) & check_na(RequiredQual))
#
# tmp_df2 <- refined_df %>%
#   filter(check_na(Title) | check_na(JobDescription) | check_na(JobRequirment) | check_na(RequiredQual))
#
# tmp_df3 <- refined_df %>%
#   filter(check_na(JobDescription) & check_na(JobRequirment) & check_na(RequiredQual))

# View(tmp_df3[c('job_id','jobpost', 'Title', 'new_title', 'JobDescription', 'new_desc', 'JobRequirment', 'new_req', 'RequiredQual', 'new_qual')])

new_df <- refined_df %>%
  filter(!(is.na(JobDescription) & is.na(JobRequirment) & is.na(RequiredQual)))

########################
# Replace missing values "NA" by "Unprovided"
########################

new_df[is.na(new_df)] <- "Unprovided"

########################
# Visualizing after-replacement missing data
########################

vis_miss(new_df[c('Title', 'JobDescription', 'JobRequirment', 'RequiredQual')]) +
  labs(title = "Row-wise missingness of Refined Online Job Posts data")

try(
  gg_miss_upset(new_df[c('Title', 'JobDescription', 'JobRequirment', 'RequiredQual')],
                matrix.color = "#ff9800", main.bar.color = "#900c3f", sets.bar.color = "#009933",
                empty.intersections = T, set_size.show = T),
  silent = T
)

########################
# Keep and rename potential useful columns
########################

new_df<- new_df %>%
  select(job_id,
         job_title = Title,
         job_description = JobDescription,
         job_requirement = JobRequirment,
         job_qualification = RequiredQual)

########################
# Export final output to CSV
########################

write.csv(new_df, file.path(base_path, "refined_jobpost_data.csv"), row.names = F)
