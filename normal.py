from instabot import Bot


# Initialize the bot
bot = Bot()
bot.login(username="shahwar_alam_naqvi", password="Saninstagram@1")


# Upload a photo and add a caption
photo_path = "D:/Hackathon/TalkToDocument/PostImages/postimage1.jpg"
caption = "Check out this amazing photo! #PythonAutomation"
bot.upload_photo(photo_path, caption=caption) 