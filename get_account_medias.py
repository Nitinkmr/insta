from bs4 import BeautifulSoup
from selenium import webdriver
from insta_post import InstaPost
import os
import requests
import urllib.request

account = {
    'username' : '',
    'password' : '',
     'cookies' : []
}

ip = InstaPost(account)
#ip.log_in()



user_names = ["memezar"]
base_url = "https://www.instagram.com/"
driver = webdriver.Chrome(executable_path="/Users/nitinkumar/Downloads/chromedriver")

posts_list = []

for user_name in user_names:
	url = base_url + user_name + "/"
	driver.get(url)
	soup = BeautifulSoup(driver.page_source,"html.parser")
	#r = requests.get(url)
	#print(r.content)
	#soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
	#print(soup.prettify())
	#table = soup.find('div', attrs = {'class':'v1Nh3.kIKUG._bz0w'}) 

	#print(posts[0])
	#div = posts[0]
	#print(div.findNext('div').findNext('div').findNext('div').findNext('img'))
	for el in soup.findAll('img', attrs = {'srcset' : True})[0:2]:
		#print(el['srcset'])
		#text = el['alt']
		images = el['srcset'].split(",")
		image = images[len(images)-1].split(" ")[0]
		print(image)
		post = {
		'image' : image,
		'caption' : 'Follow @priya_saxena6969 for Funny Memes credits : @' + user_name
		}
		posts_list.append(post)
	
	#for post in posts:
		
ip.log_in();
ip.click_not_now()

# i=0
# for post in posts_list:

# 	image_name = str(i) + ".png"
# 	post_data = {
#     'url' : '/Users/nitinkumar/Documents/instagram-scraper/examples/main_files/' + image_name,
#     'color' : None, # or leave it as None
#     'caption' : post['caption']
# 	}
# 	print(post_data)

# 	urllib.request.urlretrieve(post['image'],image_name )
# 	i = i + 1
# 	ip.load_img(post_data)
# 	ip.post_img()
# 	os.remove(image_name)
# 	ip.wait(10)
# 	#p.click_element('button', 'Cancel')
# 	find_list = [
# 		('a', 'Not Now'),
# 	 	('button', 'Save Info'),
# 	 	('button', 'Cancel'),
# 	  	('button', 'Not Now')

# 	]
	
# 	for element,text in find_list:
# 		try:
# 			ip.click_element(element,text)
# 		except Exception as e:
# 			pass
    	

ip.log_out()
ip.close_insta()


