from RumourEval2019Models.CLEARumor.src.dataset import get_conversations_from_archive
from src.feature_extractor import FeatureExtractor

if __name__ == '__main__':
    feature_extractor = FeatureExtractor()
    result = get_conversations_from_archive()
    single_sample = result['552783667052167168']['source']
    print(feature_extractor.pipeline(single_sample.raw_text,'extract_ne'))
