import csv
import os
import pandas as pd
import datetime


generalLog = 'generalLog.csv'
versionCounterLog = 'versionLog.csv'
tempVersionCounterLog = 'tempVersionLog.csv'
def createGeneralLog():
    
    if os.path.isfile(generalLog) == False:
        with open(generalLog, 'w') as cfile:
            
            write = csv.writer(cfile)
            write.writerow(['filename', 'date', 'amplify', 'setting', 'noise filter', 'setting', 'normalize', 'setting'])


def createVersionLog():
    if os.path.isfile(versionCounterLog) == False:
        with open(versionCounterLog, 'w') as cfile:
            
            write = csv.writer(cfile)
            write.writerow(['filename', 'current # of files created'])
    
def createSpecificLog(filename, info):

    path = filename[:len(filename)-4]
    if os.path.isdir(path) == False:
        os.mkdir(path)
        csvpath = path+'/'+path+'-log.csv'
        #print("first: "+csvpath)
        #print(csvpath)
        with open(csvpath, 'w') as cfile:
            
            write = csv.writer(cfile)
            rate = info[2]
            length = info[3]/rate
            write.writerow(['filename', 'date', 'amplify', 'setting', 'noise filter', 'setting', 'normalize', 'setting'])

        print('\n\n===========ATTENTION===========')
        print('since this is the first time file {} have been used in the program'.format(filename))
        print('a directory for file {} has been created by the name of {}.'.format(filename, path))
        print('it will contain all the info/created samples/modfied versions of the file {}.'.format(filename))
        print('===============================\n\n')
        addNewToVersionLog(filename)
    else:
        csvpath = path+'/'+path+'-log.csv'
        if os.path.isfile(path) == False:
            csvpath = path+'/'+path+'-log.csv'
            with open(csvpath, 'w') as cfile:
                write = csv.writer(cfile)
                rate = info[2]
                length = info[3]/rate
                #write.writerow(['filename: '+filename, 'rate: '+str(rate), 'length: '+str(length)+' seconds'])
                write.writerow(['filename', 'date', 'amplify', 'setting', 'noise filter', 'setting', 'normalize', 'setting'])

def addNewToVersionLog(filename):
    
    fields = [filename, 0]
    with open(versionCounterLog, 'a') as cfile:
        write = csv.writer(cfile)
        write.writerow(fields)
        #cfile.write(filename+',0\n')


def addNewEntry(filename, amplify, setting1, bf, setting2, normalize, setting3):
    
    date = datetime.datetime.now()
    dateS = str(date.year)+'/'+str(date.month)+'/'+str(date.day)
    fields = [filename, dateS, amplify, setting1, bf, setting2, normalize, setting3]
    with open(generalLog, 'a') as cfile:
        write = csv.writer(cfile)
        write.writerow(fields)
        #cfile.write(filename+',0\n')

def increFile(filename):

    """
    with open(versionCounterLog) as f_in, open ('test.csv', 'w') as f_out:
        header = f_in.readline()
        f_out.write(header)
        for line in f_in:
            print(line)
            f_out.write(line)
    """

    with open(versionCounterLog, 'r') as cfile:
        reader = csv.reader(cfile.readlines())

    with open(tempVersionCounterLog, 'w+') as cfile:
        write = csv.writer(cfile)
        for line in reader:
            #print(line)
            if line[0] == filename:
                incre = int(line[1])
                incre+=1
                line[1] = str(incre)
                write.writerow(line)
            else:
                write.writerow(line)
    os.remove(versionCounterLog)
    os.rename(tempVersionCounterLog, versionCounterLog)

def getNum(filename):

    with open(versionCounterLog, 'r') as cfile:
        reader = csv.reader(cfile.readlines())
        for line in reader:
            if line[0] == filename:
                return line[1]


def printGeneral():
    
    file = 'generalLog.csv'
    df = pd.read_csv(file)
    pd.options.display.max_columns = len(df.columns)
    print(df)

#if os.path.isfile(generalLog) == False:
#    createGeneralLog()
#printGeneral()

