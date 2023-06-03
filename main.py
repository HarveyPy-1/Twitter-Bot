from twitter_bot import InternetSpeedTwitterBot

CHROME_DRIVER_PATH = "C://Users//don4d//Downloads//Documents//chromedriver_win32//chromedriver.exe"


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.tweet_at_provider()
