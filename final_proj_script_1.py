'''
Author: James Thomason
'''
# Scatter plot Regression Line, Kills per set to win %  for all teams in 2022, 2022 Stats are NOT FINAL 
# Data is from 4/21/2022
from matplotlib import markers
import pandas as pd
import requests
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

link_data = "http://stats.ncaa.org/rankings/change_sport_year_div"

def pretend_browser(link, year,sport_code,ranking_period=None,stat_seq=None):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    if ranking_period is not None:
        r = requests.post(link, headers=header,
                  data={"sport_code": sport_code,
                        "academic_year": float(year),
                        "division": 1.0,
                        "ranking_period": ranking_period,
                        "org_id": -1,
                        "stat_seq": stat_seq
                        })
    else:
        r = requests.post(link, headers=header,
                    data={"sport_code": sport_code,
                            "academic_year": float(year),
                            "division": 1.0,
                            "team_individual":"T",
                            "game_high": "N",
                            "ranking_summary": "N",
                            "org_id": -1,
                            "stat_seq": stat_seq,
                            "conf_id":-1
                            })
    return r.text

def scrape_text_winloss_pct(text):
    scraped_df = pd.read_html(text)
    actual_data = scraped_df[1]
    actual_data = actual_data.loc[:,["Team","Pct."]]
    actual_data = actual_data.drop(50)
    actual_data = actual_data.reset_index(drop=True)
    return actual_data
    
def scrape_text_klls_per_set(text):
    scraped_kills = pd.read_html(text)
    kill_data = scraped_kills[1]
    kill_data = kill_data.loc[:,["Team","Per Set"]]
    kill_data = kill_data.drop(50)
    kill_data = kill_data.reset_index(drop=True)
    return kill_data
    
def merge_both_df(df1,df2):
    # sort both dataframes by team name
    sorted_by_team_wl = df1.sort_values(by=["Team"],ascending=False)
    sorted_by_team_akps = df2.sort_values(by=["Team"],ascending=False)
    sorted_by_team_wl["Per Set"] = sorted_by_team_akps["Per Set"]
    sorted_by_team_wl = sorted_by_team_wl.reset_index(drop=True)
    return sorted_by_team_wl
    
def make_plot_w_regression_line(merged_df):

    x = pd.Series(merged_df["Per Set"]).astype('float').values
    y = pd.Series(merged_df["Pct."]).astype('float').values
    X = sm.add_constant(x)
    model = sm.OLS(merged_df["Per Set"].astype('float'),X)
    result = model.fit()
    plt.plot(x,y,'o')
    m,b = np.polyfit(x,y,1)
    plt.plot(x, m*x+b, linewidth=4)
    plt.grid(True)
    plt.xlabel("Average Kills per set in the 2022 Season",fontsize=14)
    plt.ylabel("Win Pct. (2021-2022)", fontsize=14)
    plt.title("Average Kills per set vs Win Pct in Div. I Mens College Volleyball (2022 Season)")
    return result

def main():
    link = "http://stats.ncaa.org/rankings/change_sport_year_div"
    year_2022_data_winloss_pct = pretend_browser(link,2022,sport_code="MVB",stat_seq=530)
    year_2022_data_klls_ps = pretend_browser(link,2022,sport_code="MVB",ranking_period=70.0,stat_seq=526)
    wl_pct = scrape_text_winloss_pct(year_2022_data_winloss_pct)
    kps = scrape_text_klls_per_set(year_2022_data_klls_ps)
    merged = merge_both_df(wl_pct,kps)
    make_plot_w_regression_line(merged)
    plt.show()
    


if __name__ == "__main__":
    main()
