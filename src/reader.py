from RumourEval2019Models.CLEARumor.src.dataset import get_conversations_from_archive
from src.feature_extractor import FeatureExtractor
from itertools import chain
from RumourEval2019Models.CLEARumor.src.dataset import load_posts, \
    load_sdcq_instances, load_verif_instances

if __name__ == '__main__':
    feature_extractor = FeatureExtractor()
    result = get_conversations_from_archive()
    single_sample = result['552783667052167168']['source']
    print(single_sample)
    print(feature_extractor.pipeline(single_sample.raw_text))

    sdqc_train_instances, sdqc_dev_instances, sdqc_test_instances = \
        load_sdcq_instances()
    sdqc_all_instances = list(chain(
        sdqc_train_instances, sdqc_dev_instances, sdqc_test_instances))
    verif_train_instances, verif_dev_instances, verif_test_instances = \
        load_verif_instances()
    verif_all_instances = list(chain(
        verif_train_instances, verif_dev_instances, verif_test_instances))

    print(sdqc_dev_instances)
