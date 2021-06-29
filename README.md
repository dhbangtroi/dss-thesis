# DSS Thesis

Code container for DSS Master thesis:

- CODES folder: includes all codes (R and python) for the project
  - (omitted) Thesis-Draft_Data-Cleaning.R: Data cleaning using R (run first)
  - (omitted) Thesis-Draft-Codes.ipynb: NLP text pre-processing + Clustering using python
  
  * JOB TITLES: 
  - (complete) 01_job-post__treating-missing-values.Rmd: visualize missing values in heatmap, extracting corresponding section in jobpost column to fill in missing values of columns [JobDescription, JobRequirment, RequiredQual], replace missing values by "Unprovided" value.
  - (complete) 02_job-title_01_pre-processing.ipynb: pre-processing text using NLP: lowercasing, removing stopwords, removing special characters, lemmatizing.
  - (complete) 02_job-title_02_doc_embedding.ipynb: create document embeddings from pre-trained word embeddings (spacy)
  - (complete) 02_job-title_03a_testing-cluster-tendency.ipynb: test cluster tendency of the document embeddings
  - (complete) 02_job-title_03b_reducing-dimensions-4visualization.ipynb: reduce dimensions of document embeddings for t-SNE and PCA visualization
  - (complete) 02_job-title_04a_clustering-kmeans.ipynb: cluster document embeddings of job titles using kmeans
  - (complete) 02_job-title_04b_clustering-genie.ipynb: cluster document embeddings of job titles using genie
  - (complete) 02_job-title_04c_clustering-hdbscan.ipynb: cluster document embeddings of job titles using HDBSCAN
  - (complete) 02_job-title_04d_clustering-lda.ipynb: cluster document embeddings of job titles using LDA
  - (complete) 02_job-title_04e_clustering-gsdmm.ipynb: cluster document embeddings of job titles using GSDMM
  
- DATASET folder: includes all dataset needed to run the codes
  - original online-job-postings.csv: is retrieved here: https://www.kaggle.com/udacity/armenian-online-job-postings
  - refined refined_jobpost_data.csv: is output of Missingness Treatment Rscript (01_job-post__treating-missing-values.Rmd)
  - clean_title_df.csv: output of pre-processing python script (02_job-title_01_pre-processing.ipynb)
  - title_embeddings.npy: embeddings, output of embedding creation python script (02_job-title_02_doc_embedding.ipynb)
  - title_docs.csv: corpus, output of embedding creation python script (02_job-title_02_doc_embedding.ipynb)
