from RumourEval2019Models.CLEARumor.src.dataset import get_conversations_from_archive
from pathlib import Path

if __name__ == '__main__':
    root = Path('data/rumoureval')
    training_data = (root/ 'rumoureval-2019-training-data.zip')
    test_data = (root/ 'rumoureval-2019-test-data.zip')
    get_conversations_from_archive(training_data, test_data)
