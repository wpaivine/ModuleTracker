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

def updateModuleList(listName, modules, authorName, email):
    '''Use this function to update the stored list associated with the name
    `listName` with list of strings `modules`. Requires GitPython'''
    if GIT == False:
        print('GitPython not installed, please install before updating module \
list', file=sys.stderr)
    else:
        moduleLists = _loadCSV()
        if listName in moduleLists:
            oldVals = moduleLists[listName]
        else:
            oldVals = 'N/A'
        
        if oldVals == modules:
            return
        if modules == [] and oldVals != 'N/A':
            del moduleLists[listName]
            listDump = [[key]+moduleLists[key] for key in moduleLists]
            _writeCSV(listDump)
            _updateGit('Removed moduleList "{}"'.format(listName), 
                    '{} <{}>'.format(authorName, email))
        else:
            moduleLists[listName] = modules
            listDump = [[key]+moduleLists[key] for key in moduleLists]
            _writeCSV(listDump)
            _updateGit('Updated moduleList "{}" from \n{}\n to \
                    \n{}\n'.format(listName, oldVals, modules), 
                    '{} <{}>'.format(authorName, email))

def _updateGit(message, author):
    if GIT == False:
        print('GitPython not installed, please install before updating git \
repo', file=sys.stderr)
    else:
        repo.git.add(CSVFILE)
        try:
            repo.git.commit('-m', message, author=author)
        except: # push our local changes even if the previous commit failed (we
            # could have stored commits
            pass
        repo.git.push()


def _syncCSV():
    if GIT == False:
        urllib.request.urlretrieve(RAW_URL, FILENAME)
    else:
        try:
            repo.remotes.origin.pull()
        except: # If can't connect
            pass
        repo.git.checkout(CSVFILE)


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
        moduleLists = [['Group Name']] + moduleLists
        maxLen = max([len(moduleList) for moduleList in moduleLists])
        for moduleList in moduleLists:
            if len(moduleList) < maxLen:
                moduleList += [''] * (maxLen - len(moduleList))
            moduleWriter.writerow(moduleList)


if __name__ == '__main__':
    from tkinter import *
    from tkinter import messagebox, simpledialog
    class Dialog(Listbox):

        def __init__(self, master, selectmode=EXTENDED, height = 10):
            Listbox.__init__(self, master, selectmode=selectmode, height = height)
            self.current = None

        def poll(self, callback):
            now = self.curselection()
            if now != self.current:
                callback(now)
                self.current = now
            self.after(250, lambda : self.poll(callback))

    class ListInterface:
        def __init__(self, master, listNameBox, listEditorPanel):
            self.master = master
            self.listNameBox = listNameBox
            self.listEditorPanel = listEditorPanel
            self.current = None
            self.refreshListNames()

        def loadLists(self):
            self.moduleLists = _loadCSV()

        def refreshListNames(self):
            self.loadLists()
            self.listNameBox.delete(0,END)
            for name in self.moduleLists:
                self.listNameBox.insert(END, name)

        def updateDisplayedList(self, selection):
            if selection:
                selection = self.listNameBox.get(selection)
                self.current = selection
                self.listEditorPanel.delete(1.0,END)
                self.listEditorPanel.insert(END,
                        '\n'.join(self.moduleLists[selection]))

        def saveList(self):
            if GIT == False and messagebox.askyesno('Install \
GitPython','GitPython is required to save, but it is not currently installed. \
Would you like to install it now?'):
                 _installGitPython()           
            if GIT == False:
                return
            
            modules = self.listEditorPanel.get(1.0,END).split('\n')
            modules = [entry for entry in modules if entry != '']

            authorName = simpledialog.askstring('Enter your name.', 
                                                'What is your name?',
                                                parent=self.master)
            email = simpledialog.askstring('Enter your email.', 
                                           'What is your email?',
                                           parent=self.master)
            messagebox.showinfo('Notice', 
                'You will now have to enter your git credentials in the terminal window'
            )
            updateModuleList(self.current, modules, authorName, email)
            self.refreshListNames()
            print('Done.')
        def addList(self):
            robotName = simpledialog.askstring('Enter the name.', 
                                               'What is the name of the robot?',
                                               parent=self.master)
            self.moduleLists[robotName] = []
            self.listNameBox.insert(END, robotName)
            self.listEditorPanel.delete(1.0,END)
            self.current = robotName



    master = Tk()
    listNames = Dialog(master, selectmode=SINGLE, height=30)
    listEditorPanel = Text(master)
    interface = ListInterface(master, listNames, listEditorPanel)
    listEditorPanel.grid(row=1, column=2, rowspan=5)
    listNames.grid(row=1, column=0, rowspan=7, columnspan=2)
    Button(master, text = 'Refresh', command = interface.refreshListNames).grid(row = 0, column = 0, columnspan = 1)
    Button(master, text = 'Save', command = interface.saveList).grid(row = 0, column = 2, columnspan = 1)
    Button(master, text = 'Add', command = interface.addList).grid(row = 0, column = 1, columnspan = 1)
    listNames.poll(interface.updateDisplayedList)
    mainloop()

    snakeMonster = ['snakeMonster','SA000','SA001','SA002','SA073']
    snake = ['snake','SA003','SA004','SA044']
    wSnakeMonster = ['wirelessSnakeMonster','SA005','SA006']
