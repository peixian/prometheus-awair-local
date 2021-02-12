FROM python:3
RUN pip install prometheus_client
RUN pip install argparse
RUN pip install requests
WORKDIR awair
ADD awair.py .
ADD config.json .
ENTRYPOINT [ "python", "-u", "awair.py", "-c", "config.json"]
