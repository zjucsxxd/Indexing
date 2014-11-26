import os
import linecache
import string
import sys

def getValue(filename, lineNum):
    line = linecache.getline( filename, lineNum )
    return line

def getMark(filename, outfile):
    fi = open(filename,"rb")
    fo = open(outfile, "w")
    for line in fi:
        if line[0] == '0' and line[1] == '0':
            sub = line[0:9]
            key = int(sub, 10)
            value = getValue(sys.argv[3], key)
            line = str(value[0:-1]) + "  " + line
        else:
            line = "\n\n" # + line
        fo.write(line)

    
    fi.close()
    fo.close()
       

def getLineValue(line):
    i = 0
    vStr = ""
    while(line[i] != ' '):
        vStr += line[i]
        i += 1
    if vStr == "":
        return -1

    return float(vStr)

def calPrecious(filename):
    fi = open(filename, "rb")

    count = -1
    flag = 0
    matchFlag = 0
    match = []
    kind = []
    value = -1
    for line in fi:
        if flag == 0 and line[0] != '\n':
            matchFlag = 0
            flag = 1
            count += 1
            kind.append(getValue(sys.argv[4], count+1))
            print "number " + str(count)+ ":  " + str(kind[count])

            value = getLineValue(line)
            if value  == kind[count]:
                matchFlag = 1
                print str(value)

        elif flag == 1 and line[0] != '\n':
            value = getLineValue(line)
            if value  == kind[count]:
                matchFlag = 1
                print str(value)

        elif flag == 1 and line[0] == '\n':
            if matchFlag == 0:
                match.append(0)
            else:
                match.append(1)

            flag = 0
            print "\n"

    t = 0.0
    for var in match:
        if var == 1:
            t += 1
            
    if len(match) != 0:
        print "\n------precious: %d / %d = %f-------\n"%(t, len(match), t*100/len(match))

    fi.close()



if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage: python calPrecious.py input_file output_file dataLable_file queryLable_file"
        sys.exit()
    
    getMark( sys.argv[1], sys.argv[2])
    calPrecious(sys.argv[2])
