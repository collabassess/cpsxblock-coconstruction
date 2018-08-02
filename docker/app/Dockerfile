FROM cpsxblock/sdkenv

ENV SHORTNAME=constructcpsxblock

WORKDIR /usr/local/var/xblock
COPY . .

RUN pip install -e $SHORTNAME

WORKDIR /usr/local/var/xblock/xblock-sdk
RUN python manage.py migrate --no-input

EXPOSE 8000
ENTRYPOINT [ "python", "manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]