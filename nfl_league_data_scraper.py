import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


urls = ['https://www.nfl.com/standings/league/2021/REG',
        'https://www.nfl.com/standings/league/2020/REG',
        'https://www.nfl.com/standings/league/2019/REG',
        'https://www.nfl.com/standings/league/2018/REG',
        'https://www.nfl.com/standings/league/2017/REG',
        'https://www.nfl.com/standings/league/2016/REG',
        'https://www.nfl.com/standings/league/2015/REG',
        'https://www.nfl.com/standings/league/2014/REG',
        'https://www.nfl.com/standings/league/2013/REG',
        'https://www.nfl.com/standings/league/2012/REG',
        'https://www.nfl.com/standings/league/2011/REG',
        'https://www.nfl.com/standings/league/2010/REG',
        'https://www.nfl.com/standings/league/2009/REG',
        'https://www.nfl.com/standings/league/2008/REG',
        'https://www.nfl.com/standings/league/2007/REG',
        'https://www.nfl.com/standings/league/2006/REG',
        'https://www.nfl.com/standings/league/2005/REG',
        'https://www.nfl.com/standings/league/2004/REG',
        'https://www.nfl.com/standings/league/2003/REG',
        'https://www.nfl.com/standings/league/2002/REG',
        'https://www.nfl.com/standings/league/2001/REG',
        'https://www.nfl.com/standings/league/2000/REG']

file_years = ['2021','2020','2019','2018','2017','2016','2015','2014','2013',
              '2012','2011','2010','2009','2008','2007','2006','2005','2004',
              '2003','2002','2001','2000']

def nfl_scrape(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    table = soup.find('table', class_ = "d3-o-table d3-o-table--row-striping d3-o-table--detailed d3-o-standings--detailed d3-o-table--sortable {sortlist: [[4,1]], sortinitialorder: 'desc'}")
    columns = table.find_all('th')

    column_names = []
    for item in columns:
        column_names.append(item.text)

    df = pd.DataFrame(columns=column_names)

    table_rows = table.find_all('tr')[1:] #Exclude the column names

    team_names = [] #Obtain correct team names
    for i in table_rows:
        team = i.find('div', class_ = 'd3-o-club-fullname').text
        team_names.append(team)
        
    junk_tags = ['x','y','z'] #Remove extra tags from team names
    for ii, item in enumerate(team_names):
        if any(ele in item[-3:] for ele in junk_tags):
            split = item.split()
            if len(split[-1]) <= 3:
                del split[-1] #Remove the bad tag
            team_names[ii] = ' '.join(split)

    for j in table_rows: #Add each row of scraped data to the new dataframe
        row_data = j.find_all('td')
        row = [tr.text for tr in row_data]
        df.loc[len(df)] = row
        
    df['NFL Team'] = team_names #Add column of our team names
    
    return df

#File path sandwich! (The file years will go in between these two strings)
file_frontend = 'C:/Users/leave/OneDrive/Documents/Scraped_Datasets/nfl_league_'
file_backend = '.csv'

#Perform the scrape for each year
for i,url in enumerate(urls):
    df = nfl_scrape(url)
    df['Year'] = file_years[i]
    
    df.to_csv(file_frontend + file_years[i] + file_backend, index= False)
    