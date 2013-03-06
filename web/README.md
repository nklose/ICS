Installation
============

1. Install Django 1.4.3
2. Install sqlite3
3. Install rabbitmq-server

    sudo rabbitmqctl add_user biomembrane
    sudo rabbitmqctl add_vhost biomembrane
    sudo set_permissions -p biomembrane biomembrane ".*" ".*" ".*"

4. Create the sqlite database at /tmp/biomembrane.db (modify web/settings.py to change location)

    python manage.py syncdb

Running
=======

1. Run the development server on localhost:8000

    python manage.py runserver
