#!/usr/bin/env python
# -*- coding:utf8 -*-

import os,sys
import pickle
import numpy as np
from numpy import linalg


def get_files(folder):
    filenames = os.listdir(folder)
    filenames.sort()
    return filenames

class SimSearch:
    def __init__(self, test_folder, train_folder):
        self.test_folder = test_folder
        self.train_folder = train_folder
        if not self.test_folder.endswith('/'):
            self.test_folder += '/'
        if not self.train_folder.endswith('/'):
            self.train_folder += '/'

    def get_filenames(self):
        self.test_files = get_files(self.test_folder)[1:]
        self.train_files = get_files(self.train_folder)[1:]
        # print self.test_files
        # print self.train_files

    def load_train(self):
        self.train_datas = []
        for file_name in self.train_files:
            file_path = self.train_folder + file_name
            f = open(file_path, 'r')
            data = pickle.load(f)
            f.close()
            self.train_datas.append(data)

    def load_test(self):
        self.test_datas = []
        for file_name in self.test_files:
            file_path = self.test_folder + file_name
            f = open(file_path, 'r')
            data = pickle.load(f)
            f.close()
            self.test_datas.append(data)
    
    def test(self, out_file='search_result', top_n = 10):
        results = []
        counter = 0
        for i in range(2):
            test_da = self.test_datas[i]
            test_d = test_da['data']
            test_l = test_da['labels']
            for j in range(test_d.shape[0]):
                test_item = test_d[j]
                test_item_label = test_l[0][j]
                sim_scores = self.test_one(test_item, top_n)
                results.append((test_item_label, sim_scores))
                counter += 1
                sys.stdout.write('\rdone: ' + str(counter))
                sys.stdout.flush()

        f = open(out_file, 'w')
        pickle.dump(results, f)
        f.close()


    def test_one(self, test_item, top_n=10):
        all_sim_scores = []
        for i in range(len(self.train_datas)):
            sim_scores = self.test_one_on_one_batch(test_item, i)
            all_sim_scores += sim_scores
        all_sim_scores = sorted(all_sim_scores, key=lambda d:d[0], reverse=False)
        return all_sim_scores[0:top_n]

    def test_one_on_one_batch(self, test_item, train_datas_index, top_n=10):
        data = self.train_datas[train_datas_index]
        d = data['data']
        l = data['labels']
        sim_scores = []
        for i in range(d.shape[0]):
            dist = linalg.norm(test_item - d[i])
            sim_scores.append((dist, l[0][i]))
        sim_scores = sorted(sim_scores, key=lambda d:d[0], reverse=False)
        return sim_scores[0:top_n]

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python sim_search.py test_folder train_folder result_file'
        sys.exit()
    
    ss = SimSearch(sys.argv[1], sys.argv[2])
    ss.get_filenames()
    print 'loading train ...'
    ss.load_train()
    print 'loading test  ...'
    ss.load_test()
    ss.test(sys.argv[3], 10)
