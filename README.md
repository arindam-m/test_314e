# Web Scrapper

Scrape through number of web pages from the root index (home page) of a given url and traverse through all the hyperlinks for a given depth level, and display the number of a particular word and a word-pair has appread.

<br/>

<b>|</b> *Currently, this project is live on [Heroku](https://test-314e.herokuapp.com/)*

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
We need to set the SECRET_KEY of our Django project and AWS S3 bucket respectively, in our local OS as a environment variable.

```python
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ACCESS_KEY = os.environ.get('S3_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY')
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

When this project need to be deployed on a remote production server*, we would have to do the following additional checks.

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


> This remote production server generally refers to a Linux machine running on AWS/Linode or something similar.

>As of now, it's already hosted on [Heroku](https://test-314e.herokuapp.com/) cloud. Though Heroku is meant to be used as a PaaS for Proof of Concept, a <b>Procfile</b> is available in this repo which automatically connects to a web-server through Gunicorn WSGI. 

---

## Built With

* [Django](https://www.djangoproject.com/) - Full stack web-framework
* [Scrappy](https://scrapy.org/) - A web-framework for extracting data
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - A parser for web scrapping