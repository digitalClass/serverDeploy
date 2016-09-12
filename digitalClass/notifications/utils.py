# -*- coding: utf-8 -*-

import sys
if sys.version > '3':
    long = int


def slug2id(slug):
    return long(slug)


def id2slug(id):
    return id
