Requirements
============

* Django 1.4.3+
* django-celery
* sqlite3
* rabbitmq-server 

Installation
============

1. Configure RabbitMQ

        sudo rabbitmqctl add_user biomembrane
        sudo rabbitmqctl add_vhost biomembrane
        sudo set_permissions -p biomembrane biomembrane ".*" ".*" ".*"

2. Create the sqlite database at /tmp/biomembrane.db (modify web/settings.py to change location)

        python manage.py syncdb

Running
=======

1. Run the development server on localhost:8000

        python manage.py runserver
