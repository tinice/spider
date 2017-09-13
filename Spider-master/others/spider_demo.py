import requests
from bs4 import BeautifulSoup
url="http://news.qq.com/world_index.shtml"
res=requests.get(url)
res.enconding='utf-8'
html_example=res.text
soup=BeautifulSoup(html_example,'html.parser')
#找到所有id为title的元素
header=soup.select('title')
print(header[0].text)
#找到所有class为text的元素，注意class前面的.
article=soup.select('.text')
for txt in article:
	#print(txt.text)
	pass
#找到所有tag为link的href链接
alinks=soup.select('a')
for link in alinks:
	print(link['href'])


test=soup.select('.linkto')
for case in test :
	try:
		print(case.text)
	except KeyError as e:
		pass
	