from insta_post import InstaPost

import urllib.request

account = {
    'username' : 'priya_saxena6969',
    'password' : 'e57156ur',
     'cookies' : []
}

urllib.request.urlretrieve("https://instagram.fdel27-4.fna.fbcdn.net/v/t51.2885-15/e35/271867029_1001272023796524_2195684813557400102_n.webp.jpg?_nc_ht=instagram.fdel27-4.fna.fbcdn.net&_nc_cat=100&_nc_ohc=nbGdDoDe4MkAX8y-Jxq&edm=AABBvjUBAAAA&ccb=7-4&oh=00_AT8o6VoxxuRJIBRWwc0mV99R_biswRrFUXG7lqrls7SjGw&oe=61E9D458&_nc_sid=83d603", "img.png")

post_data = {
    'url' : '/Users/nitinkumar/Documents/instagram-scraper/examples/main_files/img',
    'color' : None, # or leave it as None
    'caption' : 'beauty'
}

# ip = InstaPost(account)
# ip.log_in()

# ip.click_not_now()

# ip.load_img(post_data)
# ip.post_img()

# # if don't want to use cookies
# ip.log_out()
# # else
# ip.close_insta()