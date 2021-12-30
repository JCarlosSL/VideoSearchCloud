FROM python:3.9.6-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8001

#ENTRYPOINT ["sh", "/entrypoint.sh"]

ENTRYPOINT ["python","manage.py","runserver","0.0.0.0:8001"]
