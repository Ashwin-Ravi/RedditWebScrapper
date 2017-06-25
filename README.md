Reddit Web Scrapper

Given a Subreddit URL, The script scrapes the content of the webpage. It picks the first 10 items.
Subsequently Identifying the top 10 comments by points (including nested comments) for each. 
The script then identifies the high frequency (top 10) words for each item.
Providing an approximation of the trending topics and words in Reddit.



Example:

Input:
https://www.reddit.com/r/all/

Output:
[
	{
		"url": "https://i.imgflip.com/1kzbwx.jpg",
		"commentsUrl": "https://www.reddit.com/r/AdviceAnimals/comments/5y54am/my_uncle_is_an_awesome_boss/",
		"topComments": [
			"The cashier is a young woman from Guatemala (legally immigrated here 4 years ago) (17, I think), she looked genuinely scared lifeless. My uncle drove her home to make sure that jackass didn't try anything and worked her shift.",
			"I like pancakes.",
			"Emoposer is a reference to goth episode of South Park.",
			... (10 elements)
		],
		"HighFrequencyWords": [
			"cashier",
			"South Park",
			... (10 elements)
		]
	},
	{
		...
	},
	... (10 elements)
]
