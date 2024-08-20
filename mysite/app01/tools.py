#-*- coding:utf-8 -*-
"""
Author: yuanchangtian
Data: 2024-07-15
Owner: Shanghai Dermatology Hospital
"""

import pysm4

def get_sm4(text, key):
    text_sm4 = pysm4.encrypt_ecb(text, key)
    return text_sm4