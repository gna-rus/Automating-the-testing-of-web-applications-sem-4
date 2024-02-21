import functools

import pytest
from Task1_sem4 import Site
import yaml
import json
import requests

with open('testdata.yaml') as f:
    testdata = yaml.safe_load(f)


@pytest.fixture
def path_login():
    x_selector1 = "//*[@id='login']/div[1]/label/input"
    # input1 = site.find_element("xpath", x_selector1)
    # input1.send_keys("test")
    return x_selector1

@pytest.fixture
def path_passwd():
    x_selector2 = "//*[@id='login']/div[2]/label/input"
    # input2 = site.find_element("xpath", x_selector2)
    # input2.send_keys("test")
    return x_selector2

@pytest.fixture
def button():
    btn_selector = "button"
    # btn = site.find_element("css", btn_selector)
    # btn.click()
    return btn_selector

@pytest.fixture
def element():
    x_selector3 = """//*[@id="app"]/main/div/div/div[2]/h2"""
    return x_selector3


@pytest.fixture(scope="session")
def site_connect():
    site_instance = Site(testdata["browser"],testdata['addres'])
    yield site_instance
    site_instance.close()

@pytest.fixture
def result():
    return "401"
