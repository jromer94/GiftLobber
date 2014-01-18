import urllib
import urllib2
import json


def lobPost(url, values):

    data = urllib.urlencode(values)
    req = urllib2(url, data)
    response = urllib2.urlopen(req)
    return json.load(response)
