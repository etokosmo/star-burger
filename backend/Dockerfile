FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code/
COPY requirements.txt /code/
RUN pip3 install --disable-pip-version-check -r requirements.txt \
COPY . /code/
EXPOSE 8080
VOLUME ["/media"]