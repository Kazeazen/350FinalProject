'''
Author: James Thomason
'''

# Line Graph, all Big West teams win loss percent from 2017-2022 (Big West conference data isnt listed before 2016)
# 2022 Stats are NOT FINAL STATS.
import pandas as pd
import requests
import statsmodels.api as sm
import matplotlib.pyplot as plt

link_to_stats = "http://stats.ncaa.org/rankings/change_sport_year_div" 

def pretend_browser(link):
    years = [2017,2018,2019,2020,2021,2022]
    win_loss_all_teams = []
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
    for year in years:
        r = requests.post(link, headers=header,
                        data={"sport_code": "MVB",
                                "academic_year": float(year),
                                "division": 1.0,
                                "ranking_period": 70.0,
                                "team_individual":"T",
                                "game_high": "N",
                                "stat_seq": 530,
                                "org_id": -1
                                })
        win_loss_all_teams.append(r.text)
    return win_loss_all_teams

def scrape_request_text_for_big_west(text):
    years = [2018,2019,2020,2021,2022]
    scraped_dataframes_from_r_text_list = []
    only_big_west_data = []
    for data in text:
        scraped_df = pd.read_html(data)
        scraped_dataframes_from_r_text_list.append(scraped_df[1])
    for df in scraped_dataframes_from_r_text_list:
        filtered = df[df["Team"].str.contains("Big West") == True]
        filtered_only_wl_PCT = filtered.loc[:,["Team","Pct."]]
        only_big_west_data.append(filtered_only_wl_PCT)

    only_big_west_data = only_big_west_data[1:]

    for i,df in enumerate(only_big_west_data):
        df["Year"] = years[i]
    merged = pd.concat([only_big_west_data[0],only_big_west_data[1],only_big_west_data[2],only_big_west_data[3],only_big_west_data[4]],axis=0)
    return merged

def get_each_year_by_team(merged_df):
    team_one = merged_df[merged_df["Team"].str.contains("Long Beach") == True]
    team_two = merged_df[merged_df["Team"].str.contains("Hawaii") == True]
    team_three = merged_df[merged_df["Team"].str.contains("UC Irvine") == True]
    team_four = merged_df[merged_df["Team"].str.contains("CSUN") == True]
    team_five = merged_df[merged_df["Team"].str.contains("UC Santa") == True]
    team_six = merged_df[merged_df["Team"].str.contains("UC San Diego") == True]

    return [team_one,team_two,team_three,team_four,team_five,team_six]
    
def make_plot(team_list_by_year):
    plt.figure(figsize=(10,10))
    for team in team_list_by_year:
        plt.plot(team["Year"],team["Pct."], label= team.iloc[0,0][:-10], linewidth=3)
    plt.xticks([2018,2019,2020,2021,2022])
    plt.title("Win pct of teams in Big West Conference by Year",fontsize=14)
    plt.xlabel("Year",fontsize=14)
    plt.ylabel("Win Percentage",fontsize=14)
    plt.legend(bbox_to_anchor=(1.01,1), loc='center', borderaxespad=0)
    plt.grid(True)
    

def main():
    link = "http://stats.ncaa.org/rankings/change_sport_year_div"
    
    url_text = pretend_browser(link)
    big_west_by_year = scrape_request_text_for_big_west(url_text)
    teams_list_by_year = get_each_year_by_team(big_west_by_year)
    make_plot(teams_list_by_year)
    plt.show()



if __name__ == "__main__":
    main()