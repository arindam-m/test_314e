# Web Scrapper

Scrape through number of web pages from the root index and traverse through all the hyperlinks for a given depth level.

*PS: Current this project is being hosted on [Heroku](https://test-314e.herokuapp.com/) platform, as a means of PoC.*

<br/>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

See deployment for notes on how to deploy the project on a live system.

<br/>

### <ins>Prerequisites

[Python 3.7.x](https://www.python.org/downloads/) (or any of the latest stable) is required.

After cloning and moving into the directory, set up the vitural environment

```bash
$ git clone https://github.com/arindam-m/test_314e.git
$ cd test_314e/

$ python -m venv _env
$ source _env/bin/activate # _evn/Scripts/activate on Windows

```

### <ins>Installing

All the other dependencies can be install through pip and requirements.txt file provided.

```bash
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
$ pip list
```
Also, making these changes to the settings.py file in the 'project_main' directory.
```python
ALLOWED_HOSTS = ["localhost",]
```

Finally, we start the Django server

```bash
$ python manage.py runserver
```

When the developement server is successfully booted up, you get to see that it's being hosted on a localhost @ port: 8000

```python
Django version 3.1.3, using settings 'project_main.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
<br/>

---

## Deployment

When this project need to be deployed on a remote production server, we would have to do the following additional checks.

```bash
$ python manage.py check --deploy
```

We need to update ALLOWED_HOST in the settings with the url of the remote server's web-address.

```python
ALLOWED_HOSTS = ["localhost", "..."]
```

Finally, get [NGINX](https://www.nginx.com/) and [Gunicorn](https://gunicorn.org/) installed as the main web-server and WSGI http-server respectively

```bash
$ pip3 install gunicorn
$ sudo apt-get install nginx -y
$ pip install psycopg2-binary
```
And then repeat the above process to start the Django server.

<br/>

---

## Built With

* [Django](https://www.djangoproject.com/) - Python Web-framework
* [Requests](https://requests.readthedocs.io/en/master/) - HTTP library for Python
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Web scraper