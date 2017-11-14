import requests
import re
import pickle

re_btc_address = re.compile(u'(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])')

keyAddition = "&key=5q0sv0fEfFMHcw0BP5IuzA(("
# keyAddition=""
# Need page number, sorted by activity, 100 page size
queryURI = "https://api.stackexchange.com/2.2/questions?page=%d&pagesize=100&order=desc&sort=votes&site=bitcoin&filter=!Lb0vO.woyyXi8abzGjlB-5" + keyAddition

def run():
	globalList = [] # load_data() 
	runs = 5000
	page = 1 # load_metadata()
	for i in range(runs):
		print(page)
		r = requests.get(queryURI % page)
		page += 1
		items = r.json()["items"]
		for question in items:
			qInfo = formatPost(question)
			if qInfo is not None:
				globalList.append(qInfo)
			answers = question.get("answers", [])
			for answerlo in answers:
				aInfo = formatPost(question)
				if aInfo is not None:
					globalList.append(aInfo)

			comments = question.get("comments", [])
			for comment in comments:
				cInfo = formatPost(comment)
				if cInfo is not None:
					globalList.append(cInfo)

		if (i%100 ==0) :
			save_data(globalList)
			save_metadata(page)
		if (not r.json()['has_more']):
			print("Reached end of crawl")
			break
	save_data(globalList)
	save_metadata(page)

def formatPost(post):
	btc = findBtc(post["body"])
	if btc:
		response = {}
		response["owner"] = post["owner"]
		response["question_id"] = post.get("question_id", post.get("post_id", -1))
		response["answer_id"] = post.get("answer_id", -1)
		response["score"] = post.get("score", -1)
		response["owner"] = post["owner"]
		response["creation_date"] = post.get("creation_date")
		response["bitcoin"] = btc
		return response
	return None


def findBtc(content):
	return set(re_btc_address.findall(content))

def save_data(data):
	pickle.dump(data, open( "stack.p", "wb" ))

def load_data():
	try:
		data = pickle.load(open( "stack.p", "rb" ))
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

def save_metadata(page):
	pickle.dump(page, open( "stack_metadata.p", "wb" ))

def load_metadata():
	try:
		metadata = pickle.load(open( "stack_metadata.p", "rb" ))
		return metadata
	except:
		return 1