#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import base64
import json
import requests


VERBOSE = False

def log(msg, *args, **kwargs):
    if VERBOSE:
        print(msg, *args, **kwargs)


def parse_args():
    global VERBOSE
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', '-u')
    parser.add_argument('--password', '-p')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--login', action='store_true')
    parser.add_argument('--logout', action='store_true')
    args = parser.parse_args()
    VERBOSE = bool(args.verbose)
    return args

def need_login():
    log('Testing network...')
    r = requests.get('http://www.nctu.edu.tw')
    if r.text.find('NCTU Dormitory Network') != -1:
        return True
    return False

def login(args):
    log('login as', args.username)
    payload = {
        'username': args.username,
        'password': base64.b64encode(args.password.encode())
    }
    r = requests.post('http://www.nctu.edu.tw/auth/', data=payload)
    body = json.loads(r.json()['body'])
    if r.status_code == 200 and body['status'] == 'Enable':
        return True
    else:
        return False

def logout():
    log('logout')
    r = requests.post('http://140.113.178.244/unauth/', data={})
    body = json.loads(r.json()['body'])
    if r.status_code == 200 and body['status'] == 'Disable':
        return True
    else:
        return False

if __name__ == '__main__':
    args = parse_args()
    if args.login:
        if need_login():
            login(args)
    elif args.logout:
        logout()

