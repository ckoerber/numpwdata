# Database interface to nuclear density data

`numpwdata` is a Python [ORM](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) using [EspressoDB](https://espressodb.readthedocs.io/en/latest/) (and as such [Django](https://www.djangoproject.com/)) to store and interface information about nuclear wave functions and operators in a partial wave basis.

It allows you to search available data by keywords and read corresponding files into memory.

## Install

All the dependencies are `pip` installable

1. Clone [`numpwd`](https://git.noc.ruhr-uni-bochum.de/nuc/numpwd), checkout the `operator-math` branch and `pip install` it (needed for reading h5 files)
2. Run `pip install [--user] [-e] .` in this directory

## Setup

Next you have to setup the database.
This module generally supports all formats which support `JSON` fields.
For example, recent versions of `SQLITE` (file based) or `Postgres` (centralized database).

To setup the database, you have to create
* a `db-config.yaml` file either in the root directory of this repo, or
* create `db-config.yaml` in a directory of your choice and export the environment variable `export NUMPWDATA_CONFIG_DIR="..."` to this directory (this can be useful in case you have different dbs for different projects)

The DB config file specfies the access information to the database of your choice and should in almost all cases be treated sensitively.

An example file can be found in this repo under the name `db-config.yaml.example`.
To hook into another database, see also https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-DATABASES (the keywords are the same).

Once this is done, you can run
```bash
numpwdata info
```
to see if the information are accessed correctly.

To create or update the database, you have to run
```bash
numpwdata migrate
```
this will create or update the table definitions inside the database.
This only needs to run once--or if table definitions change.
After this, you are good to go.

## Using...
You can either use the browser interface to access the database, use an interactive shell or execute Python code which interfaces with the DB.

### ...the browser interface
First you need to create an superuser account to log in
```bash
numpwdata createsuperuser
```
and next you can launch a (local) web server accessible through web browser which is allowed to connect to this local port by running
```bash
numpwdata runserver [address:port]
```
In the upper right corner, you can login which enables access to the admin area which lets you connect to the data.

### ...interactive shell
Run
```bash
numpwdata shell
```

Note: you get a nicer shell if you also install `pip install ipython`.

### ...a python script

```python
# my_script.py
from numpwdata.densities.models import Density2N

all_densities = Density2N.objects.all()
db_dens = all_densities.filter(qval=0.0, thetaval=180.0, nucleus="4he", ...).first()

dens = db_dens.read_h5()
dens.matrix.shape == (n_channels, np, np)
dens.channels
```

See also the documentation page http://127.0.0.1:8000/documentation/densities/ (needs launching the web server) for the data structures and [the Django docs for making queries](https://docs.djangoproject.com/en/3.1/topics/db/queries/).
