import spacy
import regex as re


class FeatureExtractor:
    def __init__(self):
        self.ner = spacy.load("en_core_web_lg")

    def extract_ne(self,text:str)->str:
        '''
        This function extracts the name entities, and then replace them with the ne labels.
        :param text:
        :type text:
        :return:
        :rtype:
        '''
        doc = self.ner(text)
        for ent in doc.ents:
            text = text.replace(ent.text, '<'+ent.label_+'>')
        return text, doc.ents

    '@todo'
    def extract_hashtag(self, text:str)->str:
        '''
        This function extracts hashtags and then replace with <hashtag>
        :param text:
        :type text:
        :return:
        :rtype:
        '''
        pass

    '@todo'
    def extract_mention(self, text:str)->str:
        '''
        This function extracts mentions and the replace with <mention>
        :param text:
        :type text:
        :return:
        :rtype:
        '''
        pass

    def extract_url(self, text:str)->str:
        '''
        This function extracts urls and the replace with <url>
        :param text:
        :type text:
        :return:
        :rtype:
        '''
        return re.sub(r"http\S+", "<url>", text)

    def transform(self, *args):
        pass

    '@todo make callback functions as input'
    def pipeline(self, text:str)->str:
        text = self.extract_url(text)
        text = self.extract_ne(text)
        return text

