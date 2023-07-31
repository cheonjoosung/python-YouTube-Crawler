import pandas as pd
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 다운로드 링크: https://sites.google.com/a/chromium.org/chromedriver/downloads
# 최신다운로드 링크 : https://sites.google.com/chromium.org/driver/downloads

def scrape_youtube_data(search_query):
    # Chrome WebDriver 경로 설정 (본인의 경로로 변경해주세요)
    webdriver_path = '/path/to/chromedriver'

    # Headless 모드로 설정하려면 아래 주석을 해제하세요
    # options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

    # 크롬 드라이버 최신 버전 설정
    service = Service(executable_path='./chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # YouTube 검색 결과 페이지 로드
    url = f'https://www.youtube.com/results?search_query={search_query}'
    driver.get(url)

    # 비디오 정보 추출
    video_data = []
    video_elements = driver.find_elements(By.CSS_SELECTOR, 'div#dismissible')
    for element in video_elements:
        title_element = element.find_element(By.ID, 'video-title')
        link_element = element.find_element(By.ID, 'video-title')
        views_element = element.find_element(By.CSS_SELECTOR, 'span.style-scope.ytd-video-meta-block')
        channel_element = element.find_element(By.CSS_SELECTOR, 'div#text-container.style-scope.ytd-channel-name')
        # subscribers_element = element.find_element(By.CSS_SELECTOR,
        #                                            'span#subscriber-count.style-scope.ytd-c4-tabbed-header-renderer')

        # subscribers_element = element.find_element(By.CSS_SELECTOR,
        #                                            'yt-formatted-string#subscriber-count.style-scope.ytd-c4-tabbed-header-renderer')

        video_title = title_element.text
        video_link = link_element.get_attribute('href')
        video_views = views_element.text
        channel_name = channel_element.text
        # channel_subscribers = subscribers_element.text

        video_data.append([video_title, video_link, video_views, channel_name])

    # WebDriver 종료
    driver.quit()

    return video_data


def save_to_csv(data, file_name):
    df = pd.DataFrame(data, columns=['Title', 'Link', 'Views', 'Channel'])
    df.to_csv(file_name, index=False)


if __name__ == '__main__':
    # 검색어 입력 받기
    search_query = input('검색어를 입력하세요: ')

    # 데이터 스크래핑
    video_data = scrape_youtube_data(search_query)

    # 데이터를 CSV로 저장
    file_name = f'{search_query}_youtube_data.csv'
    save_to_csv(video_data, file_name)

    print(f'{file_name} 파일로 데이터를 저장하였습니다.')