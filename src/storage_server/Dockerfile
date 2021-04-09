FROM python:3.8

COPY requirements.txt .

RUN pip install -r requirements.txt
# --user makes pip install packages in your home directory instead, which doesn't require any special privileges.
WORKDIR /code

COPY . .

CMD ["python", "./storage_server.py"]
# could add -u option to force stdin, stdout and stderr to be unbuffered