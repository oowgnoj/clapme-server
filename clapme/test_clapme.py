#!/usr/bin/env python
# coding=utf8
# content of test_flask.py

import pytest
import json
import sys
sys.path.append(".")


from __init__ import app



@pytest.fixture
def client():
    client = app.test_client()

    yield client

def test_ApiGoal_post(client):
    test_data = {"title" :"hello clapme!!!", "description" : "playing!!", "interval" : "everyweek", "times" : 3, "thumbnail":"test-thumbnail"}
    rv = client.post('/goal/', data=json.dumps(test_data))
    json_data = rv.get_json()
    assert 200  == rv.status_code

def test_ApiGoal_get(client):

    rv = client.get('/goal/1', data=dict())
    json_data = rv.get_json()
    answer = {"id": 1, "description": "clapme", "interval": "everyweek", "times": 1}
    assert json_data == answer


def test_ApiGoal_patch_with_all_params(client):
    test_data = {"id" : 1, "title" :"test changed",'description': 'clapme','interval': 'everyweek', 'times': 1, 'thumbnail': None}
    rv = client.patch('/goal/', data=json.dumps(test_data))
    json_data = rv.get_json()
    answer = {'title': 'test changed', 'description': 'clapme', 'interval': 'everyweek', 'times': 1, 'thumbnail': None}
    assert json_data == answer


def test_ApiGoal_patch_with_some_params(client):
    test_data = {"id" : 1, "title" :"test changed2"}
    rv = client.patch('/goal/', data=json.dumps(test_data))
    json_data = rv.get_json()
    answer = {'title': 'test changed2', 'description': 'clapme', 'interval': 'everyweek', 'times': 1, 'thumbnail': None}
    assert json_data == answer


def test_ApiGoal_delte(client):
    test_data = {"id" : 1}
    rv = client.delete('/goal', data=json.dumps(test_data))

    assert 200 == rv.status_code