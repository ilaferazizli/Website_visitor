FROM alpine
USER root
LABEL org.opencontainers.image.authors="Zynt, Ilafer"
RUN apk add --no-cache chromium chromium-chromedriver python3 py3-pip
RUN python3 -m venv /data
RUN /data/bin/pip3 install selenium bs4 requests
RUN rm -rf /root/.cache
COPY main.sh /data
COPY oto_webpage.py /data
COPY crontab /etc/crontabs/root
RUN chmod +x /etc/crontabs/root
RUN chmod +x /data/main.sh
ENTRYPOINT /data/main.sh