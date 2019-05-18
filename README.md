# The Web Application
Shorten and save your links

## Usage

After login, the user enters the dashboard. The dashboard has two sections: *form* for submitting links and history *table*. A user inserts the link and clicks 'Submit'. The form data immediately runs through the server and returns the output. Finally, a new row entry with _tiny link_ appears in the history table.

Any user with permission to view the 'Link' table can access a page with statistics `/statistics`. This page contains numbers of redirects for each link ever created. 

Hosted on http://reasongrace.com/

# Features
* User account
* Link history
* Single page view
* Small alphabetical _tinylinks_
* View statistics (_permission required_)

# Debugging

To debug the application I use Visual Studio Code.

## Setting up Virtual Environment
To begin with, we need to have `virtualenv` installed. Creating a virtual environment

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

After that, we need to register the new application in `settings.py`.

To make models accessible in admin panel we need to register them in `admin.py`. Remember to *make migrations*, *migrate*, and create _superuser_ in Django to access admin panel

```
$ ./manage.py createsuperuser
```

Automatically create user database. Enter shell

```
$ ./manage.py shell
>>> from tinylink.extras import make_users
>>> make_users()
```

Alternatively, to restore the tables form dump I use the makefile

```
$ make restore
```

# Deploying

The first step is to archive the `site` folder

    $ tar -cvf site.tar site

Send it to the server and unarchive

    $ tar xopf site.tar

Not to forget adding a secret key variable to `secret_key.py`.

I created the makefile to *unfold* the project on a server

    $ make start

The project is deployed on a server.

Now, all the updates are being made using

    $ git pull

# Backing up the database

The simple script is embedded in the makefile

    $ make backup
    
To manually backup a table

    $ ./manage.py dumpdata tinylink.Link --indent 4 > tinylink/fixtures/links.json

# Credits

https://docs.djangoproject.com/en/dev/

http://djangogirls.org/

<!-- 
## Known issues

1. Login page reloads to `/login/login` when a password is incorrect
2. Sometimes '403 missing csrf token' arises
 -->
