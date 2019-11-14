import pandas as pd
import config_reader
import json
from RumourEval2019Models.CLEARumor.src.dataset import VerifInstance


def from_sdqc_to_df(data, data_name='dummy'):
    '''
    Convert data to pandas frame for analysis
    :param data:
    :type data:
    :param data_name:
    :type data_name:
    :return:
    :rtype:
    '''
    data_name = data_name + '.pkl'
    data_dir = config_reader.get_dataframe_path()
    file_path = data_dir / data_name
    if file_path.is_file():
        return pd.read_pickle(file_path)
    df = pd.DataFrame()
    for instance in data:
        df = df.append(
            pd.merge(pd.io.json.json_normalize(instance.__dict__),
                     pd.io.json.json_normalize(instance.conversation.__dict__), on='id'))
    pd.to_pickle(df, file_path)
    df = df.drop(['conversation'], axis=1)
    return df


def from_verif_to_df(data, data_name='dummy'):
    '''
    Convert data to pandas frame for analysis
    :param data:
    :type data:
    :param data_name:
    :type data_name:
    :return:
    :rtype:
    '''
    data_name = data_name + '.pkl'
    data_dir = config_reader.get_dataframe_path()
    file_path = data_dir / data_name
    if file_path.is_file():
        return pd.read_pickle(file_path)
    df = pd.DataFrame()
    for instance in data:
        df = df.append(pd.io.json.json_normalize(instance.__dict__))
    pd.to_pickle(df, file_path)
    df = df.drop(['conversation.source', 'conversation.replies'], axis=1)
    return df


def get_dfs_from_archive(data_name):
    data_name = data_name + '.pkl'
    data_dir = config_reader.get_dataframe_path()
    file_path = data_dir / data_name
    if file_path.is_file():
        return pd.read_pickle(file_path)


def merge_sdqc_veracity(sdqc_df, verif_df):
    verif_df.loc[:, 'source_id'] = verif_df['id']
    return pd.merge(sdqc_df, verif_df, on='source_id')


def merge_answers(data, answer_path, name):
    with open(answer_path, 'r') as fin:
        answer = json.loads(fin.read())
        verif = pd.DataFrame.from_dict([[key, value[0]] for key, value in answer['subtaskbenglish'].items()])
        verif.columns = ['source_id', name + '_verif']
        merged_data = pd.merge(data, verif, on='source_id')
        sdqc = pd.DataFrame.from_dict(answer['subtaskaenglish'].items())
        sdqc.columns = ['id_x', name + '_sdqc']
        merged_data = pd.merge(merged_data, sdqc, on='id_x')
        data_dir = config_reader.get_dataframe_path()
        data_name = name + '.pkl'
        file_path = data_dir / data_name
        pd.to_pickle(merged_data, file_path)
    return merged_data

# if __name__ == '__main__':
#     data = get_dfs_from_archive('merged')
#     merge_answers(data,'/Users/tmp/Documents/veracity-detection/data/answers/answer_branch_lstm.json','branch_lstm')