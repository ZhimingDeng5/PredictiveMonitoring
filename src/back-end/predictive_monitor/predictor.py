#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'

from fastapi import File

class Predictor(object):
    predictor_ID: int
    predictor_name: str
    type: str
    schema: File
    encoding_type: str
    bucketing_type: str
    pre_method: str
    cluster: int
    max_features: int
    max_depth: int

    def __init__(self, predictor_ID, predictor_name, type, schema, encoding_type, bucketing_type, pre_method, cluster, max_features, max_depth):
        self.predictor_ID = predictor_ID
        self.predictor_name =predictor_name
        self.type = type
        self.schema = schema
        self.encoding_type = encoding_type
        self.bucketing_type = bucketing_type
        self.pre_method = pre_method
        self.cluster = cluster
        self.max_features = max_features
        self.max_depth = max_depth