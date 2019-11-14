from sklearn.feature_extraction.text import TfidfVectorizer
from bert_serving.client import BertClient


class LangModel(object):
    def __init__(self):
        pass

    @classmethod
    def transform(cls,test_data):
        pass

class BagOfWordsGenerator(LangModel):
    def __init__(self, train_data, feat_extractor):
        self.vector = TfidfVectorizer(
            tokenizer=feat_extractor.tokenize,
            preprocessor=feat_extractor.preprocess,
            ngram_range=(1, 3),
            stop_words=None,  # We do better when we keep stopwords
            strip_accents=None,
            use_idf=True,
            smooth_idf=False,
            norm=None,  # Applies l2 norm smoothing
            decode_error='replace',
            max_features=10000,
            min_df=5,
            max_df=0.501)
        self.vector.fit_transform(train_data)
        self.train = self.vector.transform(train_data).toarray()

    def transform(self, test_data):
        return self.vector.transform(test_data).toarray()

class BERTEmbeddings:
    def __init__(self):
        self.bert_client = BertClient(ip='141.26.208.141', port = 8088)

    def transform(self,test_data):
        self.bert_client.encode(test_data)


def model_selection(model_name:str,feat_extractor = None,train_data=None)->LangModel:
    if model_name is 'tf-idf':
        return BagOfWordsGenerator(train_data,feat_extractor)
    elif model_name is 'bert':
        return BERTEmbeddings()


if __name__ == '__main__':
    bc = BERTEmbeddings()
    try:
        vec = bc.transform(['hey you', 'whats up?'])
    except:
        print('error')


# class Word2Vec:
#     def __init__(self):
#         self.vector = gensim.models.KeyedVectors.load_word2vec_format(config.get_word2vec_pretrain(), binary=True)