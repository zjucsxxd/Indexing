#!/usr/bin/env python
# -*- coding:utf8 -*-

import re
import os, sys
import pickle

class CalPrecision:
    def __init__(self):
        self.reg = '[0-9\.]+'

    def process_result(self, result_file, top_n=100):
        tmp_result = []
        result_in = open(result_file, 'r')
        lines = result_in.readlines()
        length = len(lines)
        i = 0

        search_points_num = 0
        correct_num = 0

        while i < length:
            line = lines[i]
            if not line.startswith('T'):
                if line.startswith('M'):
                    break
                print 'T or M error on line ' + str(i)
                return
            # i=0 to i=1
            i += 1 
            
            searched_points_num = 0
            search_point_index = -1
            line = lines[i]
            if not line.startswith('Q'):
                print 'Q error on line ' + str(i)
                return
            else:
                nums = re.findall(self.reg, line)
                if len(nums) == 6:
                    searched_points_num = int(nums[-1])
                elif len(nums) == 2:
                    searched_points_num = 0
                search_point_index  = int(nums[0])

            correct_label = self.test_label[search_point_index]

            # i=1 to i=2
            i += 1
            end = i + searched_points_num
            searched_labels = []
            for j in range(i, min(i+top_n,end)):
                line = lines[j]
                if not line.startswith('0'):
                    print line
                    return
                train_sample_index = int(line.split('\t')[0])
                train_sample_label = self.train_label[train_sample_index]
                searched_labels.append(train_sample_label)
            if correct_label in searched_labels:
                correct_num += 1
            tmp_result.append((correct_label, searched_labels))
            
            search_points_num += 1
            '''
            sys.stdout.write('\ri from %d to %d' % (i, end) )
            sys.stdout.flush()
            '''
            i = end
        # print ''
        print correct_num, search_points_num, 1.0 * correct_num / search_points_num

        result_in.close()
        return tmp_result

    def read_tt_labels(self, train_label_file, test_label_file):
        self.train_label = self.read_labels(train_label_file)
        self.test_label  = self.read_labels(test_label_file)

    def read_labels(self, file_name):
        in_f = open(file_name, 'r')
        labels = []
        for line in in_f:
            labels.append(float(line))
        in_f.close()
        return labels


if __name__ == '__main__':
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print 'Usage: python cal_precisions.py <result> <train_label> <test_label> <top-n> <tmp_file>'
        sys.exit()
    
    result_file = sys.argv[1]
    train_label = sys.argv[2]
    test_label  = sys.argv[3]
    top_n = int(sys.argv[4])
    
    cp = CalPrecision()
    cp.read_tt_labels(train_label, test_label)
    tmp_result = cp.process_result(result_file, top_n)

    if len(sys.argv) == 6: 
        temp_file   = sys.argv[5]
        out_f = open(temp_file, 'w')
        pickle.dump(tmp_result, out_f)
        out_f.close()
