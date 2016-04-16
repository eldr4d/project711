# project711
In this project we will analyze the king latency dataset for determining close proximity servers.

## Installation
Create a directory `./Data/`

Download the measurements.gz file from [here](https://pdos.csail.mit.edu/archive/p2psim/kingdata/) into the newly created `./Data/` directory
Extract the measurements file in the `./Data/` directory, and rename it `measurements`.
Now install pip
```
sudo apt-get install pip
```
Now install virtualenv
```
pip install virtualenv
```
Now get virtualenvwrapper (so we can maintain where the venv is created)
```
pip install virtualenvwrapper
```
Now run the setup.sh script (you may need to modify the permissions using `chmod +777 setup.sh`)
```
./setup.sh
```

Now, whenever you want to execute a python script, first load up the virtual environment by typing
```
workon cmsc711project
```
You can now call python on whatever you want, i.e.
```
python myfile.py
```

Exit the virtual environment with
```
deactivate
```
At this point, you should be able to execute the following without any errors:
```
./test/test.sh
```
Now you should see the first line of the measurements file printed to the console.
