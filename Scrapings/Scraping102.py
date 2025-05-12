from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Global list to store DataFrames temporarily
dfs = []

def getmvps(years):
    """
    Downloads MVP award HTML pages for each year in the 'years' list
    and saves them in the 'mvp' directory.
    """
    url = "https://www.basketball-reference.com/awards/awards_{}.html"
    save_dir = "mvp"
    os.makedirs(save_dir, exist_ok=True)  # Ensure directory exists

    for year in years:
        urlmvp = url.format(year)
        res = requests.get(urlmvp)
        file_path = os.path.join(save_dir, f"{year}.html")
        with open(file_path, "w+", encoding="utf-8") as f:
            f.write(res.text)

def getmvpdata(years):
    """
    Parses saved MVP HTML files, extracts the MVP table for each year,
    and concatenates all years into a single CSV file 'mvps.csv'.
    """
    for year in years:
        with open('mvp/{}.html'.format(year), 'r', encoding='utf-8', errors='ignore') as f:
            page = f.read()
            soup = BeautifulSoup(page, "html.parser")
            soup.find('tr', class_="over_header").decompose()  # Remove extra header row
            mvptable = soup.find_all(id='mvp')[0]  # Find the MVP table
            mvp_df = pd.read_html(str(mvptable))[0]
            mvp_df['Year'] = year
            dfs.append(mvp_df)
    mvps = pd.concat(dfs)
    mvps.to_csv("mvps.csv")

def getplayerstats(years):
    """
    Uses Selenium to scrape per-game player stats HTML pages for each year,
    scrolling to load all data, and saves them in the 'player' directory.
    """
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
    for year in years:
        driver = webdriver.Edge()
        driver.get(url.format(year))
        driver.execute_script("window.scrollTo(0, 140000)")  # Scroll to bottom to load all content
        time.sleep(40)  # Wait for content to load
        html = driver.page_source
        save_dir = "player"
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, f"{year}.html")
        with open(file_path, "w+", encoding="utf-8", errors='ignore') as f:
            f.write(html)
        driver.quit()  # Close the browser after each year

def getplayerdata(years):
    """
    Parses saved player stats HTML files, extracts the per-game stats table for each year,
    and concatenates all years into a single CSV file 'players.csv'.
    """
    for year in years:
        with open('player/{}.html'.format(year), 'r', encoding='utf-8', errors='ignore') as f:
            page = f.read()
            soup = BeautifulSoup(page, "html.parser")
            soup.find('tr', class_="thead").decompose()  # Remove extra header row
            player_table = soup.find_all(id='per_game_stats')[0]
            player_df = pd.read_html(str(player_table))[0]
            player_df['Year'] = year
            dfs.append(player_df)
            print(player_df)
    players = pd.concat(dfs)
    players.to_csv("players.csv")

def init():
    years = list(range(1991, 2021))
    """
    Master function to execute all steps in order and print relevant outputs.
    """
    print("Downloading MVP HTML files...")
    getmvps(years)
    print("MVP HTML files downloaded.")

    # Clear dfs before each new data extraction
    global dfs
    dfs = []
    print("Extracting MVP data and saving to CSV...")
    getmvpdata(years)
    print("MVP data extraction complete. Saved as 'mvps.csv'.")

    print("Downloading player stats HTML files (this may take a while)...")
    getplayerstats(years)
    print("Player stats HTML files downloaded.")

    dfs = []
    print("Extracting player stats data and saving to CSV...")
    getplayerdata(years)
    print("Player stats data extraction complete. Saved as 'players.csv'.")

# To run everything in order:
# init()
