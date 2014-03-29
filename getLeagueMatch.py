# fetch dota2 match details 
import os
import json
import requests

mykey = '8A826DD8EFF31829651376577344FAEE'

def get_match_detail(apikey, match_id, url='https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'):
	params = {
		'match_id' : match_id,
	}

	r = requests.get(url, params=params)
	return r

def get_league_matches(fdir, name):
	path = os.path.join(fdir, name)
	f = open(path)
	jd = json.load(f)
	for m in jd["result"]["matches"]:
		r = get_match_detail(mykey, str(m["match_id"]))
		print('get match[' + str(m["match_id"]) + '] detail')
		mf = open('match_detail_' + str(m["match_id"]), 'w+')
		njd = r.json()
		json.dump(njd, mf)
		mf.close()
	f.close()

leag_dir = "./data/leagues/"
for fname in os.listdir(leag_dir):
	#fpath = os.path.join(leag_dir, fname)
	get_league_matches(leag_dir, fname)

