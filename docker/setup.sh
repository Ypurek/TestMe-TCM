# assumed project copied into docker home dir and home dir opened /home/simpleuser

#create user TODO
adduser simpleuser --create-home simpleuser


alias py=python3
alias pip=pip3

py virtualenv simpleenv
source simpleenv/bin/activate
pip install django gunicorn psycopg2-binary

py simple/manage.py makemigrations --noinput
py simple/manage.py migrate --noinput
# create default superuser admin:admin
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'test@email.com', 'admin')" | py manage.py shell

py simple/manage.py collectstatic --noinput

cp simple/docker/gunicorn.socket /etc/systemd/system/gunicorn.socket
cp simple/docker/gunicorn.service /etc/systemd/system/gunicorn.service

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

cp simple/docker/simple-nginx.cfg /etc/nginx/sites-available/simple-nginx.cfg
sudo ln -s /etc/nginx/sites-available/simple-nginx.cfg /etc/nginx/sites-enabled

sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'