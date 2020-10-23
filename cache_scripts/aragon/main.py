"""
   Descp: Main script to create Aragon datawarehouse, it call all the collectors.

   Created on: 15-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import os
import json
from typing import Dict, List, Callable

import aragon.collectors.organizations as organizations
import aragon.collectors.apps as apps
import aragon.collectors.mini_me_token as token
import aragon.collectors.token_holders as holders
import aragon.collectors.repo as repos
import aragon.collectors.vote as votes
import aragon.collectors.cast as casts
import aragon.collectors.transaction as transactions

DIRS: str = os.path.join('datawarehouse', 'aragon')
META_PATH: str = os.path.join(DIRS, 'meta.json')
KEYS: List[str] = [
    organizations.META_KEY,
    apps.META_KEY,
    token.META_KEY,
    holders.META_KEY,
    repos.META_KEY,
    votes.META_KEY,
    casts.META_KEY,
    transactions.META_KEY,
] # add here new keys
COLLECTORS: List[Callable] = [
    organizations.update_organizations,
    apps.update_apps,
    token.update_tokens,
    holders.update_holders,
    repos.update_repos,
    votes.update_votes,
    casts.update_casts,
    transactions.update_transactions,
] # add new collectors


def _fill_empty_keys(meta_data: Dict) -> Dict:
    meta_fill: Dict = meta_data

    for k in KEYS:
        if k not in meta_data:
            meta_fill[k] = {'rows': 0}

    return meta_fill


def _get_meta_data() -> Dict:
    meta_data: Dict

    if os.path.isfile(META_PATH):
        with open(META_PATH) as json_file:
            meta_data = json.load(json_file)
    else:
        meta_data = dict() # there are not previous executions

    return _fill_empty_keys(meta_data=meta_data)


def _write_meta_data(meta: Dict) -> None:
    with open(META_PATH, 'w+') as outfile:
        json.dump(meta, outfile)
    
    print(f'Updated meta-data in {META_PATH}')


def run() -> None:
    print('------------- Updating Aragon\' datawarehouse -------------\n')
    if not os.path.isdir(DIRS):
        os.makedirs(DIRS)

    meta_data: Dict = _get_meta_data()

    for c in COLLECTORS:
        c(meta_data)

    _write_meta_data(meta=meta_data)
    print('------------- Aragon\' datawarehouse updated -------------\n')


if __name__ == '__main__':
    run()
