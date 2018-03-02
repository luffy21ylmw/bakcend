#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
POOL = redis.ConnectionPool(host='192.168.0.191',port=6379)
