#!/bin/env python3
import csv
import sys
import pip
import os.path
import urllib.request
import urllib.parse

packageDirectory = os.path.dirname(__file__) 

CSVFILE = 'modules.csv'
REPO = 'wpaivine/ModuleTracker/' # needs to end in /
FILENAME = os.path.join(packageDirectory, CSVFILE)
URL = urllib.parse.urljoin('https://github.com/',REPO[:-1])
RAW_URL = urllib.parse.urljoin(
            urllib.parse.urljoin('https://raw.githubusercontent.com/', REPO),
            urllib.parse.urljoin('master/', 'modules.csv')
        )

def _loadGitPython():
    global GIT
    global repo
    try:
        from git import Repo
        repo = Repo(packageDirectory)
        GIT = True
    except ImportError:
        GIT = False
        repo = None

_loadGitPython()

def getModuleList(listName):
    '''Use this function to get the list of modules associated with the given
    listName'''
    moduleLists = _loadCSV()
    if not listName in moduleLists:
        print('Module list {} not found!'.format(listName), file=sys.stderr)
        return None
    else:
        return moduleLists[listName]

def updateModuleList(listName, modules):
    '''Use this function to update the stored list associated with the name
    `listName` with list of strings `modules`. Requires GitPython'''
    if GIT == False:
        print('GitPython not installed, please install before updating module \
        list', fiel=sys.stderr)
    else:
        moduleLists = _loadCSV()
        moduleLists[listName] = modules
        listDump = [[key]+moduleLists[key] for key in moduleLists]
        _writeCSV(listDump)
        _updateGit()

def _updateGit():
    if GIT == False:
        print('GitPython not installed, please install before updating git \
                repo', file=sys.stderr)
    else:
        pass


def _syncCSV():
    if GIT == False:
        urllib.request.urlretrieve(RAW_URL, FILENAME)
    else:
        repo.remotes.origin.pull()


def _installGitPython():
    pip.main(['install', 'gitpython'])
    _loadGitPython()

def _loadCSV():
    _syncCSV()
    with open(FILENAME, 'r') as csvfile:
        moduleReader = csv.reader(csvfile)
        moduleLists = [[entry for entry in moduleList if entry != ''] for
                moduleList in moduleReader]
        moduleLists = {moduleList[0]:moduleList[1:] for moduleList in
                moduleLists[1:]}
    return moduleLists

def _writeCSV(moduleLists):
    with open(FILENAME, 'w') as csvfile:
        moduleWriter = csv.writer(csvfile)
        maxLen = max([len(moduleList) for moduleList in moduleLists])
        moduleLists = [['Group Name']] + moduleLists
        for moduleList in moduleLists:
            if len(moduleList) < maxLen:
                moduleList += [''] * (maxLen - len(moduleList))
            moduleWriter.writerow(moduleList)


if __name__ == '__main__':
    snakeMonster = ['snakeMonster','SA000','SA001','SA002','SA073']
    snake = ['snake','SA003','SA004','SA044']
    wSnakeMonster = ['wirelessSnakeMonster','SA005','SA006']
    writeCSV('modules.csv', [snakeMonster, snake, wSnakeMonster])
