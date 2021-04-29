FROM tiangolo/meinheld-gunicorn-flask:python3.8

RUN apt-get update
RUN apt-get -y install ipmitool
RUN pip install flask-wtf
RUN pip install wtforms
RUN pip install flask-bootstrap4

COPY ./app /app