import numpy as np
import math
from tqdm.notebook import tqdm

def build_corpus(corpus1, N=20):
    """
    Function to build corpus
    Inputs:
        corpus1: list of documents created from id2word.doc2bow of Gensim
        N: parameter used to normalize the document lengths, which is required for the Poisson model.
    Return:
        corpus with normalized words
    """

    totals = []
    for doc in corpus1:
        Nm = 0
        for word in doc:
            Nm += word[1]
        totals.append(Nm)
        
    corpus = []
    pbar1 = tqdm(desc="Build corpus", total=len(corpus1))
    for m, doc2 in enumerate(corpus1):
        document = []
        Nm = 0
        for word in doc2:
            Nm += word[1]
            a = list(word)  # (word_id, count)
            a[1] = (float(word[1])/totals[m])*N
            document.append(tuple(a))
        corpus.append(document)
        pbar1.update(1)
    pbar1.close()
    return corpus
       
       
def getTopicWordCount(nTopics, id2word, numDocuments, corpus):
    """
    Function to get list of word count per topic
    Inputs:
        nTopics: number of finalized topics (clusters)
        id2word: Gensim list of word ids and word counts per doc
        numDocuments: number of documents (input data)
        corpus: corpus returned from function build_corpus()
    Return: 
        List of topic words and counts per doc
    """
    topicWordCount = []
    pbar1 = tqdm(desc="Initialize topicWordCount", position=1, total=nTopics)
    for i in range(nTopics):
        topicWordCount.append(
            [0 for x in range(len(id2word))])  # initialise
        pbar1.update(1)
    pbar1.close()
    
    pbar1 = tqdm(desc="Update number of occurences of word", position=1, total=len(range(numDocuments)))
    for d in range(numDocuments):
        for j in range(len(corpus[d])):
            word = corpus[d][j]
            for topic in range(nTopics):
                # update number of occurences of word w in document
                topicWordCount[topic][word[0]] += word[1]		
        pbar1.update(1)
    pbar1.close()
    
    return topicWordCount
		
def getTopTopicalWords(selected_topics, topicWordCount, id2word, twords=10):
    """
    Function to retrieve top words per topic
    Inputs:
        selected_topics: list of finalized topic ids (cluster labels)
        topicWordCount: List of topic words and counts returned from function getTopicWordCount()
        id2word: Gensim list of word ids and word counts per doc
        twords: number of top words per topic
    Return:
        List of word indices sorted by word count per topic
        List of words sorted by word count per topic
    """
    coherence_index_all = []
    coherence_word_all = []

    pbar1 = tqdm(desc="Get Top words of topics", position=1,
                 total=len(selected_topics))
    for idx, t in enumerate(selected_topics):
        wordCount = {w: topicWordCount[idx][w]
                     for w in range(len(id2word))}

        count = 0
        coherence_word_per_topic = []
        coherence_index_per_topic = []

        for index in sorted(wordCount, key=wordCount.get, reverse=True):
            coherence_index_per_topic.append(index)
            coherence_word_per_topic.append(id2word[index])
            count += 1

            if count >= twords:
                break
        coherence_index_all.append(coherence_index_per_topic)
        coherence_word_all.append(coherence_word_per_topic)
        pbar1.update(1)
    pbar1.close()
    return coherence_index_all, coherence_word_all

def coherence(corpus, coherence_index_all, nTopics):
    """
    Function to calculate topic coherence of the Topic Model
    Inputs:
        corpus: corpus returned from function build_corpus()
        coherence_index_all: top words per topic returned from function getTopTopicalWords()
        nTopics: number of finalized topics (clusters)
    Return:
        Coherence score
    """
    
    coherence_corpus = []
    for a in corpus:
        coherence_doc = []
        for b in a:
            coherence_doc.append(b[0])
        coherence_corpus.append(coherence_doc)

    nTopWords = len(coherence_index_all[0])  # number of top words per topic
    nDocs = len(coherence_corpus)  # number of documents
    epsilon = 1  # smoothing parameter
    coherence = []

    pbar1 = tqdm(desc="Compute topic coherence", position=1,
                 total=len(range(0, nTopics)))
    for t in range(0, nTopics):  # calculate coherence
        for vj in range(1, nTopWords):  # each word in topic t
            Dvj = 0
            for d in range(0, nDocs):
                # check how many docs contain word vj
                if (coherence_index_all[t][vj] in coherence_corpus[d]):
                    Dvj += 1

            for vi in range(0, vj):
                Dvjvi = 0
                for d in range(0, nDocs):
                    # check how many docs contain both word vj and vi
                    if (coherence_index_all[t][vj] in coherence_corpus[d]) and (coherence_index_all[t][vi] in coherence_corpus[d]):
                        Dvjvi += 1

                coherence.append(math.log((Dvjvi+epsilon)/float(Dvj), 10))

        pbar1.update(1)
    pbar1.close()

    return np.sum(coherence)/nTopics
		