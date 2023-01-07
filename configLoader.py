#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time  : 2023/01/07 17:55:22
# @Author: wd-2711
'''

import yaml

def getYamlData(config_path):
    """
        Get infomation from yaml.
    """
    with open(config_path, 'r', encoding = 'utf-8') as f:
        return yaml.load(f.read())