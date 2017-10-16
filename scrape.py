import praw
import info
import re



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
	submission.comments.replace_more(limit=0)
	for comment in submission.comments.list():
		try:
			author = comment.author
			addr = get_list_of_addresses(comment.body)
			if (addr):
				addresses.append((author, addr))
		except:
			pass

def scrape_subreddit(subreddit, number_to_scrape=1000):
	scraped = 0
	start = None
	addresses = []
	earliest_start = float("inf")
	while (scraped < number_to_scrape):
		scraped += 1000
		submissions = subreddit.submissions(start - 1)
		for submission in submissions:
			addr = get_list_of_addresses(submission.selftext)
			if (addr):
				addresses.append((submission.author, addr))
			btc_addresses = scrape_comments_for_btc(submission)
			if (btc_addresses):
				addresses.extend(btc_addresses)
			earliest_start = min(submission.created_utc, earliest_start)
			print(earliest_start, addresses)
		# end of subreddit reached
		if (len(submissions) < 2):
			break
	return addresses

def scrape_user(user, number_to_scrape=1000):
	scraped = 0
	while (scraped < number_to_scrape):
		scraped += 1000

scrape_subreddit(btc_sub)


