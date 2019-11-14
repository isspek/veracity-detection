import numpy as np

def stances_from_replies(replies):


if __name__ == '__main__':
    p = [[0.56225159,0.17711719 ,0.07712304 ,0.18350819],
     [0.6778293 , 0.14636666 ,0.05955794 ,0.11624611],
     [0.73968982 ,0.16584648, 0.0584374 , 0.0360263 ]]
    p2 = []

    stances_train = []
    for p in [p,p2]:
        divided_p = np.divide(np.sum(p, axis=0), len(p)) if p else np.zeros((4,), dtype=float)
        print(divided_p)
        stances_train = np.append(stances_train, divided_p)

    stances_train = stances_train.reshape(-1, 4)
    print(stances_train.shape)