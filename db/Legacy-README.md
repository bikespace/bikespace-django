#### Dependencies

**For Windows/Linux**

Unfortunately this setup for windows has only been tested using the Ubuntu for Windows (WSL) which provides a bash terminal for Windows.

_WSL Installation_: [https://docs.microsoft.com/en-us/windows/wsl/install-win10](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

__Expose Docker and docker-compose on your WSL terminal (Windows only):__

Since WSL exposes access to both the Windows and Linux kernels you can use the docker installation on your Windows volume in the bash terminal.
Just have to add some lines your `.bashrc` file in your home directory.
Open your terminal for WSL, and using your favourite text editor add these lines to your `.bashrc`

```shell
export PATH="$HOME/bin:$HOME/.local/bin:$PATH"
export PATH="$PATH:/mnt/c/Program\ Files/Docker/Docker/resources/bin"
alias docker=docker.exe
alias docker-compose=docker-compose.exe
```

Reopen a new terminal window to make the changes in effect.

__Install postgres and postgis CLI (Windows and Linux):__

```shell

# Install postgres package
sudo apt-get install update
sudo apt-get install postgresql postgresql-contrib

# Install postgis package

sudo apt-get install postgis
```

**For mac OSX**

For mac OSX the easiest method is to download the [Postgres app](http://postgresapp.com/).
There are other methods to install from source but this is the easiest method available.


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
