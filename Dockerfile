FROM python:3.9-slim
RUN mkdir /app
WORKDIR /app
ADD . /app

RUN \
 apt-get update && \
 apt-get install -y libpq-dev gcc postgresql-client && \
 pip install --upgrade pip && \
 pip install psycopg2~=2.8 && \
 pip install gunicorn && \
 chmod +x /app/init_database.sh && \
 python3 -m pip install -r requirements.txt && \
 apt-get clean && apt-get autoremove -y gcc