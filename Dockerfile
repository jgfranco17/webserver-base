FROM python:3.10.6-alpine
WORKDIR /root
COPY . .
RUN mkdir -p /root/.config/pyxelbyte
RUN ls
RUN pip install .
CMD ["webserver-base"]