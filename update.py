#!/bin/env python3
import csv


def loadCSV(filename):
    with open(filename.csv) as csvfile:
        moduleReader = csv.reader(csvfile)
        moduleLists = [moduleList for moduleList in moduleReader]
    return moduleLists

def writeCSV(filename, moduleLists):
    with open(filename, 'w') as csvfile:
        moduleWriter = csv.writer(csvfile)
        maxLen = max([len(moduleList) for moduleList in moduleLists])
        moduleLists = [['Group Name']] + moduleLists
        for moduleList in moduleLists:
            if len(moduleList) < maxLen:
                moduleList += [''] * (maxLen - len(moduleList))
            print(len(moduleList))
            moduleWriter.writerow(moduleList)

if __name__ == '__main__':
    snakeMonster = ['snakeMonster','SA000','SA001','SA002','SA073']
    snake = ['snake','SA003','SA004','SA044']
    wSnakeMonster = ['wirelessSnakeMonster','SA005','SA006']
    writeCSV('modules.csv', [snakeMonster, snake, wSnakeMonster])
