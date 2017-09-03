#! /usr/bin/env python

import sys
import requests
import config

import xml.etree.ElementTree
import xml.etree as etree

BASE_URL = 'http://www.zillow.com/webservice'

GET_SEARCH_RESULTS = BASE_URL + '/GetSearchResults.htm'
GET_ESTIMATE = BASE_URL + '/GetZestimate.htm'

def get_top_match(addr, zipc):
    r = requests.get(GET_SEARCH_RESULTS, params={
        'zws-id': config.ZWSID,
        'address': addr,
        'citystatezip': zipc,
    })
    # TODO: Handle failure case

    # Return the first one
    e = xml.etree.ElementTree.fromstring(r.content)
    for res in e.iter('zpid'):
        return res.text
    return None

def get_estimate(zpid):
    r = requests.get(GET_ESTIMATE, params={
        'zws-id': config.ZWSID,
        'zpid': zpid,
        'rentzestimate': 'true',
    })
    # TODO: Handle failure case

    print r.content
    e = xml.etree.ElementTree.fromstring(r.content)
    xml.etree.ElementTree.tostring(e.text)

if __name__ == '__main__':
    ADDRESS = sys.argv[1]
    ZIPCODE = sys.argv[2]

    print 'Retrieving info for address', ADDRESS, ZIPCODE
    zpid = get_top_match(ADDRESS, ZIPCODE)
    print 'Received ZPID', zpid
    get_estimate(zpid)
