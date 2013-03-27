Requirements
============

* Django 1.4
* django-celery
* django-registration
* sqlite3
* rabbitmq-server 

Installation
============

1. Configure RabbitMQ

        sudo rabbitmqctl add_user biomembrane
        sudo rabbitmqctl add_vhost biomembrane
        sudo rabbitmqctl set_permissions -p biomembrane biomembrane ".*" ".*" ".*"

2. Create the sqlite database at web/biomembrane.db (modify web/settings.py to change location)

        python manage.py syncdb

Running
=======

1. Start the Celery worker process

        python manage.py celery worker --loglevel=info

2. Run the development server on localhost:8000

        python manage.py runserver
