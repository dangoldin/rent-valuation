#! /usr/bin/env python

import sys
import requests
import config

import xml.etree.ElementTree
import xml.dom.minidom

BASE_URL = 'http://www.zillow.com/webservice'

GET_SEARCH_RESULTS = BASE_URL + '/GetSearchResults.htm'
GET_ESTIMATE = BASE_URL + '/GetZestimate.htm'
GET_PROPERTY_DETAILS = BASE_URL + '/GetUpdatedPropertyDetails.htm'

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

    xml2 = xml.dom.minidom.parseString(r.content)
    pretty_xml_as_string = xml2.toprettyxml()
    print pretty_xml_as_string

def get_property_details(zpid):
    r = requests.get(GET_PROPERTY_DETAILS, params={
        'zws-id': config.ZWSID,
        'zpid': zpid
    })
    # TODO: Handle failure case

    print r.content

if __name__ == '__main__':
    ADDRESS = sys.argv[1]
    ZIPCODE = sys.argv[2]

    print 'Retrieving info for address', ADDRESS, ZIPCODE
    zpid = get_top_match(ADDRESS, ZIPCODE)
    print 'Received ZPID', zpid
    get_estimate(zpid)
    get_property_details(zpid)
