#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>

import requests

url = "http://api.best.gg/v1/live/match/lol/17972"

querystring = {":acceptLanguage":"zh-cn"}

headers = {
    'cache-control': "no-cache",
    'postman-token': "81c9d8b5-57fc-50ee-35a3-b85da9cb1e0c"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)