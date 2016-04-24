# project711
In this project we will analyze the king latency dataset for determining close proximity servers.

## Installation
Create a directory `./Data/`

Download the measurements.gz file from [here](https://pdos.csail.mit.edu/archive/p2psim/kingdata/) into the newly created `./Data/` directory
Extract the measurements file in the `./Data/` directory, and rename it `measurements`.

Now, create a postgreSQL database with the name `cmsc711` and password `cmsc711`
```
createuser -U postgres -d -P cmsc711
```
Now create a database under that user
```
createdb -U cmsc711 -O cmsc711 king
```
If you get an error about peer authentication failure, go here [here](http://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge).

While youre at it, get psycopg2 to serve as the interface from python to the database

```
sudo apt-get install python-psycopg2
```

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

Time to import the data from the measurements file to the database. 
```
workon cmsc711project
cd ./src
python createDB.py
```
This will take some time because it creates a table `Measurements` and then parses each line from the measurements file into this new table.
Currently, the limit in the `createDB.py` file is the first 100000 lines in the measurements file (there are about 97 million lines total)


Collect locations for each ip

First install the following external library [ipinfodb](http://http://ipinfodb.com/)
pip install git+git://github.com/markmossberg/pyipinfodb.git

You can use this API key but it will be better if you create an acount and generate a new one.
API key 7bc84207e8b13e67b546b6857459aa263ffc5ce7fd9ca12af653de66015ca988

In order to find the distance between two locations we use the [geopy](https://pypi.python.org/pypi/geopy) library.

Load the locations table:

```psql -f locations.sql king```


