from torch.utils.data import Dataset
from RumourEval2019Models.CLEARumor.src.dataset import get_conversations_from_archive
from RumourEval2019Models.CLEARumor.src.dataset import load_sdcq_instances
from RumourEval2019Models.CLEARumor.src.dataset import load_verif_instances
from RumourEval2019Models.CLEARumor.src.dataset import Post
from typing import Optional
from enum import Enum


class RumourDataset(Dataset):
    def __init__(self, conversations):
        self.verif_dataset = None
        self.sdqc_dataset = None
        self.conversations = conversations
        self._init_dataset()

    def _init_dataset(self):
        self.verif_dataset = VerifDataset(self.conversations)
        self.sdqc_dataset = SDQCDataset(self.conversations)

    def get_sdqc(self):
        return self.sdqc_dataset

    def get_verif(self):
        return self.verif_dataset

class SDQCDataset(Dataset):
    def __init__(self, conversations):
        self.train = []
        self.dev = []
        self.test = []
        self._init_dataset(conversations)

    class SDQCInstance:
        class Label(Enum):
            """Enum for SDQC labels `support`, `deny`, `query`, and `comment`."""
            support = 0
            deny = 1
            query = 2
            comment = 3

        def __init__(self, id: str, post: [Post],source_post:Optional[Post],prev_post:Optional[Post],label: Optional[Label] = None):
            self.id = id
            self.post = post
            self.label = label.name
            self.source_post = source_post
            self.prev_post = prev_post

        def __repr__(self):
            return 'SDQC ({}, {})'.format(self.conversation, self.label)

    def _init_dataset(self, conversations):
        train_instances, dev_instances, test_instances = load_sdcq_instances()
        for _, conversation in conversations.items():
            source = conversation['source']
            label = next((x.label for x in train_instances if x.post_id == source.id), None)

            if label:
                self.train.append(self.SDQCInstance(source.id, source,None, None,label))
                replies = conversation['replies']

                for i in range(len(replies)):
                    label = next((x.label for x in train_instances if x.post_id == replies[i].id))
                    if i == 0:
                        self.train.append(self.SDQCInstance(replies[i].id, post=replies[i], source_post=source, prev_post= None, label=label))
                    else:
                        self.train.append(self.SDQCInstance(replies[i].id, post=replies[i], source_post=source, prev_post=replies[i-1], label=label))
            else:
                # try for dev
                label = next((x.label for x in dev_instances if x.post_id == source.id), None)
                if label:
                    self.dev.append(self.SDQCInstance(source.id, source,None, None,label))
                    replies = conversation['replies']

                    for i in range(len(replies)):
                        label = next((x.label for x in dev_instances if x.post_id == replies[i].id))
                        if i == 0:
                            self.dev.append(self.SDQCInstance(replies[i].id, post=replies[i], source_post=source, prev_post= None, label=label))
                        else:
                            self.dev.append(self.SDQCInstance(replies[i].id, post=replies[i], source_post=source, prev_post=replies[i-1], label=label))
                else:
                    # try for test
                    label = next((x.label for x in test_instances if x.post_id == source.id), None)
                    self.test.append(self.SDQCInstance(source.id, source,None, None, label))
                    replies = conversation['replies']

                    for i in range(len(replies)):
                        label = next((x.label for x in test_instances if x.post_id == replies[i].id))
                        if i==0:
                            self.test.append(self.SDQCInstance(replies[i].id, post=replies[i], source_post=source, prev_post= None, label=label))
                        else:
                            self.test.append(self.SDQCInstance(replies[i].id, post=replies[i], source_post=source, prev_post=replies[i-1], label=label))

class VerifDataset(Dataset):
    def __init__(self, conversations):
        self.train = []
        self.dev = []
        self.test = []
        self._init_dataset(conversations)

    class VerifInstance:
        class Label(Enum):
            """ Enum for verification labels `true`, `false`, and `unverified`."""
            false = 0
            true = 1
            unverified = 2

        def __init__(self, id, conversation, label: Optional[Label] = None):
            self.id = id
            self.conversation = conversation
            self.label = label.name

        def __str__(self):
            print('Verif ({}, {})'.format(self.conversation, self.label))

    def _init_dataset(self, conversations):
        train_instances, dev_instances, test_instances = load_verif_instances()
        for instance in train_instances:
            self.train.append(self.VerifInstance(instance.post_id, conversations.get(instance.post_id), instance.label))

        for instance in dev_instances:
            self.dev.append(self.VerifInstance(instance.post_id, conversations.get(instance.post_id), instance.label))

        for instance in test_instances:
            self.test.append(self.VerifInstance(instance.post_id, conversations.get(instance.post_id), instance.label))

if __name__ == '__main__':
    conversations = get_conversations_from_archive()
    rumour_dataset = RumourDataset(conversations)
