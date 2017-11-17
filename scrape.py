import praw
import info
import re
import pickle
import time



reddit = praw.Reddit(client_id=info.CLIENT_ID,
                     client_secret=info.CLIENT_SECRET,
                     password=info.PASSWORD,
                     user_agent=info.USER_AGENT,
                     username=info.USER_NAME)

re_btc_address = re.compile(u'(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])')

btc_sub = reddit.subreddit("bitcoin")

print("Beginning scrape as %s" % reddit.user.me())

def get_list_of_addresses(text):
	return [x for x in re_btc_address.findall(text)]

def scrape_comments_for_btc(submission):
	'''
	Scrapes the comments of a submission for bitcoin addresses
	'''
	addresses = []
	try:
		submission.comments.replace_more(limit=10)
	except:
		pass
	for comment in submission.comments.list():
		try:
			author = comment.author
			addr = get_list_of_addresses(comment.body)
			if (addr):
				addresses.append((author.name, addr))
		except:
			print("failed to handle comment")
			pass

def save_address(data):
	pickle.dump(data, open( "save.p", "wb" ))

def save_metadata(time, count):
	pickle.dump((time, count), open( "metadata.p", "wb" ))

def scrape_subreddit(subreddit, number_to_scrape=1000, start = float("inf")):
	scraped = 0
	earliest_start = start
	try:
		metadata = pickle.load(open( "metadata.p", "rb" ))
		earliest_start = metadata[0]
		scraped = metadata[1]
	except:
		pass
	addresses= []
	try:
		addresses = pickle.load(open( "save.p", "rb" ))
	except:
		pass

	while (scraped < number_to_scrape):
		if earliest_start != float("inf"):
			submissions = subreddit.submissions(end = earliest_start - 1)
		else:
			submissions = subreddit.submissions()
		lastScraped = scraped
		for submission in submissions:
			scraped += 1
			addr = get_list_of_addresses(submission.selftext)
			if (addr):
				addresses.append((submission.author.name, addr))
			btc_addresses = scrape_comments_for_btc(submission)
			if (btc_addresses):
				addresses.extend(btc_addresses)
			if (addr or btc_addresses):
				save_address(addresses)
				save_metadata(submission.created_utc, scraped)
				print(len(addresses))
			print(submission.created_utc, scraped)
			earliest_start = min(submission.created_utc, earliest_start)
		# end of subreddit reached
		if (scraped - lastScraped < 2):
			break
	return addresses

def scrape_user(user, number_to_scrape=1000000):
	scraped = 0
	while (scraped < number_to_scrape):
		scraped += 1000

def load():
	return pickle.load(open( "save.p", "rb" ))

loading = True
if loading:
	a = load()
	listOfAddresses = []
	for i in a:
		listOfAddresses.extend(i[1])

	print(set(listOfAddresses))
	print(len(set(listOfAddresses)))
	
else:
	scrape_subreddit(btc_sub, number_to_scrape=1000000)

#(1508290281.0, 2)
#(1507920729.0, 1635)





