from selenium_scraper import scrape_website
from sqlite_manager import save_list_to_sqlite, set_db, get_latest_time_stamp, get_all_champions, save_new_champs


def change_not_insert_champs(new_champs, list):
    if new_champs is None or len(new_champs) == 0:
        return list
    for rank in list:
        champ = [champ for champ in new_champs if champ['chinese']
                 == rank['champ_id']]
        if champ is None:
            continue
        rank['champ_id'] = champ[0]['id']
    return list


if __name__ == "__main__":
    url = 'https://lolm.qq.com/act/a20220818raider/index.html'

    set_db()
    latest_timestamp = get_latest_time_stamp()
    champions = get_all_champions()
    data = scrape_website(url, latest_timestamp, champions)
    new_champs = save_new_champs(data[1])
    list = change_not_insert_champs(new_champs, data[0])
    print("scrape data: ", len(data[0]), "not exist hero",  len(data[1]))
    save_list_to_sqlite(data[0])
    print("Data saved to SQLite")
