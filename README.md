# ModuleTracker
Keeps the list of modules in the biorobotics robots synced, so if someone
replaces a robot module on a robot, and has to update their code accordingly,
the change is updated across all computers in the lab. Uses git for version
control, and works offline (uses last synced values). Can be imported in python
code to directly give the saved list of modules, or can be run standalone to
produce an output CSV file which can then be used in C, C++, MATLAB code, etc.
Use this so demo code isn't broken by changes to the robot when performing
research!

## Installation
Clone this repo next to where you want to use it.

## Usage
To update the CSV file, run
```
    python tracker.py -u
```
There are no external dependecies required for syncing.

To run within python, see 'example.py'.

To save new values, update old values, create new robots, or delete old robots,
run the file 'tracker.py' a tkinter GUI should pop up with an editable box with
the module names, one per line. To delete a robot, delete all the modules in
the text box. To add a robot, click 'Add' and type the name of the new robot.
Saving your changes requires one package, GitPython, which can be installed
automatically when you click Save (a dialog box will pop up if it is not
installed, and prompt you for an automatic install). After you click save, you
will need to enter your lab git credentials in the terminal from which you
launched the program. You will also need to enter your name and email. Please
note that you can only update a single robot at a time, so if you click on
another robot in the left field, your current changes will be deleted. 

If something goes wrong, and everything is not working as expected, please send
me an email describing the problem at

    wjp@andrew.cmu.edu

You can always delete the repo and re-clone it to fix most problems.


## Please do not manually commit or push any changes to the repo, only make changes with the provided scripts!
