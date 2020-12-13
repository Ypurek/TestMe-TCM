source simpleenv/bin/activate
py simple/manage.py migrate
py simple/manage.py test
systemctl restart gunicorn