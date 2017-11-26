import requests
import re
import pickle
import time
from lxml import etree
import csv

# Need page number, sorted by activity, 100 page size
queryURI = "https://bitcoin-otc.com/viewratings.php"

# users tagged with id, fingerprint, keyid, btc address, nickname, auth, registration 
def findUsersWithBitcoinScore():
	r = requests.get(queryURI)
	allrows = []
	table = etree.HTML(r.text).findall("body/table")[1]
	rows = iter(table)
	headers = [col.text for col in next(rows)]
	for row in rows:
	    values = [col.text for col in row]
	    allrows.append(dict(zip(headers, values)))
	return allrows

def findUsersWithBitcoin():
	users = load("otc_users.p")
	if users:
		return users

	r = requests.get(queryURI)
	count = 0
	users = r.json()
	finalUsers = []
	for user in users:
		if(user.get("bitcoinaddress", None)):
			count += 1
			finalUsers.append(user)
	save_users(finalUsers)
	return finalUsers

def run():
	users = findUsersWithBitcoin()
	scoreMap = getScoreMap()
	finalScoreMap = {}
	for user in users:
		userId = user["id"]
		btc = user["bitcoinaddress"]
		if userId in scoreMap:
			score = scoreMap[userId]
			finalScoreMap[btc] = score["total rating"]
	save(finalScoreMap, "otc_id_to_score_map.p")

def formatById(rows):
	return dict((row["id"], row) for row in rows)

def save(data, fileName):
	pickle.dump(data, open( fileName, "wb" ))

def load(fileName):
	try:
		data = pickle.load(open(fileName, "rb" ))
		return data
	except:
		return []

def getScoreMap():
	users = findUsersWithBitcoinScore()
	return formatById(users)

def saveData():
	save(getScoreMap(), "otc_score_map.p")

def writeDataToCsv(data):
	with open('otc_scores_dict.csv', 'w') as csv_file:
	    writer = csv.writer(csv_file)
	    for key in data:
	    	if (data[key]):
		    	writer.writerow([key.encode(), data[key].encode()])

def runCsv():
	data = load("otc_id_to_score_map.p")
	writeDataToCsv(data)
