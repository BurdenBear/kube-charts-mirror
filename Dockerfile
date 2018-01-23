FROM python:3-alpine

WORKDIR /root/

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./*.* ./

VOLUME ["/mnt/charts/]

ENTRYPOINT ["/root/update.sh"]
