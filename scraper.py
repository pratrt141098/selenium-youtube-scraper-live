from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
import pandas as pd

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

  
  
  
