Requirements
============

* Django 1.4
* django-celery
* django-registration
* sqlite3
* matplotlib
* pil
* numpy
* rabbitmq-server 
* ImageMagick
* PythonMagick

Installation
============

1. Configure RabbitMQ (modify web/settings.py with credentials)

        sudo rabbitmqctl add_user <user> <password>
        sudo rabbitmqctl add_vhost <vhost>
        sudo rabbitmqctl set_permissions -p <vhost> <user> ".*" ".*" ".*"
        
Dev Settings

        sudo rabbitmqctl add_user ics_user ics_password
        sudo rabbitmqctl add_vhost ics_vhost
        sudo rabbitmqctl set_permissions -p ics_vhost ics_user ".*" ".*" ".*"


2. Create the sqlite database at web/biomembrane.db (modify web/settings.py to change location)

        python manage.py syncdb

Running
=======

1. Start the Celery worker process

        python manage.py celery worker --loglevel=info

2. Run the development server on localhost:8000

        python manage.py runserver
