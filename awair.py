#!/usr/bin/env python
from prometheus_client import start_http_server, Gauge, Summary, Counter
import time
import argparse
import json
import requests
RESPONSE_CODE = Counter('awair_reponse_code',
                        'HTTP Response Codes', ['http_code'])
FAILURE_COUNT = Counter('awair_failure_count',
                        'AWAIR API FAILURES', ['method'])
AWAIR_SCORE = Gauge("awair_device_score", "Awair score of device", ['device'])
AWAIR_TEMP = Gauge("awair_device_temp", "Awair temp of device", ['device'])
AWAIR_HUMID = Gauge("awair_device_humid",
                    "Awair humidity of device", ['device'])
AWAIR_CO2 = Gauge("awair_device_co2", "Awair co2 level of device", ['device'])
AWAIR_VOC = Gauge("awair_device_voc", "Awair voc of device", ['device'])
AWAIR_PM25 = Gauge("awair_device_pm25", "Awair pm25 of device", ['device'])
AWAIR_DEW =  Gauge("awair_device_dew", "Awair dew point", ['device'])


def produce_data(ip, name):
    resp = requests.get("http://" + ip + "/air-data/latest")
    r = json.loads(resp.text)
    AWAIR_SCORE.labels(name).set(r['score'])
    AWAIR_PM25.labels(name).set(r['pm25'])
    AWAIR_VOC.labels(name).set(r['voc'])
    AWAIR_HUMID.labels(name).set(r['humid'])
    AWAIR_CO2.labels(name).set(r['co2'])
    AWAIR_TEMP.labels(name).set(r['temp'])
    AWAIR_DEW.labels(name).set(r['dew_point'])

def parse_config(config_path):
    # config is in {'IP_ADDRESS': "ALIAS"} format
    with open(config_path, "r") as f:
        config = json.load(f)
    return config

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help='Path to config', required=True)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--interval", type=int, default=3)
    args = parser.parse_args()
    cfg = parse_config(args.config)
    start_http_server(args.port)
    print(cfg)
    while True:
        for ip, name in cfg.items():
            produce_data(ip, name)
        time.sleep(args.interval)
