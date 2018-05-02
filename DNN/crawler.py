#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>

import requests
import json
from pprint import pprint

def get_game_list(year = 2018,month = 3):
    url = "http://api.best.gg/v1/schedule/list"

    querystring = {":acceptLanguage":"zh-cn","leagues":"","year":year,"month":month}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "c0b59334-2f3e-5391-78d4-a1f0affebfb0"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    '''
    Response.text's Structure :
        - code : 200(success)
        - content
            - type : json(type of this response)
            - body
                - matches
                    [ list of matches ]
                        - id
                        - status
                        - league
                        - scheduled_at
                        - teams
    '''

    text = json.loads(response.text)

    game_list = []

    if text['code'] == 200:
        for match in text['content']['body']['matches']:
            game_id, game_league, game_schedule, game_teamA, game_teamB, game_scoreA, game_scoreB = \
                match['id'], match['league'], match['scheduled_at'], match['teams'][0]['team'], \
                match['teams'][1]['team'], match['teams'][0]['score'], match['teams'][1]['score']

            game_dict = {'id':game_id,'league':game_league,'schedule':game_schedule,'teamA':game_teamA, \
                'teamB':game_teamB,'scoreA':game_scoreA,'scoreB':game_scoreB}

            game_list.append(game_dict)
        return game_list

    else:
        return False

def 