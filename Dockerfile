FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm requirements.txt
COPY src/*.py ./

VOLUME /data
COPY input.txt /data/input.txt

USER user

RUN python CardMarketTrendFinder.py --input_file /data/input.txt --output_file /data/output.csv --debug_mode False

