import requests
import re
import pickle

re_btc_address = re.compile(u'(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])')

# API key from stack exchange
keyAddition = "&key=5q0sv0fEfFMHcw0BP5IuzA(("
# keyAddition=""
# Need page number, sorted by activity, 100 page size
queryURI = "https://api.stackexchange.com/2.2/questions?page=%d&pagesize=100&order=desc&sort=votes&site=stackoverflow&filter=!Lb0vO.woyyXi8abzGjlB-5" + keyAddition

# metadata is page, acount, qcount, ccount abcount, qbcount, cbcount
def run():
	answerCount = 0
	questionCount = 0
	commentCount = 0

	answerBCount = 0
	questionBCount = 0
	commentBCount = 0
	page = 1
	globalList = []
	runs = 8000
	metadata = load_metadata()
	try:
		if len(metadata) == 7:
			page = metadata[0]
			answerCount = metadata[1]
			questionCount = metadata[2]
			commentCount = metadata[3]
			answerBCount = metadata[4]
			questionBCount = metadata[5]
			commentBCount = metadata[6]
			globalList = load_data() 
	except:
		pass

	
	for i in range(runs):
		try:
			print(page)
			r = requests.get(queryURI % page)
			page += 1
			items = r.json()["items"]
			for question in items:
				questionCount += 1
				qInfo = formatPost(question)
				if qInfo is not None:
					questionBCount += 1
					globalList.append(qInfo)
				answers = question.get("answers", [])
				for answer in answers:
					answerCount += 1
					aInfo = formatPost(answer)
					if aInfo is not None:
						answerBCount += 1
						globalList.append(aInfo)

				comments = question.get("comments", [])
				for comment in comments:
					commentCount += 1
					cInfo = formatPost(comment)
					if cInfo is not None:
						commentBCount += 1
						globalList.append(cInfo)

			if (i%20 ==0) :
				save_data(globalList)
				save_metadata([page, answerCount, questionCount, commentCount, answerBCount, questionBCount, commentBCount])
				total = answerCount + questionCount + commentCount
				print("Crawled -- Answers: %d, Questions: %d, Comments: %d, Total: %d" % (answerCount, questionCount, commentCount, total))
				totalB = answerBCount + questionBCount + commentBCount
				print("BTC Detected -- Answers: %d, Questions: %d, Comments: %d, Total: %d" % (answerBCount, questionBCount, commentBCount, totalB))
	
			if (not r.json()['has_more']):
				print("Reached end of crawl")
				break
		except KeyboardInterrupt:
			break
		except:
			print("FAILED")

	save_data(globalList)
	save_metadata([page, answerCount, questionCount, commentCount, answerBCount, questionBCount, commentBCount])
	total = answerCount + questionCount + commentCount
	print("Crawled -- Answers: %d, Questions: %d, Comments: %d, Total: %d" % (answerCount, questionCount, commentCount, total))

	totalB = answerBCount + questionBCount + commentBCount
	print("BTC Detected -- Answers: %d, Questions: %d, Comments: %d, Total: %d" % (answerBCount, questionBCount, commentBCount, totalB))
	

def formatPost(post):
	btc = findBtc(post["body"])
	if btc:
		response = {}
		response["question_id"] = post.get("question_id", post.get("post_id", -1))
		response["answer_id"] = post.get("answer_id", -1)
		response["score"] = post.get("score", -1)
		response["owner"] = post["owner"]
		response["creation_date"] = post.get("creation_date")
		response["bitcoin"] = btc
		response["body"] = post["body"]
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

def save_metadata(metadata):
	pickle.dump(metadata, open( "stack_metadata.p", "wb" ))

def load_metadata():
	try:
		metadata = pickle.load(open( "stack_metadata.p", "rb" ))
		return metadata
	except:
		return 1