import json
from icmplib import ping
import requests
import ctypes
import struct
import urllib.request
import socket
import os
from faker import Faker
import logging

logger = logging.getLogger(__name__)


def cal_uptime(metric):
    libc = ctypes.CDLL('libc.so.6')
    buf = ctypes.create_string_buffer(4096)
    if libc.sysinfo(buf) != 0:
        print('failed')
        metric.set(-1)
        return

    uptime = struct.unpack_from('@l', buf.raw)[0]
    metric.set(uptime)
    return


def cal_restapi_availability(metric):
    REST_API_ADD_URL = os.environ.get("REST_API_ADD_URL")
    REST_API_DEL_URL = os.environ.get("REST_API_DEL_URL")

    fake = Faker(["fa"])
    phone_number = fake.msisdn()[:10]
    username = fake.user_name()

    test_phb_data = {
        "phoneNumber": phone_number,
        "username": username
    }

    try:
        resp = requests.post(
            url=REST_API_ADD_URL,
            data=json.dumps(test_phb_data),
            timeout=3,
            headers={"Content-Type": 'application/json'}
        )
        if resp.status_code != 200 and resp.status_code != 400:
            logger.error(f"restapi status code {resp.status_code}")
            metric.set(0)
            return
    except Exception as e:
        metric.set(0)
        logger.error(f"restapi exeption {e}")
        return

    try:
        resp = requests.delete(
            url=REST_API_DEL_URL,
            data=json.dumps(test_phb_data),
            timeout=3,
            headers={"Content-Type": 'application/json'}
        )
        if resp.status_code != 200:
            logger.error(f"status code {resp.status_code}")
            metric.set(0)
            return
    except Exception as e:
        metric.set(0)
        logger.error(f"restapi exeption {e}")
        return
    metric.set(1)


def cal_gateway_accessibility(metric):
    GATEWAY_IP = os.environ.get("GATEWAY_IP")
    res = ping(GATEWAY_IP, interval=0.5, privileged=True)
    metric.set(res.is_alive)


def cal_nginx_availability(metric):
    NGINX_ADDR = os.environ.get("NGINX_ADDR")
    res = urllib.request.urlopen(NGINX_ADDR)

    metric.set(res.status == 200)


def cal_internet_connection(metric):
    EXTERNAL_ADDR = os.environ.get("EXTERNAL_ADDR")
    res = urllib.request.urlopen(EXTERNAL_ADDR)

    metric.set(res.status == 200)


def cal_dns_check(metric):
    DNS_ADDR = os.environ.get("DNS_ADDR")
    DNS_IP = os.environ.get("DNS_IP")
    ip = socket.gethostbyname(DNS_ADDR)

    metric.set(ip == DNS_IP)
