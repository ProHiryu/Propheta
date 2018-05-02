#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>

import requests
import json
from pprint import pprint

def get_game_id(year = 2018,month = 3):
    url = "http://api.best.gg/v1/schedule/list"

    querystring = {":acceptLanguage":"zh-cn","leagues":"","year":year,"month":month}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "c0b59334-2f3e-5391-78d4-a1f0affebfb0"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    text = json.loads(response.text)



    pprint(text)

get_game_id()