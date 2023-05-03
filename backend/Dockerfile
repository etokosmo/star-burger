FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code/
COPY requirements.txt /code/
RUN export DEBIAN_FRONTEND=noninteractive \
    && export DEBCONF_NOWARNINGS=yes \
    && apt-get update \
    && pip3 install --disable-pip-version-check -r requirements.txt \
    && apt-get autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list
COPY . /code/
EXPOSE 8080
VOLUME ["/media"]