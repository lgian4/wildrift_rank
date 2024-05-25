from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import time


def scrape_website(url, latest_timestamp):
    driver = webdriver.Chrome()
    driver.get(url)
    list = []
    ranks = ['diamond', 'master', 'grandmaster', 'challenger']
    roles = ['top', 'jungle', 'mid', 'bot', 'sup']
    elements = driver.find_elements(By.CLASS_NAME, "btn-dan")
    print(len(elements), 'ranks')
    element_index = 0
    if (len(elements) <= 0):
        print("tab not found")
        exit()
    time.sleep(2)
    for element in elements:

        element.click()

        for role in roles:
            tab = driver.find_element(By.CLASS_NAME, "btn-place-" + role)
            tab.click()

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            date_span = soup.find('span', {'id': 'data-time'})

            date_text = clean_text(date_span.text)
            if (date_text == ""):
                print('date not found')
                return
            date_object = datetime.strptime(date_text, "%Y-%m-%d")
            date_timestamp = datetime.timestamp(date_object)
            if (date_timestamp <= latest_timestamp):
                print('data already scraped')
                return list

            ul = soup.find('ul', {'id': 'data-list'})
            li_tags = ul.find_all('li')
            print(role, ranks[element_index], len(li_tags))

            for li in li_tags:
                data = {}
                divs = li.find_all('div')

                data['time_stamp'] = date_timestamp
                data['date'] = date_text
                data['rank_number'] = int(clean_text(divs[0].text))
                data['role'] = role
                data['hero_img_url'] = divs[3].find('img')['src']
                data['hero_name'] = clean_text(divs[2].text)
                data['rank_filter'] = ranks[element_index]
                data['win_rate'] = float(clean_text(divs[4].text))
                data['pick_rate'] = float(clean_text(divs[5].text))
                data['ban_rate'] = float(clean_text(divs[6].text))
                data['created_at'] = datetime.now().timestamp()
                list.append(data)
        element_index += 1

    driver.close()
    return list


def clean_text(text):
    return text.strip().replace('\n\n', '').replace('%', '')


if __name__ == "__main__":
    url = 'https://example.com'
    scrape_website(url)
