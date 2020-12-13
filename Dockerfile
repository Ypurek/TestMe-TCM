FROM python:3.9.0-slim-buster

# install tools
RUN apt update && apt -y install vsftpd nginx postgresql
# install python tools
RUN pip install --upgrade pip
RUN pip --no-input install django django-database-view gunicorn psycopg2-binary virtualenv

WORKDIR /app
# copy project
COPY . /app

# put config files
RUN cp /app/docker/vsftpd.conf /etc/vsftpd.conf
# TODO

# run services // service vsftpd start &&
RUN service postgresql start

# prepare DB
RUN python /app/manage.py migrate

EXPOSE 20, 21, 8080, 5432

ENTRYPOINT python /app/manage.py runserver 8080
