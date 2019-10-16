from torch.utils.data import Dataset
from RumourEval2019Models.CLEARumor.src.dataset import get_conversations_from_archive
from RumourEval2019Models.CLEARumor.src.dataset import load_sdcq_instances
from RumourEval2019Models.CLEARumor.src.dataset import load_verif_instances
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

        def __init__(self, id: str, conversation, label: Optional[Label] = None):
            self.id = id
            self.conversation = conversation
            self.label = label.name

        def __repr__(self):
            return 'SDQC ({}, {})'.format(self.conversation, self.label)

    def _init_dataset(self, conversations):
        train_instances, dev_instances, test_instances = load_sdcq_instances()
        for _, conversation in conversations.items():
            source = conversation['source']
            label = next((x.label for x in train_instances if x.post_id == source.id), None)

            if label:
                self.train.append(self.SDQCInstance(source.id, source, label))
                replies = conversation['replies']

                for reply in replies:
                    label = next((x.label for x in train_instances if x.post_id == reply.id))
                    self.train.append(self.SDQCInstance(reply.id, reply, label))
            else:
                # try for dev
                label = next((x.label for x in dev_instances if x.post_id == source.id), None)
                if label:
                    self.dev.append(self.SDQCInstance(source.id, source, label))
                    replies = conversation['replies']

                    for reply in replies:
                        label = next((x.label for x in dev_instances if x.post_id == reply.id))
                        self.dev.append(self.SDQCInstance(reply.id, reply, label))
                else:
                    # try for test
                    label = next((x.label for x in test_instances if x.post_id == source.id), None)
                    self.test.append(self.SDQCInstance(source.id, source, label))
                    replies = conversation['replies']

                    for reply in replies:
                        label = next((x.label for x in test_instances if x.post_id == reply.id))
                        self.test.append(self.SDQCInstance(reply.id, reply, label))


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
