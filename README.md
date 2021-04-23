# DSS Thesis

Code container for DSS Master thesis:

- CODES folder: includes all codes (R and python) for the project
  - (omitted) Thesis-Draft_Data-Cleaning.R: Data cleaning using R (run first)
  - (omitted) Thesis-Draft-Codes.ipynb: NLP text pre-processing + Clustering using python
  - (complete) 01_job-post__treating-missing-values.Rmd: visualize missing values in heatmap, extracting corresponding section in jobpost column to fill in missing values of columns [JobDescription, JobRequirment, RequiredQual], replace missing values by "Unprovided" value.
  - (complete) 02_job-title_01_pre-processing.ipynb: pre-processing text using NLP: lowercasing, removing stopwords, removing special characters, lemmatizing.
  - (complete) 02_job-title_02_embedding.ipynb: create document embeddings from pre-trained GloVe word embeddings (convert glove.6B.100d.txt extracted from the original file glove.6B.zip from https://nlp.stanford.edu/projects/glove/ to word2vec format using python gensim function glove2word2vec)
  - (experiment) 02_job-title_03_clustering-bak.ipynb: k-means clustering document embeddings and calculate Silhouette score with k range = (2-100) + Hopkins statistic with document embeddings 
- DATASET folder: includes all dataset needed to run the codes
  - original online-job-postings.csv: is retrieved here: https://www.kaggle.com/udacity/armenian-online-job-postings
  - refined refined_jobpost_data.csv: is output of Missingness Treatment Rscript (01_job-post__treating-missing-values.Rmd)
  - clean_title_df.csv: output of pre-processing python script (02_job-title_01_pre-processing.ipynb)
  - title_embeddings.npy: embeddings, output of embedding creation python script (02_job-title_02_embedding.ipynb)
  - title_docs.csv: corpus, output of embedding creation python script (02_job-title_02_embedding.ipynb)
