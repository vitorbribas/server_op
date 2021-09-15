FROM python:3

RUN apt update && apt install -y \
  netcat \
  postgresql-client \
  git

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

# Start the main process.
EXPOSE 8000
ENTRYPOINT ["bash", "entrypoint.sh"]