#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>


import requests
import json
from pprint import pprint

def get_game_list(year = 2018,month = 3):
    url = "http://api.best.gg/v1/schedule/list"

    querystring = {":acceptLanguage":"en-us","leagues":"","year":year,"month":month}

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

    '''
    game_list's Structure :
        [ list of games ]
            - id
            - league
            - schedule
            - teamA
            - teamB
            - scoreA
            - scoreB
    '''

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



def get_game_details(match_num = 17972):
    url = "http://api.best.gg/v1/live/match/lol/" + str(match_num)

    querystring = {":acceptLanguage":"en-us"}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "dd3c07fe-8776-58ba-7c35-c5d526a90752"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    '''
    Response.text's Structure :
        - code : 200( success )
        - content
            - type : json ( type of this response )
            - body
                - streams
                - live_match
                - match
                    - league
                    - title
                    - type
                    - teams
                    - scheduled_at
                    - preview
                - sets
                    [ list of sets ]
                        - id
                        - title
                        - number
                        - videos
                        - participants_teams
                            [ list of participants_teams ( 2 ) ]
                                - is_win
                                - kills
                                - assists
                                - deaths
                                - slug
                                - name
                                - image_url
                                - players
                                    [ list of players ( 5 ) ]
                                        - id
                                        - name
                                        - kills
                                        - deaths
                                        - assists
                                        - champion
                                            - _version
                                            - _id
                                            - title
                                            - tooltip_string
                                            - image_url
    '''

    text = json.loads(response.text)

    '''
    set_list's Structure :
        [ list of sets ]
            - id
            - number
            - participants_teams
                [ list of participants_teams ( 2 ) ]
                    - is_win
                    - kills
                    - assists
                    - deaths
                    - slug
                    - name
                    - players
                        [ list of players ( 5 ) ]
                            - id
                            - name
                            - kills
                            - deaths
                            - assists
                            - title
            - version
    '''

    set_list = []

    if text['code'] == 200:
        for set_ in text['content']['body']['sets']:
            version = set_['participants_teams'][0]['players'][0]['champion']['_version']
            del set_['videos']
            for participants_team in set_['participants_teams']:
                del participants_team['image_url']
                for player in participants_team['players']:
                    player['title'] = player['champion']['title']
                    del player['champion']
            set_['version'] = version

            set_list.append(set_)
        return set_list

    else:
        return False
