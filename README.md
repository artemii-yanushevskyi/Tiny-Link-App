# The Web Application

# Debugging

To debug the application I use Visual Studio Code.

## Setting up Virtual Environment
To begin with, we need to have `virtualenv` installed. Creating virtual environment

```
$ python3 -m virtualenv env
$ # activating
$ # set python path
/Users/aware/Desktop/Tiny Link App/env/bin/python
$ source env/bin/activate
$ # start django project
$ django-admin startproject core
$ ./manage.py runserver
```

## Starting to develop

To create an application
```
$ ./manage.py startapp tinylink
```

After that we need to register the new application in `settings.py`.

To make models accessible in admin panel we need to register them in `admin.py`. Remember to *make migrations*, *migrate*, and create _superuser_ in django to access admin panel

```
$ ./manage.py createsuperuser
```

Automatically create user database. Enter shell

```
$ ./manage.py shell
>>> from tinylink.extras import make_users
>>> make_users()
```

Alternatively, to restore the tables form dump I use makefile

```
$ make restore
```

# Deploying

The first step is to archive `site` folder

    $ tar -cvf site.tar site

Send it to the server and unarchive

    $ tar xopf site.tar

Not to forget adding secret key variable to `secret_key.py`.

I created the makefile to *unfold* the project on a server

    $ make start

The project is deployed on a server.