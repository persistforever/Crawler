# -*- encoding=utf-8 -*-

from weibo import APIClient
import json
import time
import datetime

charset = 'utf-8'

class Weibo :
	# attributes
	APP_KEY = '1464287299' # app key
	APP_SECRET = 'e4d573c77e41118abe06df2628cc4418' # app secret
	CALLBACK_URL = 'http://www.example.com/callback' # callback url
	WEIBOLIST_PATH = '../result/weibolist/'
	INFOLIST_PATH = '../result/infolist/'
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	access_token='2.00v5KI4DFBAGbB4289cec5d0MFFs5B'

	# methods
	def getNewWeiboIdList(self) :
		idlist = []
		for i in range(iternum) :
			try:
				jsondata = self.client.statuses.public_timeline.get(access_token = self.access_token, count=100)
				for weibo in jsondata['statuses'] :
					idlist.append(weibo['id'])
				time.sleep(60)
			except Exception, e:
				print e
				break
		return list(set(idlist))

	def writeWeiboIdList(self, weibolist) :
		now = datetime.date.today().strftime('%Y%m%d')
		name = self.WEIBOLIST_PATH + now + '.txt'
		with open(name, 'w') as fw :
			for weiboid in weibolist :
				fw.writelines(str(weiboid) + '\n')

	# API 1: store weiboid list into /result/weibolist
	def storeWeiboIdList(self) :
		weibolist = self.getNewWeiboIdList()
		self.writeWeiboIdList(weibolist)

	def readWeiboIdfoList(self) :
		idlist = []
		now = datetime.date.today().strftime('%Y%m%d')
		yester = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y%m%d')
		name = self.WEIBOLIST_PATH + yester + '.txt'
		with open(name, 'r') as fo :
			for line in fo.readlines() :
				weiboid = line.strip()
				idlist.append(weiboid)
		return idlist

	def getWeiboInfoList(self, weibolist) :
		infolist = []
		for weiboid in weibolist :
			try :
				jsondata = self.client.statuses.show.get(access_token = self.access_token, id=weiboid)
				infolist.append(str(weiboid) + '#' + str(weibo['comments_count']))
				time.sleep(6)
			except Exception, e:
				print e
				break
		return infolist

	def writeWeiboInfoList(self, infolist) :
		now = time.strftime('%Y%m%d', time.datetime.now())
		yester = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y%m%d')
		name = self.INFOLIST_PATH + yester + '.txt'
		with open(name, 'w') as fw :
			for info in infolist :
				fw.writelines(str(info) + '\n')

	# API 2: store info list into /result/infolist
	def storeWeiboInfoList(self) :
		idlist = self.readWeiboIdfoList()
		infolist = self.getWeiboInfoList(idlist)
		self.writeWeiboInfoList(infolist)

	def getCommentsList(self, weiboid) :
		pair = []
		qalist = []
		for page in range(1, 3) :
			try :
				jsondata = self.client.comments.show.get(access_token = self.access_token, id=weiboid, count=200, page=page)
				for comment in  jsondata['comments'] :
					senduser = comment['user']['screen_name'] # [comment['text']], comment['created_at']
					recvuser, content = self.findReplyComment(comment['text'])
					if recvuser != None :
						pair.append([senduser, recvuser, content])
						qalist.append([senduser, recvuser, content, self.convertDate(comment['created_at'])])
				time.sleep(60)
			except Exception, e :
				break
		return qalist
		# for senduser, recvuser, content, time in qalist :
		# 	print senduser.encode(charset), recvuser.encode(charset), content.encode(charset), time

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

	def extractQtAsPair(self, infolist) :
		qadict = dict()
		for senduser, recvuser, content, time in infolist:
			key = sorted([senduser, recvuser])[0] + '<#>' + sorted([senduser, recvuser])[1]
			if key not in qadict.keys() :
				qadict[key] = []
			qadict[key].append([senduser, recvuser, content, time])
		for key in qadict :
			qadict[key] = sorted(qadict[key], key=lambda x: x[3], reverse=False)
			for senduser, recvuser, content, time in qadict[key] :
				print senduser.encode(charset), recvuser.encode(charset), content.encode(charset), time
			print '-'*20


if __name__ == '__main__' :
	weibo = Weibo()
	# weibo.storeWeiboIdList()
	# weibo.storeWeiboInfoList()
	# infolist = weibo.getCommentsList('3880506963620373')
	# weibo.extractQtAsPair(infolist)