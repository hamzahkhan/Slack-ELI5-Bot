import praw

reddit = praw.Reddit(client_id = 'N0x577dukjYOog',
					client_secret = 'K59asXl2u2oCZLXOAAQRBkQKraM' ,
					username = 'khamzah22' ,
					password=  'Aligarh!2', 
					user_agent = 'eli5_bot' 
					)

from googlesearch import search 

# to search 
query = "eli5 turbocharger"
  
def praw_query(query_word):
	to_query = []
	for j in search("eli5 " + query_word, tld="co.in", num=10, stop=10, pause=2):
		to_query.append(str(j))
		break

	post = reddit.submission(url=to_query[0])

	for comment in post.comments:
		to_query.append(comment.body)
		break

	return to_query[1]