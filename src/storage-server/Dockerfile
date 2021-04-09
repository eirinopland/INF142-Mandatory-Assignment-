FROM python:3.8

COPY requirements.txt requirements.txt
# or "COPY requirements.txt ."?

RUN pip install --user -r requirements.txt
# --user makes pip install packages in your home directory instead, which doesn't require any special privileges.

# alternatively "RUN pip install --no-cache-dir -r requirements.txt"?
# if we want to keep a Docker image as small as possible, and cache should generally not be needed in a Docker image

# WORKDIR?

COPY . .

# ENV?

CMD ["python", "./storage-server.py"]
# could add -u option to force stdin, stdout and stderr to be unbuffered