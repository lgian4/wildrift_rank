from selenium_scraper import scrape_website
from sqlite_manager import save_list_to_sqlite, run_migrations, get_latest_time_stamp

if __name__ == "__main__":
    url = 'https://lolm.qq.com/act/a20220818raider/index.html'

    run_migrations()
    latest_timestamp = get_latest_time_stamp()
    list = scrape_website(url, latest_timestamp)
    print("scrape data: ", len(list))
    save_list_to_sqlite(list)
    print("Data saved to SQLite")
