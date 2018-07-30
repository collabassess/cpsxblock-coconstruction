FROM library/python:2.7.15-jessie

ENV SHORTNAME=constructcpsxblock

RUN apt-get install -y \
        libxslt-dev \
        libxml2-dev 

WORKDIR /usr/local/var/xblock
COPY . .

RUN ls .
RUN pip install -r ./xblock-sdk/requirements/base.txt \
    && pip install -e $SHORTNAME

WORKDIR /usr/local/var/xblock/xblock-sdk
RUN mkdir -p var \
    && touch var/workbench.log \
    && make install \
    && python manage.py migrate --no-input

EXPOSE 8000
ENTRYPOINT [ "python", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]