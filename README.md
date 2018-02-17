[![pipeline status](https://gitlab.com/bikespace/Bicycle-parking/badges/master/pipeline.svg)](https://gitlab.com/bikespace/Bicycle-parking/commits/master)

[![coverage report](https://gitlab.com/bikespace/Bicycle-parking/badges/master/coverage.svg)](https://gitlab.com/bikespace/Bicycle-parking/commits/master)

# Toronto Bike Parking Project

Note: This is a debugging branch and should NOT be merged with the master until and unless the code is updated and stable.

## Local Development

To use this project, we will work though the following steps:

1. Install requirements
2. Clone this repo
3. Create a `virtualenv` in the project root folder
4. Have a local instance of `postgres` running
5. Install ngrok
6. Code away

We strongly suggest on using `virtualenv` for python development

#### Next we Install python3 on your computer

On mac osx

```shell
# On Mac OSX we suggest homebrew, also known as brew
# please visit https://brew.sh/
# follow the on-screen instructions of the website

# hopefully homebrew is installed
# let us now use brew to install python3
brew install python3
```

On windows

```shell
# On windows we suggest chocolatey, also known as choco
# please visit https://chocolatey.org/
# follow the on-screen instructions of the website

# hopefully homebrew is installed
# let us now use choco to install python3
choco install python --version 3.6.3
```

##### Next we get the projects code setup to run

We now will setup an environment to run the python code of
the [https://gitlab.com/bikespace/Bicycle-parking](https://gitlab.com/bikespace/Bicycle-parking) project setup on your computer

```shell
pip3 install virtualenv

# get the repository of code on your machine and change to the directory
git clone git@gitlab.com:bikespace/Bicycle-parking.git civictechto-bicycle-parking

# change to the directory
cd civictechto-bicycle-parking

# setup a virtualenv for python3
virtualenv -p python3 venv
# note "venv" is now the name of the directory containing the python virtualenv

# Use the "venv" you setup earlier for your python3 project buy running the activate script
source venv/bin/activate

# Install requirements
# Install the requirements from the supplied `requirements.txt`.
pip3 install -r requirements.txt
```

### Have a postgres instance running

For mac OSX the easiest method is to download the [Postgres app](http://postgresapp.com/)

For other OS specific postgres packages running on the default 5432 port
Please visit the [postgres download page](https://www.postgresql.org/download/)

Create a database in postgres with the name ```bike_parking_toronto```.
The database needs the postgres user to have the password ```postgres```.

In Linux:
```
$ sudo su - postgres
$ psql
$ CREATE DATABASE bike_parking_toronto;
### The postgres user is going to already
### BUT we need to safely set that user's password
$ \password postgres
Enter new password: postgres
Enter it again: postgres
$ GRANT ALL PRIVILEGES ON DATABASE bike_parking_toronto to postgres;
```

The PostGIS package needs to be installed and the extension enabled.

Assuming postgresql version 9.6 and Linux:
```
$ sudo apt-get install postgresql-9.6-postgis-2.3 postgis
$ sudo su - postgres
$ psql
$ \connect bike_parking_toronto
$ CREATE EXTENSION postgis;
```

Create an intersection database and a test intersection database using the geographic database script:
in linux or OSX, type:

```shell
./mkintersectiondb
```

The script will ask for the password a few times, enter ```postgres``` which we set up earlier.

On linux distros, your postgresql installation must permit access from the local host using the
default postgres database userid. If you get an access denied error from `mkintersectiondb`, 
on Ubuntu do the following:

```shell
sudo ufw enable
sudo nano /etc/postgresql/9.6/main/pg_hba.conf 
```

find the line with
```shell
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5 (or any value but "trust')

```

replace the last column with the word trust as follows:

```shell
host    all             all             127.0.0.1/32            trust
```

### Install ngrok

ngrok is needed to serve the local django application over ssl.
To install ngrok, use [npm](https://www.npmjs.com/get-npm).

Install ngrok globally:

We can use npm or yarn.

### With npm:
```shell
which npm
npm install ngrok -g
```
### Build client side js

We are using rollup to bundle the js for the client side. To compile `cd` into the `bicycleparking` and run :

```shell
npm build
```

For hot-reloading setup a watcher:

```shell
rollup -c -w
```

### With yarn:
### Installing yarn and ngrok on Linux:
```
$ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
$ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
$ sudo apt-get update && sudo apt-get install yarn
$ sudo yarn global add ngrok
```

### Build client side js
In the main project directory:
```
$ yarn postinstall
```

For hot-reloading:
In the ```bicycleparking``` directory
```
$ yarn run watch
```

### Start the Django Application

Once all the above steps are complete test by running the django app.

**Run migrations to apply the models defined into the database**

Run this migrate whenever the models.py for the app has been changed so the
changes can be applied to the databases.

```shell
# First we run the migrations for the database
python manage.py migrate

# Let us first create a superuser for the admin web page
python manage.py createsuperuser

# Now we can run the django web app
python manage.py runserver

# Now run ngrok to serve over https
# ngrok http [please_insert_port_django_is_running_on]
# for example
ngrok http 3000
```

## Contributing

See our [contributing guidelines](https://gitlab.com/bikespace/Bicycle-parking/blob/readmeContributing/CONTRIBUTING.md)

## Project Structure

This is the current project structure, please note:

- the `Bicycle_parking` is the main Django Project folder
- the `bicycleparking` dir is one of the apps for the project

```
├── bicycleparking
│   ├── admin.py
│   ├── apps.py
│   ├── geocode.py
│   ├── __init__.py
│   ├── intersection.py
│   ├── migrations
│   ├── models.py
│   ├── node_modules
│   ├── package.json
│   ├── __pycache__
│   ├── rollup.config.js
│   ├── Routers.py
│   ├── serializers.py
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── uploader.py
│   ├── urls.py
│   └── views.py
├── Bicycle_parking
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings
│   ├── static
│   ├── urls.py
│   └── wsgi.py
├── CONTRIBUTING.md
├── db.sqlite3
├── docker-compose.yml
├── HTML_CSS
│   ├── background_images
│   ├── files_old
│   ├── flatpickr.css
│   ├── happening.html
│   ├── icons
│   ├── index.html
│   ├── issue.html
│   ├── map.html
│   ├── mobilesheet.css
│   ├── Open_Sans
│   ├── picture.html
│   ├── stylesheet2.css
│   ├── stylesheet.css
│   ├── success.html
│   └── summary.html
├── LICENSE
├── manage.py
├── mkaddressdb
├── mkintersectiondb
├── node_modules
│   ├── flatpickr
│   ├── leaflet
│   └── leaflet-search
├── package.json
├── package-lock.json
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
├── sql
│   ├── intersec2d.sql
│   ├── intersection_types.sql
│   ├── makegisdb.sql
│   └── visit_address.sql
├── test
│   ├── areas.xml
│   ├── geodata_001.xml
│   ├── intersection_test.cpg
│   ├── intersection_test.dbf
│   ├── intersection_test.prj
│   ├── intersection_test.shp
│   ├── intersection_test.shx
│   ├── makeAreas.py
│   ├── removeTestDB.py
│   ├── test_data.sql
│   ├── useaws
│   └── useci
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── pip-selfcheck.json
    └── share
```

## License: MIT

please see the `LICENSE` file
generated using https://choosealicense.com/licenses/mit/
