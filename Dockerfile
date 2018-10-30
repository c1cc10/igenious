from python:3.6.2

WORKDIR /app

#ADD . /app
COPY . /app

EXPOSE 8888

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "xchange.py"]
