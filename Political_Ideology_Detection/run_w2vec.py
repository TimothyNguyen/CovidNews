import numpy as np  # Make sure that numpy is imported
import gensim

# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
# Index2word is a list that contains the names of the words in
# the model's vocabulary. Convert it to a set, for speed
index2word_set = set(model.index2word)


def make_feature_vec(words, num_features):
    # Function to average all of the word vectors in a given
    # paragraph
    #
    # Pre-initialize an empty numpy array (for speed)
    feature_vec = np.zeros((num_features,), dtype="float32")
    #
    nwords = 0.
    #

    # Loop over each word in the review and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            feature_vec = np.add(feature_vec, model[word])
    #
    # Divide the result by the number of words to get the average
    feature_vec = np.divide(feature_vec, nwords)
    return feature_vec