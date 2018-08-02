FROM library/python:2.7.15-jessie

RUN apt-get install -y \
        libxslt-dev \
        libxml2-dev 

WORKDIR /usr/local/var/xblock
COPY . .

RUN pip install -r ./xblock-sdk/requirements/base.txt

WORKDIR /usr/local/var/xblock/xblock-sdk
RUN mkdir -p var \
    && touch var/workbench.log \
    && make install \
    && python manage.py migrate --no-input