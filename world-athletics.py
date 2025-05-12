import requests
import time
import json
import mysql.connector
from datetime import datetime
from bs4 import BeautifulSoup
from dbconfig import db_config

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Database connection
database = mysql.connector.connect(**db_config)
cursor = database.cursor()


# Load the JSON configuration
with open('config.json') as config_file:
    config = json.load(config_file)

REQUEST_DELAY = config["request_delay"]
HEADER = config["header"]
MONTH_DICT = config["month_dict"]
EVENT_DICT = config["event_dict"]
FIELD_EVENTS = config["field_events"]

# Converts race date and date of birth to a sql friendly date
def convert_date(date):
    date_parts = date.split(" ")

    # For athletes who don"t have a birthday listed on WA
    if len(date_parts) != 3:
        return None
    
    date_day = date_parts[0]
    date_month = MONTH_DICT.get(date_parts[1].upper())
    date_year = date_parts[2]
    date_full = f"{date_year}-{date_month}-{date_day}" 
    return date_full

def extract_country_code(race_location):
    if "(" in race_location and ")" in race_location:
        start = race_location.find("(") + 1
        end = race_location.find(")")
        return race_location[start:end]
    else:
        return None

# Converts a mark to total seconds (e.g., "4:35.25" to 275.25, or "1:09:05.71" to 4145.71)
def convert_mark_to_seconds(mark):
    parts = mark.split(":")
    try:
        if len(parts) == 3:
            # Format: H:MM:SS.ss
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:
            # Format: M:SS.ss
            minutes = int(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        else:
            # Format: SS.ss
            return float(mark)
    except ValueError:
        return None
    

def get_total_pages(event_id, category, event_url_name, gender, todays_date):
    url = f"https://worldathletics.org/records/all-time-toplists/{category}/{event_url_name}/all/{gender}/senior?regionType=world&timing=electronic&bestResultsOnly=false&firstDay=1899-12-29&lastDay={todays_date}&maxResultsByCountry=all&eventId={event_id}&ageCategory=senior"
    response = requests.get(url, headers=HEADER, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Look for the last page button
        last_page_button = soup.find("a", class_="btn--pagination btn--pag-last pag-control")
        if last_page_button:
            # Extract the page number from the 'data-page' attribute
            total_pages = int(last_page_button.get("data-page"))
            return total_pages
        else:
            # Assume there's only one page
            return 1
    else:
        print(f"Failed to fetch the page count for event {event_url_name}, status code: {response.status_code}")
    
# Used for duration
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def create_database():

    # Create and use database
    create_db_query = "CREATE DATABASE IF NOT EXISTS world_athletics"

    # Create table
    create_table_query = """
            CREATE TABLE IF NOT EXISTS results (
                result_id INT AUTO_INCREMENT PRIMARY KEY,
                athlete VARCHAR(100) NOT NULL,
                nationality VARCHAR(3) NOT NULL,
                date_of_birth DATE NULL,
                gender ENUM("Men", "Women", "Mixed") NOT NULL,
                event VARCHAR(20) NOT NULL,
                mark VARCHAR(20) NOT NULL,
                mark_in_seconds DECIMAL(10, 2) NULL,
                wind DECIMAL(4, 1) NULL,
                environment ENUM("Indoor", "Outdoor", "Road") NOT NULL,
                race_location VARCHAR(255) NULL,
                race_date DATE NOT NULL,
                score VARCHAR(4) NULL,
                UNIQUE(athlete, nationality, event, mark, race_date, race_location)
            );
        """
    cursor.execute(create_db_query)
    cursor.execute(create_table_query)
    database.commit()

def scrape_results():
    try:
        create_database()
        todays_date = datetime.now().strftime("%Y-%m-%d")
        todays_time = datetime.now().strftime("%H:%M:%S")
        total_time_start = time.time()
        for event_id, (event, event_url_name, category, gender) in EVENT_DICT.items():
            row_count = 0
            start_time = time.time()
            total_pages = get_total_pages(event_id, category, event_url_name, gender, todays_date)
            print(f"[{todays_time}] Fetching and scraping {total_pages} pages of World Athletics data for {gender}'s {event}")
            for page in range(1, total_pages + 1):

                url = f"https://worldathletics.org/records/all-time-toplists/{category}/{event_url_name}/all/{gender}/senior?regionType=world&timing=electronic&page={page}&bestResultsOnly=false&firstDay=1899-12-29&lastDay={todays_date}&maxResultsByCountry=all&eventId={event_id}&ageCategory=senior"
                response = requests.get(url, headers=HEADER, verify=False)
                soup = BeautifulSoup(response.text, "html.parser")
                
                if response.status_code == 200:
                    rows = soup.find_all("tr")
                    for row in rows:
                        columns = row.find_all("td")
                        if columns:
                            
                            athlete = columns[3].text.strip()
                            nationality = columns[5].text.strip()
                            date_of_birth = columns[4].text.strip()
                            date_of_birth = convert_date(date_of_birth)
                            mark = columns[1].text.strip()
                            if event not in FIELD_EVENTS:
                                mark_in_seconds = convert_mark_to_seconds(mark.replace('h', '')) # remove hand-timed before converting to seconds
                            else:
                                mark_in_seconds = None
                            wind = columns[2].text.strip()
                            if wind == "":
                                wind = None
                            race_location = columns[8].text.strip()
                            if "road-running" in url or "k RW" in event:
                                environment = "Road"
                            else:
                                if "(i)" in race_location: # check (i) before extracting country code which gets rid of it
                                    environment = "Indoor"
                                else:
                                    environment = "Outdoor"
                            race_location = extract_country_code(race_location)
                            race_date = columns[9].text.strip()
                            race_date = convert_date(race_date)
                            score = columns[10].text.strip()

                            try:
                                insert_query = "INSERT INTO results (athlete, nationality, date_of_birth, gender, event, mark, mark_in_seconds, wind, environment, race_location, race_date, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                cursor.execute(insert_query, (athlete, nationality, date_of_birth, gender, event, mark, mark_in_seconds, wind, environment, race_location, race_date, score))
                                database.commit()
                                row_count += 1
                            except mysql.connector.Error as err:
                                if err.errno == 1062:  # Duplicate entry code
                                    continue
                                else: # Break on other error types
                                    print("MySQL Insert Error:", err)
                                    print(f"Offending row: {athlete} ({event}, {mark}) on {race_date}")
                                    break 

                else:
                    print(f"Failed to fetch page {page} for event {gender}'s {event}, status code: {response.status_code}")
                
                time.sleep(REQUEST_DELAY)
            
            total_time_end = time.time()
            total_duration = total_time_start - total_time_end

            end_time = time.time()
            duration = end_time - start_time
            print(f"[{todays_time}] {gender}'s {event} data processed and uploaded. {row_count} new row(s) added to the database in {convert(duration)}.")
        print(f"Finished processing World Athletics database {convert(total_duration)}. Exiting...")
        exit()

    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    try:
        scrape_results()
    finally:
        cursor.close()
        database.close()

if __name__ == "__main__":
    main()