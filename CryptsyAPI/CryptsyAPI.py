#!/usr/bin/env python

# CryptsyAPI: Python Cryptsy API implementation
#
# Copyright (c) 2014 - Albert Puigsech Galicia (albert@puigsech.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import random
import requests
from requests.auth import AuthBase
import hmac
import hashlib
import json

class CryptsyAuth(AuthBase):
  def __init__(self, key, secret):
    self.key = key
    self.secret = secret

  def __call__(self, r):
    r.body += '&nonce={0}'.format(int(random.uniform(0,4294967296)))
    diggest = hmac.new(self.secret, r.body, hashlib.sha512).hexdigest()

    r.headers['Key'] = self.key
    r.headers['Sign'] = diggest
    return r


class CryptsyAPI:
  def __init__(self, key, secret, simulation=False, cached=False):
    self.url = 'https://api.cryptsy.com/api'
    self.key = key
    self.secret = secret
    self.simulation = simulation
    self.cached = cached
    self.cache = {}


  def request(self, method, args=None):
    if args == None:
      args = {}

    res = requests.post(
      self.url,
      data=dict(args.items() + {'method': method}.items()),
      auth=CryptsyAuth(self.key, self.secret)
    )

    return json.loads(res.text)


  def getinfo(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'getinfo'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('getinfo')
    return self.cache[keycache]


  def getmarkets(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'getmarkets'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('getmarkets')
    return self.cache[keycache]


  def getcoindata(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'getcoindata'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('getcoindata')
    return self.cache[keycache]


  def getwalletstatus(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'getwalletstatus'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('getwalletstatus')
    return self.cache[keycache]


  def mytransactions(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'mytransactions'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('mytransactions')
    return self.cache[keycache]  


  def markettrades(self, marketid, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'markettrades'+str(marketid)
    if cached == False or self.cached.has_key(keycache) == False:
      args = {
        'marketid': marketid
      }
      self.cache[keycache] = self.request('markettrades', args)
    return self.cache[keycache] 


  def marketorders(self, marketid, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'marketorders'+str(marketid)
    if cached == False or self.cached.has_key(keycache) == False:
      args = {
        'marketid': marketid
      }
      self.cache[keycache] = self.request('marketorders', args)
    return self.cache[keycache] 


  def mytrades(self, marketid, limit=200, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'mytrades'+str(marketid)+str(limit)
    if cached == False or self.cached.has_key(keycache) == False:
      args = {
        'marketid': marketid,
        'limit': limit
      }
      self.cache[keycache] = self.request('mytrades', args)
    return self.cache[keycache] 


  def allmytrades(self, startdate=None, enddate=None, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'allmytrades'+str(startdate)+str(enddate)
    if cached == False or self.cached.has_key(keycache) == False:
      args = {
        'startdate': startdate,
        'enddate': enddate
      }
      self.cache[keycache] = self.request('allmytrades', args)
    return self.cache[keycache]


  def myorders(self, marketid, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'myorders'+str(marketid)
    if cached == False or self.cached.has_key(keycache) == False:
      args = {
        'marketid': marketid
      }
      self.cache[keycache] = self.request('myorders', args)
    return self.cache[keycache]


  def depth(self, marketid, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'depth'+str(marketid)
    if cached == False or self.cached.has_key(keycache) == False:
      args = {
        'marketid': marketid
      }
      self.cache[keycache] = self.request('depth', args)
    return self.cache[keycache]  


  def allmyorders(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'allmyorders'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('allmyorders')
    return self.cache[keycache]


  def createorder(self, marketid, ordertype, quantity, price, simulated=None):
    if simulated == None:
      simulated = self.simulated

    if simulated == False:
      args = {
        'marketid': marketid,
        'ordertype': ordertype,
        'quantity': quantity,
        'price': price
      }
      r = self.request('createorder', args)
    else:
      r = None
    return r


  def cancelorder(self, orderid, simulated=None):
    if simulated == None:
      simulated = self.simulated

    if simulated == False:
      args = {
        'orderid': orderid,
      }
      r = self.request('cancelorder', args)
    else:
      r = None
    return r


  def cancelmarketorders(self, marketid, simulated=None):
    if simulated == None:
      simulated = self.simulated

    if simulated == False:
      args = {
        'marketid': marketid
      }
      r = self.request('cancelmarketorders', args)
    else:
      r = None
    return r


  def cancelallorders(self, simulated=None):
    if simulated == None:
      simulated = self.simulated

    if simulated == False:
      r = self.request('cancelallorders')
    else:
      r = None
    return r


  def calculatefees(self, ordertype, quantity, price, simulated=None):
    if simulated == None:
      simulated = self.simulated

    if simulated == False:
      args = {
        'ordertype': ordertype,
        'quantity': quantity,
        'price': price
      }
      r = self.request('calculatefees', args)
    else:
      r = None
    return r


  def generatenewaddress(self, currencyid=None, currencycode=None):
    pass


  def mytransfers(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'mytransfers'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('mytransfers')
    return self.cache[keycache]


  def makewithdrawal(self, address, amount, simulated=None):
    if simulated == None:
      simulated = self.simulated

    if simulated == False:
      args = {
        'address': address,
        'amount': amount
      }
      r = self.request('makewithdrawal', args)
    else:
      r = None
    return r


  def getmydepositaddresses(self, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'getmydepositaddresses'
    if cached == False or self.cached.has_key(keycache) == False:
      self.cache[keycache] = self.request('getmydepositaddresses')
    return self.cache[keycache]


  def getorderstatus(self, orderid, cached=None):
    if cached == None:
      cached = self.cached

    keycache = 'getorderstatus'+str(orderid)
    if cached == False or self.cached.has_key(keycache) == False:
      args = {
        'orderid': orderid
      }
      self.cache[keycache] = self.request('getorderstatus', args)
    return self.cache[keycache]


  def getmarket(self, primary, secondary):
    for m in self.getmarkets()['return']:
      if m['primary_currency_code'] == primary and m['secondary_currency_code'] == secondary:
        return m
    return None


  def order_buy(self, primary, secondary, quantity, price, simulated=None):
    return self.createorder(self.getmarket(primary, secondary)['marketid'], 'Buy', quantity, price, simulated=simulated)


  def order_sell(self, primary, secondary, quantity, price, simulated=None):
    return self.createorder(self.getmarket(primary, secondary)['marketid'], 'Sell', quantity, price, simulated=simulated)





