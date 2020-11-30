from gensim.models import LdaMulticore


# find the optimal number of topics 

def compute_coherence_values(dictionary, bow_corpus, processed_corpus, limit, start=3, step=1):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    d = {}
    for num_topics in range(start, limit, step):
        model = LdaMulticore(corpus=bow_corpus,
                             id2word=dictionary,
                             num_topics=num_topics,
                             workers=3,
                             alpha='symmetric', # 'auto' is only available in plain LDA model
                             eta='auto')
        coherencemodel = CoherenceModel(model=model, texts=processed_corpus, dictionary=dictionary, coherence='c_v')
        d[num_topics] = (model, coherencemodel.get_coherence())

    return d


d = compute_coherence_values(dictionary, bow_corpus, processed_corpus, limit=10, start=3, step=1)

x = d.keys()
coherence_values = [t[1] for t in d.values()]
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.show()