# Developed on March 24, 25 and 26, 2020.

import argparse
import itertools
import re
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def read_excel(io):
    df = pd.read_excel(io)
    df = df.fillna('')
    return df

def add_column_parts(df, column):
    data = [re.split(r'\#|\$|\;|\,', code) for code in df[column]]
    max_parts = max([len(parts) for parts in data])
    for i in range(max_parts):
        new_column = f'{column}_{i}'
        assert new_column not in df.columns
        df[new_column] = [parts[i] if i < len(parts) else '' for parts in data]

def add_columns_parts(df):
    for column in df.columns:
        add_column_parts(df, column)

def show_barplot(data_frame, path):
    num_columns = len(data_frame.columns)
    count_unique = [len(set(data_frame[column]) - set([''])) for column in data_frame.columns]
    count_total = [len(data_frame[data_frame[column] != '']) for column in data_frame.columns]
    data = pd.DataFrame()
    data['field'] = list(data_frame.columns) * 2
    data['count'] = count_unique + count_total
    data['count type'] = ['unique'] * num_columns + ['total'] * num_columns
    plt.figure('Number of unique vs total values')
    ax = sns.barplot(x='count', y='field', hue='count type', data=data, orient='h')
    for i, v1, v2 in itertools.zip_longest(range(num_columns), count_unique, count_total):
        ax.text(x=v2, y=i, s='%s/%s' % (v1, v2), va='center')
    plt.title(path)
    plt.show()
    plt.close()

def analyze_files(paths):
    for path in paths:
        df = read_excel(path)
        add_columns_parts(df)
        show_barplot(df, path)

def main(args):
    parser = argparse.ArgumentParser('python3 %s' % (args[0]))
    parser.add_argument('paths', action='store', nargs='+', type=str, \
        help='the relative or absolute path to a file or folder', metavar='path')
    args = parser.parse_args(args[1:])
    analyze_files(args.paths)

if __name__ == '__main__':
    main(sys.argv)
