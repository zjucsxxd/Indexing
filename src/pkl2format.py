import pickle, pprint
import string
import os
import sys

def main(pkl_name):
    pkl_file = open(pkl_name, 'rb')

    lable, data = pickle.load(pkl_file).values()
    lableStr = ''
    dataStr = ''
    lb = []

    for row in lable:
        for mark in row:
            if int(mark) > kind_count:
                lb.append(0)
            else:
                lb.append(1)
                lableStr = lableStr + str(mark) + "\n"

    count = -1
    for row in data:
        outStr = ''
        count += 1

        if count%100 == 0:
            print count
        if total_count != -1 and count >= total_count:
            break

        if lb[count] == 0:
            continue
        for colum in row:
            value = '%f'%colum
            outStr = outStr + value + " "
        outStr = outStr + '\n'

        dataStr = dataStr + outStr
        
    pkl_file.close()
    
    lable_file.write(lableStr)
    data_file.write(dataStr)



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python pkl2format.py data_fold data_file lable_file kind_count(option) total_count(option)"
        sys.exit()

    fold        = sys.argv[1]
    data_file   = open( sys.argv[2], "w")
    lable_file  = open( sys.argv[3], "w")
    kind_count  = 150
    total_count = -1
    if len(sys.argv) == 5:
        kind_count = sys.argv[4]
    if len(sys.argv) == 6:
        total_count = sys.argv[5]
    

    count = 0
    for f in os.listdir(fold):
        count = count + 1
        #if count >= 40:
        #    break
        print f
        main(fold + f)

    lable_file.close()
    data_file.close()
