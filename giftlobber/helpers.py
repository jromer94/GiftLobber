import urllib
import urllib2
import json
import base64


def lobPost(url, values, password):
	base64string = base64.encodestring('%s:' % (password))[:-1]
	print "fuckkkk"	
	data = urllib.urlencode(values)
	req = urllib2.Request(url)
	print data
	req.add_data(urllib.urlencode(values))
	req.add_header("Authorization", "Basic %s" % base64string)
	response = urllib2.urlopen(req)


	return json.load(response)
