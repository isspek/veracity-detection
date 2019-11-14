from RumourEval2019Models.RumourDataset import RumourDataset
from RumourEval2019Models.CLEARumor.src.dataset import get_conversations_from_archive
import RumourEval2019Models.utils as utils

if __name__ == '__main__':
    conversation = get_conversations_from_archive()
    rumour_dataset = RumourDataset(conversation)
    sdqc_train = utils.to_pd_frame(rumour_dataset.sdqc_dataset.train, 'sdqc_train')
    verif_train = utils.to_pd_frame(rumour_dataset.verif_dataset.train, 'verif_train')
