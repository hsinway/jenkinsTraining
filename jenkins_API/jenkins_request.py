import json

import requests


def test_jenkins_1():
    """
    启动一次任务
    :return:
    """
    url = "http://admin:admin@127.0.0.1:8080/job/demo_a/build"
    res = requests.post(url=url)
    print(res.text)


def test_jenkins_2():
    """
    查询jenkins任务最近一次build number
    :return:
    """
    url = "http://admin:admin@127.0.0.1:8080/job/demo_a/lastBuild/buildNumber"
    res = requests.get(url=url)
    print(res.text)


def test_jenkins_3():
    """
    查询jenkins任务状态
    :return:
    """
    url = "http://admin:admin@127.0.0.1:8080/job/demo_a/7/api/json"
    res = requests.get(url=url)
    print(json.dumps(res.json(), indent=2))
