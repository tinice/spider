from bs4 import BeautifulSoup
import requests

def get_news_general(url):
	'''get news title and url'''
	web = requests.get(url)
	web.enconding='utf-8'
	soup = BeautifulSoup(web.text,'html.parser')
	title_url={}
	text=[]
	for new in soup.select('.linkto'):
		title_url[new.text]=new['href']	
	return title_url;
def get_news_detail(title_url):
	'''get every url detail include contents,time,source website and write to file'''
	for title,link in title_url.items():
		new_link=requests.get(link)
		new_link.enconding='utf-8'
		new_soup=BeautifulSoup(new_link.text,'html.parser')
		time =new_soup.select('.a_time')
		source_site=new_soup.select('.a_source')
		first=True
		with open('{0}.txt'.format(title),'a') as fobj:
			try:
				fobj.write(source_site[0].text)
				fobj.write(time[0].text)
			except Exception as e:
				pass
			for article in new_soup.select('.text')[1:]:
				if first:
					first=False
				else:
					fobj.write("{0}\n".format(article.text))

		break
		
if __name__ == '__main__':
	url="http://news.qq.com/"
	new_general=get_news_general(url)
	print(new_general)
	get_news_detail(new_general)
	