'''
Author: James Thomason
'''
#  Scatter plot, Average Digs per set to W/L % in division 3 2021 Season. No regression line
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import requests
link_data = "https://hawaiiathletics.com/sports/mens-volleyball/stats/2022"

def scrape_website_wl(link):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    r = requests.post(link, headers=header,
                  data={"sport_code": "MVB",
                        "academic_year": float(2021),
                        "division": 3.0,
                        "game_high":"N",
                        "org_id": -1,
                        "stat_seq": 530,
                        "conf_id": -1
                        })
    return r.text
    
def scrape_website_digs(link):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    r = requests.post(link, headers=header,
                  data={"sport_code": "MVB",
                        "academic_year": float(2021),
                        "division": 3.0,
                        "game_high":"N",
                        "ranking_summary":"N",
                        "org_id": -1,
                        "stat_seq": 533,
                        "conf_id": -1
                        })
    return r.text

def get_table_from_text_digs(text):
    df = pd.read_html(text)
    actual_digs = df[1]
    actual_digs["Digs Per Set"] = actual_digs["Per Set"]
    actual_digs = actual_digs.loc[:,["Team","Digs Per Set"]]
    return actual_digs

def get_table_from_text_wl(text):
    df = pd.read_html(text)
    actual_wl = df[1]
    actual_wl["Win Pct."] = actual_wl["Pct."]
    actual_wl = actual_wl.loc[:,["Team","Win Pct."]]
    return actual_wl

def merge_both_into_one_df(df1,df2):
    sorted_by_team_df1 = df1.sort_values(by=["Team"],ascending=False)
    sorted_by_team_df2 = df2.sort_values(by=["Team"],ascending=False)
    sorted_by_team_merged = sorted_by_team_df1
    sorted_by_team_merged["Win Pct."] = sorted_by_team_df2["Win Pct."]
    sorted_by_team_merged = sorted_by_team_merged.reset_index(drop=True)
    return sorted_by_team_merged
    
def make_plot(merged_df):
    plt.plot(merged_df["Digs Per Set"],merged_df["Win Pct."], 'o', linewidth=3)
    plt.grid(True)
    plt.xlabel("Average Digs per Set", fontsize=14)
    plt.ylabel("Win Pct.", fontsize=14)
    plt.title("Average Digs per Set vs Win Pct. in Div. III Mens College Volleyball 2021 Season")
    
    
def main():
    link = "http://stats.ncaa.org/rankings/change_sport_year_div"
    digs_2021 = scrape_website_digs(link)
    wl_2021 = scrape_website_wl(link)
    
    wl_2021_scraped = get_table_from_text_wl(wl_2021) # Some teams played MUCH more than other teams
    digs_2021_scraped = get_table_from_text_digs(digs_2021)
    
    merged = merge_both_into_one_df(digs_2021_scraped,wl_2021_scraped)
    
    make_plot(merged)
    plt.show()

    


if __name__ == "__main__":
    main()
