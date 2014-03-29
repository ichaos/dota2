# dota2 webapi python code
import os
import json
import requests

def get_league_listing(apikey, url="https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/"):
	params = {
		'key' : apikey
	}
	r = requests.get(url, params=params)
	#print(r.text)
	return r

# 65001 - dota2 international 2012
def get_match_history(apikey, leagueid='', start_at_match_id='', url="https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/"):
	params = {
		'key' : apikey,
		'league_id' : leagueid,
		'start_at_match_id' : start_at_match_id,
	}
	r = requests.get(url, params=params)
	return r

mykey = '8A826DD8EFF31829651376577344FAEE'

# read dota2 league data
if not os.path.isfile('./data/dota2leaguelist.txt'):
	r = get_league_listing(mykey)
	#write to file
	f = open('./data/dota2leaguelist.txt', 'a+')
	f.write(r.text)
	f.close()

f = open('./data/dota2leaguelist.txt', 'r')

j = json.load(f)

# parse the results and get all matches results
for league in j["result"]["leagues"]:
	print league["name"] + " : " + str(league["leagueid"])
	recv_num = 0
	r = get_match_history(mykey, str(league["leagueid"]))
	
	fname = 'league' + str(league["leagueid"]) + 'matches.txt'
	m = open('./data/leagues/' + fname, 'w+')
	#m.write(r.text)
	jd = r.json()
	recv_num = recv_num + len(jd["result"]["matches"])
	total = jd["result"]["total_results"]
	while recv_num < total:
		r = get_match_history(mykey, str(league["leagueid"]), str(jd["result"]["matches"][len(jd["result"]["matches"]) - 1]["match_id"] - 1))
		njd = r.json()
		recv_num = recv_num + len(njd["result"]["matches"])
		jd["result"]["matches"].extend(njd["result"]["matches"])
		jd["result"]["results_remaining"] = jd["result"]["results_remaining"] - len(njd["result"]["matches"])
	
	print "get matches " + str(recv_num) + " from total " + str(jd["result"]["total_results"]) + \
		", remaining " + str(jd["result"]["results_remaining"])
	json.dump(jd, m)
	m.close()
	#break
