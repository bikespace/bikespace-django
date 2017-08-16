# Toronto Bike Parking Project


## Local Development

To use this project, follow these steps:

1. Clone this repo
2. Create a virtualenv in the project root folder
3. Install requirements
4. Have a local instance of postgres running
5. Code away

### Virtualenv

Strongly suggest on using virtualenv for local development.

**Install virtualenv if not installed using**

```bash
pip install virtualenv
````

**Use python3 for the virtualenv**
```bash
virtualenv -p python3 venv
```

**Start the virtualenv**

```bash
source venv/bin/activate
```

### Install requirements

Install the requirements from the supplied `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Have a postgres instance running

Download your OS specific postgres package running on the default 5432 port from their download [page](https://www.postgresql.org/download/)

For mac OSX the easiest method is to download the [Postgres app](http://postgresapp.com/)

### Start the Django Application

Once all the above steps are complete test by running the django app.

**Run migrations to apply the models defined into the database**

Run this migrate whenever the models.py for the app has been changed so the
changes can be applied to the databases.

```bash
python manage.py migrate
```

**Run the django app**

```bash
python manage.py runserver
```

**Create a superuser for admin**

```bash
python manage.py createsuperuser
```

## Project Structure

This the current project structure
```
.
├── addDataToPostgres.py
├── bicycleparking
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── static
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── Bicycle_parking
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── static
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── LICENSE
├── manage.py
├── Procfile
├── README.md
├── README.rst
├── requirements.txt
├── runtime.txt
├── settingUpPostgres.md
```

`Bicycle_parking` is the main Django Project folder.

`bicycleparking` is one of the apps for the project.

## Client Side

```
cd bicycleparking
npm install
rollup -c -w
```

## Pushing changes

Please checkout out a new branch when working on the project and submit merge requests
for the proposed changes to the master branch.



## License: MIT
