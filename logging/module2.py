#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 11:24:24 2017

@author: sogoyal
"""

import logging

def foo():
    logger = logging.getLogger("root." + __name__)
    logger.info("This is an Error")
    print()
    print("Hello")