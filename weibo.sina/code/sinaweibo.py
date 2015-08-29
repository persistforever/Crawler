# -*- encoding=utf-8 -*-

from weibo import APIClient
import json
import time

charset = 'utf-8'

class Weibo :
	# attributes
	APP_KEY = '1464287299' # app key
	APP_SECRET = 'e4d573c77e41118abe06df2628cc4418' # app secret
	CALLBACK_URL = 'http://www.example.com/callback' # callback url
	WEIBOLIST_PATH = '../result/weibolist/'
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	access_token='2.00v5KI4DFBAGbB4289cec5d0MFFs5B'

	# methods
	def getNewWeiboList(self, weibonum) :
		idlist = []
		iternum = int(weibonum/100)
		for i in range(iternum) :
			try:
				jsondata = self.client.statuses.public_timeline.get(access_token = self.access_token, count=100)
				for weibo in jsondata['statuses'] :
					idlist.append(weibo['id'])
			except Exception, e:
				pass
		return list(set(idlist))

	def writeWeiboList(self, weibolist) :
		now = time.strftime('%Y%m%d_%H%M', time.localtime())
		name = self.WEIBOLIST_PATH + now + '.txt'
		with open(name, 'w') as fw :
			for weiboid in weibolist :
				fw.writelines(str(weiboid) + '\n')

	def getCommentsList(self, weiboid) :
		pair = []
		qalist = []
		for page in range(1, 4) :
			try :
				jsondata = self.client.comments.show.get(access_token = self.access_token, id=weiboid, count=200, page=page)
				for comment in  jsondata['comments'] :
					senduser = comment['user']['screen_name'] # [comment['text']], comment['created_at']
					recvuser, content = self.findReplyComment(comment['text'])
					if recvuser != None :
						pair.append([senduser, recvuser, content])
						qalist.append([senduser, recvuser, content, self.convertDate(comment['created_at'])])
			except Exception, e :
				pass
		for senduser, recvuser, content, time in qalist :
			print senduser.encode(charset), recvuser.encode(charset), content.encode(charset), time

	def findReplyComment(self, text) :
		if u'回复@' in text and ':' in text :
			stidx = text.find('@')
			edidx = text[stidx:].find(':')
			username = text[stidx+1: edidx+2]
			content = text[edidx+3:]
			return username, content
		else :
			return None, None

	def convertDate(self, timestr) :
		week, month, day, detailtime, temp, year = timestr.split(' ')
		strtime = year + '-' + month + '-' + day + '_' + detailtime
		nowtime = time.mktime(time.strptime(strtime, '%Y-%b-%d_%H:%M:%S'))
		reference = time.mktime(time.strptime("2015-01-01", "%Y-%m-%d"))
		span = int(nowtime-reference)
		return span


if __name__ == '__main__' :
	weibo = Weibo()
	# weibolist = weibo.getNewWeiboList(1000)
	# weibo.writeWeiboList(weibolist)
	weibo.getCommentsList('3880506963620373')