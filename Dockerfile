FROM python:3.10

WORKDIR /
RUN pip install pipenv

RUN git clone https://github.com/Juanipis/RDS-AWS-Taller-SO.git

WORKDIR /RDS-AWS-Taller-SO
RUN pipenv install

RUN pipenv install psycopg2-binary


EXPOSE 80

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]