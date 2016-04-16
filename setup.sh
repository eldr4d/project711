#!/bin/bash

bashrc=$HOME"/.bashrc"
line1="export WORKON_HOME=$HOME/.virtualenvs"
line2="export CMSC_HOME=$WORKON_HOME/cmsc711project"
line3="source /usr/local/bin/virtualenvwrapper.sh"
echo $line1 >> $bashrc
echo $line2 >> $bashrc
echo $line3 >> $bashrc

$line1
$line2
$line3

source /usr/local/bin/virtualenvwrapper.sh

source $bashrc

mkvirtualenv cmsc711project

workon cmsc711project

pip install -r requirements.txt

deactivate
