import pandas as pd
import random

def redundancy(datafile, n):
    data = pd.read_csv(datafile, index_col=None)



    # 随机对每个任务选取 n 个工人注释
    sample_data = pd.DataFrame()


    max = 0
    for _, group in data.groupby("taskId"):
        nums = len(group)
        if max < nums:
            max = nums
        if nums < n:
            sample_data = pd.concat([sample_data, group])
        else:
            sample_data = pd.concat([sample_data, group.sample(n, random_state=random.randint(0, 1000))])

    sample_data.reset_index(drop=True, inplace=True)
    print(sample_data)
    print(max)
    sample_data.to_csv('../data/redundancy_2/train_data_' + str(n) + '.csv', index=0)
if __name__ == '__main__':

    datafile = '../data/new/train/data_train.csv'

    for n in range(1, 4):
        redundancy(datafile, n)

