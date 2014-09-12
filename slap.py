import sqlite3
import uptime
import datetime

# Dori! This is not the actual path!

db = sqlite3.connect("../.mozilla/firefox/yy35kyvm.default/places.sqlite") 


def site_id(site  = 'facebook'):	#defaults to FB

	""" Returns url of a site from moz_places table. """

	site = site.capitalize() 

	query_string = "select id from moz_places where title = '%s' order by url asc" % site

	c = db.execute(query_string)

	return [i[0] for i in c][0]
	

def site_visits(site, hours_back):

	""" Number of visits in the last x hours. """
	
	now_epoch = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds()

	if hours_back == 0:
		up = uptime.uptime()          # OR TODAY IF IT'S LESS!!! datetime.timedelta
		uptime_epoch = int(now_epoch - up)

	else:
		uptime_epoch = int(now_epoch - hours_back*3600)

	sid = site_id(site)

	query_string = "select visit_date as raw_visit_date,datetime(visit_date/1000000,'unixepoch', 'localtime') from moz_historyvisits where place_id == %d" % sid 

	c = db.execute(query_string)
	
	results = [i for i in c if int(i[0]/1000000) >= uptime_epoch]
	return len(results)



