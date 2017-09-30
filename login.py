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
    r = requests.get('http://www.nctu.edu.tw/fgtauth')
    r.encoding = 'utf-8'
    soup = bs4(r.text)
    payload = {x.get('name'): x.get('value') for x in soup.find_all('input') if x.get('name')}
    payload['username'] = args.username
    payload['password'] = args.password
    r = requests.post('http://www.nctu.edu.tw/fgtauth/', data=payload)

def logout():
    log('logout')
    r = requests.post('http://140.113.178.244/unauth/', data={})

if __name__ == '__main__':
    args = parse_args()
    if args.login:
        if need_login():
            login(args)
    elif args.logout:
        logout()

