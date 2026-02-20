FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED=1

WORKDIR /d05

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache \
    libffi-dev \
    build-base \
    postgresql-dev \
    postgresql-client \
    && pip install --upgrade pip \
    && pip install -r /requirements.txt

COPY ./d05 /d05

EXPOSE 8000

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]