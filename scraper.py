import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
import os
import pandas as pd
import json
from datetime import datetime
import pytz
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
#from email.message import EmailMessage


YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  channel_tag = video.find_element(By.ID, 'channel-name')
  channel_name = channel_tag.text

  metadata_tag = video.find_element(By.ID, 'metadata-line')

  view_tag = metadata_tag.find_elements(By.TAG_NAME, 'span')[0]
  views = view_tag.text

  date_tag = metadata_tag.find_elements(By.TAG_NAME, 'span')[1]
  uploaded = date_tag.text

  description_tag = video.find_element(By.ID, 'description-text')
  description = description_tag.text

  return {
    'Title': title,
    'URL': url,
    'Channel': channel_name,
    'Views': views,
    'Uploaded': uploaded,
    'Description': description,
    'Thumbnail': thumbnail_url
  }

def send_email(path, reciever):
  try:
    # updating time and date of scraping
    currentDateAndTime = datetime.now(pytz.timezone('Asia/Kolkata'))
    currentDate = currentDateAndTime.strftime("%Y:%m:%d")
    currentTime = currentDateAndTime.strftime("%H:%M:%S")
        
    #this is new email code
    subject = "Top 10 Trending Videos on Yooutube"
    body = "This is a summary of the top 10 trending videos on Youtube in India as of " + currentDate + " at " + currentTime 
    sender_email = 'thierrytribhuwan@gmail.com'
    recipient_email = "prat10000@gmail.com"
    sender_password = os.environ['GOOGLE_PW']
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    # MIMEMultipart() creates a container for an email message that can hold
    # different parts, like text and attachments and in next line we are
    # attaching different parts to email container like subject and others.
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    body_part = MIMEText(body)
    message.attach(body_part)

    # section 1 to attach file
    with open(path,'rb') as file:
      # Attach the file with filename to the email
      message.attach(MIMEApplication(file.read(), Name="trending.csv"))

      # secction 2 for sending email
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
      server.login(sender_email, sender_password)
      server.sendmail(sender_email, recipient_email, message.as_string())
      server.close()
      print('Email sent successfully')
    
  except:
    print("Something went wrong...")
    
  

if __name__ == "__main__":
  print("Creating driver")
  driver = get_driver()

  print("Fetching trending videos")
  videos = get_videos(driver)
  print(f'Found {len(videos)} videos')

  print('Parsing top 10 videos')
  videos_data = [parse_video(video) for video in videos[:10]]

  print("Saving the data to a CSV")
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv')
  print('Sending an email with the results in a csv file')
  send_email('trending.csv', 'prat10000@gmail.com')
  print('Done')