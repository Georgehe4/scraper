import requests
import re
import pickle
import time

# Need page number, sorted by activity, 100 page size
queryURI = "https://bitcoin-otc.com/viewgpg.php?outformat=json"

# Rating reprocity, fill in nickname
reprocityURI = "https://bitcoin-otc.com/ratingreciprocity.php?nick=%s&outformat=json"

# users tagged with id, fingerprint, keyid, btc address, nickname, auth, registration 
def findUsersWithBitcoin():
	users = load_users()
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


def createRatingsList():
	users = findUsersWithBitcoin()
	userMapByNickname = createUserMapBy(users, "nick")
	nicknames = sorted(userMapByNickname.keys())
	nicknameIndex = load_metadata()
	allRatings = load_data()
	if not nicknameIndex:
		nicknameIndex = 0
	while(nicknameIndex < len(nicknames)):
		try:
			nickname = nicknames[nicknameIndex]
			print(nicknameIndex, nickname, len(allRatings))
			allRatings.extend(findRatings(nickname, userMapByNickname))
			nicknameIndex += 1
			save_data(allRatings)
			save_metadata(nicknameIndex)
			time.sleep(1)
		except Exception as e:
			print("Unable to get data", e)
			time.sleep(5)
			save_data(allRatings)
			save_metadata(nicknameIndex)


def createUserMapBy(users, field):
	return dict((user[field], user) for user in users)

def findRatingRaw(nickname):
	r = requests.get(reprocityURI %nickname)
	reprocities = r.json()
	return reprocities
# Returns lit of triplets of (from, to, rating)
# nickname = user nickname
def findRatings(nickname, userMapByNickname):
	reprocities = findRawingRaw(nickname)
	ratings = []
	for rep in reprocities:
		if (rep["rater_nick"] != nickname):
			break
		rater = userMapByNickname.get(rep["rater_nick"], None)
		ratee = userMapByNickname.get(rep["rated_nick"], None)
		if (rater is None or ratee is None):
			break
		ratings.append((rater["id"], ratee["id"], rep["rating"]))
	return ratings

def save_data(data):
	pickle.dump(data, open( "otc_data.p", "wb" ))

def load_data():
	try:
		data = pickle.load(open( "otc_data.p", "rb" ))
		return data
	except:
		return []

def save_metadata(data):
	pickle.dump(data, open( "otc_metadata.p", "wb" ))

def load_metadata():
	try:
		data = pickle.load(open( "otc_metadata.p", "rb" ))
		return data
	except:
		return []

def save(data, fileName):
	pickle.dump(data, open( fileName, "wb" ))

def load(data,fileName):
	try:
		data = pickle.load(open(fileName, "rb" ))
		return data
	except:
		return []

def save_users(data):
	pickle.dump(data, open( "otc_users.p", "wb" ))

def load_users():
	try:
		data = pickle.load(open( "otc_users.p", "rb" ))
		return data
	except:
		return []

def print_addr():
	data = load_data()
	btc = []
	for point in data:
		btc.extend(point["bitcoin"])
	btc_set = set(btc)
	print(btc_set)
	print(len(btc_set))