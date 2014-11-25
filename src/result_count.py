#!/usr/bin/env python
# -*- coding:utf8 -*-

import pickle
import os,sys


def result_count(data):
    all_num = len(data)
    top_1_right = 0
    top_5_right = 0
    top_10_right = 0

    for item in data:
        label, sim_scores = item
        if label == sim_scores[0][1]:
            top_1_right += 1
        for sim_score in sim_scores[0:5]:
            if label == sim_score[1]:
                top_5_right += 1
                break
        for sim_score in sim_scores:
            if label == sim_score[1]:
                top_10_right += 1
                break

    print top_1_right, top_5_right, top_10_right
    top_1_rate = top_1_right * 1.0 / all_num
    top_5_rate = top_5_right * 1.0 / all_num
    top_10_rate = top_10_right * 1.0 / all_num
    print top_1_rate, top_5_rate, top_10_rate




if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python result_count.py <result_file>"
        sys.exit()

    result_file = sys.argv[1]
    f = open(result_file, 'r')
    data = pickle.load(f)
    result_count(data)
    f.close()
