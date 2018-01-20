# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 07:18:00 2018

@author: Nitin
"""

import gensim


model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin')
