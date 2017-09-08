#! /usr/bin/env python

import sys
import requests
import config
import re

import xml.etree.ElementTree
import xml.dom.minidom

BASE_URL = 'http://www.zillow.com/webservice'

GET_SEARCH_RESULTS = BASE_URL + '/GetSearchResults.htm'
GET_ESTIMATE = BASE_URL + '/GetZestimate.htm'
GET_PROPERTY_DETAILS = BASE_URL + '/GetUpdatedPropertyDetails.htm'
GET_DEEP_COMPS = BASE_URL + '/GetDeepComps.htm'

RE_XML_ERROR_CODE = re.compile(r'<code>(\d+)</code>')

def pretty_print_xml(xml_string):
    return xml.dom.minidom.parseString(xml_string).toprettyxml()

def get_error_code(xml_string):
    error_codes = RE_XML_ERROR_CODE.findall(xml_string)
    if len(error_codes):
        return int(error_codes[0])
    return 0

def is_valid_request(r):
    return not (r.status_code >= 300 or get_error_code(r.content) > 0)

def get_top_match(addr, zipc):
    r = requests.get(GET_SEARCH_RESULTS, params={
        'zws-id': config.ZWSID,
        'address': addr,
        'citystatezip': zipc,
    })
    if not is_valid_request(r):
        print 'Failed to find address', addr, zipc
        return None

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
    if not is_valid_request(r):
        print 'Failed to get estimate for', zpid
        return None

    e = xml.etree.ElementTree.fromstring(r.content)
    print pretty_print_xml(r.content)

def get_property_details(zpid):
    r = requests.get(GET_PROPERTY_DETAILS, params={
        'zws-id': config.ZWSID,
        'zpid': zpid,
    })
    if not is_valid_request(r):
        print 'Failed to get property details for', zpid
        return None

    print pretty_print_xml(r.content)

def get_deep_comps(zpid):
    r = requests.get(GET_DEEP_COMPS, params={
        'zws-id': config.ZWSID,
        'zpid': zpid,
        'count': 25,
        'rentzestimate': 'true',
    })
    if not is_valid_request(r):
        print 'Failed to get deep comps for', zpid
        return None

    print pretty_print_xml(r.content)

# TODO: Possibly use headless code
# HOA (Zillow has this but seems it's random)
# Taxes (Some counties have this public)

if __name__ == '__main__':
    ADDRESS = sys.argv[1]
    ZIPCODE = sys.argv[2]

    print 'Retrieving info for address', ADDRESS, ZIPCODE
    zpid = get_top_match(ADDRESS, ZIPCODE)
    print 'Received ZPID', zpid
    get_estimate(zpid)
    get_property_details(zpid)
    get_deep_comps(zpid)
