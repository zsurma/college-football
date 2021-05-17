#!/usr/bin/env python3

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from bs4 import Comment

class Player:
    '''Player class to obtain statistics for college football athletes.
    
    This class utilizes Sports Reference's CFB site to pull applicable pandas
    data frames. In order to create an instance, the player's first name,
    last name, team name, and years played should be included.
    '''
    def __init__(self, first_name, last_name, team, years):
        self.first_name = first_name
        self.last_name = last_name
        self.team = team
        self.years = years
        self.player_url = ''
        
        self.passing_summary = None
        self.rushing_receiving_summary = None
        self.punting_kicking_summary = None
        self.return_summary = None
        self.defense_summary = None
        self.scoring_summary = None

        print(f'Searching for {self.first_name} {self.last_name} ({self.team}, {self.years})...')
        r = requests.get(f'https://www.sports-reference.com/cfb/search/search.fcgi?search={first_name}+{last_name}')
        soup = BeautifulSoup(r.text, features='lxml')
        search_items = soup.find_all(class_ = 'search-item')
        if search_items:
            # multiple search results match name
            for item in search_items:
                item_str = str(item).lower()
                if f'{self.first_name.lower()} {self.last_name.lower()}' in item_str and f'{self.team.lower()}' in item_str and f'{self.years}' in item_str:
                    self.player_url = item_str.split('"')[5]
                elif f'{self.first_name.lower()} {self.last_name.lower()}' in item_str and f'{self.team.lower()}' in item_str:
                    print('Year does not match any results. Choosing match by name and team.')
                    self.player_url = item_str.split('"')[5]
            if self.player_url == '':
                raise Exception('Player not found. Please make sure that name, school, and years are correct.')
            
            # potentially fix years... TODO: change this for transfers!!
            r = requests.get(f'https://www.sports-reference.com{self.player_url}')
            soup = BeautifulSoup(r.text, 'lxml')
            year_team_tag = soup.find('a', class_='poptip default')
            year_team = str(year_team_tag['data-tip'])
            if f'{self.team} {self.years}' not in year_team:
                text_list = year_team.split()
                self.years = text_list[-1]
                print(f'Years changed to {self.years}.')
        else:
            # check for no search results condition
            for p in soup.find_all('p'):
                if '0 hits' in p.get_text():
                    raise Exception('Player not found. Please make sure that name, school, and years are correct.')
            # already got to player page!
            full_tag = soup.find('a', text=re.compile('(.*)Overview'))
            self.player_url = full_tag['href']
            
            # potentially fix name
            tag_text = full_tag.get_text()
            if f'{self.first_name} {self.last_name} Overview' not in tag_text:
                text_list = full_tag.get_text().split()
                self.first_name = text_list[0]
                self.last_name = text_list[1]
                print(f'Name changed to {self.first_name} {self.last_name}.')

            # potentially fix school and years
            year_team_tag = soup.find('a', class_='poptip default')
            year_team = str(year_team_tag['data-tip'])
            if f'{self.team} {self.years}' not in year_team:
                text_list = year_team.split()
                self.team = ' '.join(text_list[0:-1])
                self.years = text_list[-1]
                print(f'Team changed to {self.team}, years changed to {self.years}.')

        print(f'Found {self.first_name} {self.last_name} ({self.team}, {self.years}).')


    def get_passing_summary(self):
        '''Get passing statistics for the player.

        This method will return a pandas data frame created with the passing
        table on the site. If no passing statistics are available, the method
        will raise an error.
        '''
        if self.passing_summary is None:
            r = requests.get(f'http://www.sports-reference.com{self.player_url}')
            soup = BeautifulSoup(r.text, 'lxml')
            
            if soup.find(id='passing'):
                self.passing_summary = pd.read_html(str(soup.find(id='passing')))[0].fillna(0)
            else:
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    if 'id="passing"' in str(comment):
                        self.passing_summary = pd.read_html(str(comment))[0].fillna(0)
            
            if self.passing_summary is None:
                raise Exception(f'No passing stats available for {self.first_name} {self.last_name}.')
        return self.passing_summary


    def get_rushing_receiving_summary(self):
        '''Get rushing/receiving statistics for the player.

        This method will return a pandas data frame created with the rushing/
        receiving table on the site. If no rushing/receiving statistics are
        available, the method will raise an error.
        '''
        if self.rushing_receiving_summary is None:
            r = requests.get(f'http://www.sports-reference.com{self.player_url}')
            soup = BeautifulSoup(r.text, 'lxml')
            
            if soup.find(id='rushing'):
                self.rushing_receiving_summary = pd.read_html(str(soup.find(id='rushing')))[0].fillna(0)
            else:
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    if 'id="rushing"' in str(comment):
                        self.rushing_receiving_summary = pd.read_html(str(comment))[0].fillna(0)
            
            if self.rushing_receiving_summary is None:
                raise Exception(f'No rushing or receiving stats available for {self.first_name} {self.last_name}.')
        return self.rushing_receiving_summary


    def get_punting_kicking_summary(self):
        '''Get punting/kicking statistics for the player.

        This method will return a pandas data frame created with the punting/
        kicking table on the site. If no punting/kicking statistics are 
        available, the method will raise an error.
        '''
        if self.punting_kicking_summary is None:
            r = requests.get(f'http://www.sports-reference.com{self.player_url}')
            soup = BeautifulSoup(r.text, 'lxml')
            
            if soup.find(id='punting'):
                self.punting_kicking_summary = pd.read_html(str(soup.find(id='punting')))[0].fillna(0)
            else:
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    if 'id="punting"' in str(comment):
                        self.punting_kicking_summary = pd.read_html(str(comment))[0].fillna(0)
            
            if self.punting_kicking_summary is None:
                raise Exception(f'No punting or kicking stats available for {self.first_name} {self.last_name}.')
        return self.punting_kicking_summary


    def get_return_summary(self):
        '''Get return statistics for the player.

        This method will return a pandas data frame created with the return 
        table on the site. If no return statistics are available, the method
        will raise an error.
        '''
        if self.return_summary is None:
            r = requests.get(f'http://www.sports-reference.com{self.player_url}')
            soup = BeautifulSoup(r.text, 'lxml')
            
            if soup.find(id='punt_ret'):
                self.return_summary = pd.read_html(str(soup.find(id='punt_ret')))[0].fillna(0)
            else:
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    if 'id="punt_ret"' in str(comment):
                        self.return_summary = pd.read_html(str(comment))[0].fillna(0)
            
            if self.return_summary is None:
                raise Exception(f'No return stats available for {self.first_name} {self.last_name}.')
        return self.return_summary


    def get_defense_summary(self):
        '''Get defensive statistics for the player.

        This method will return a pandas data frame created with the defense 
        table on the site. If no defensive statistics are available, the method
        will raise an error.
        '''
        if self.defense_summary is None:
            r = requests.get(f'http://www.sports-reference.com{self.player_url}')
            soup = BeautifulSoup(r.text, 'lxml')
            
            if soup.find(id='defense'):
                self.passing_summary = pd.read_html(str(soup.find(id='defense')))[0].fillna(0)
            else:
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    if 'id="defense"' in str(comment):
                        self.defense_summary = pd.read_html(str(comment))[0].fillna(0)
            
            if self.defense_summary is None:
                raise Exception(f'No defensive stats available for {self.first_name} {self.last_name}.')
        return self.defense_summary


    def get_scoring_summary(self):
        '''Get scoring statistics for the player.

        This method will return a pandas data frame created with the scoring
        table on the site. If no scoring statistics are available, the method
        will raise an error.
        '''
        if self.scoring_summary is None:
            r = requests.get(f'http://www.sports-reference.com{self.player_url}')
            soup = BeautifulSoup(r.text, 'lxml')
            
            if soup.find(id='scoring'):
                self.scoring_summary = pd.read_html(str(soup.find(id='scoring')))[0].fillna(0)
            else:
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                for comment in comments:
                    if 'id="scoring"' in str(comment):
                        self.scoring_summary = pd.read_html(str(comment))[0].fillna(0)
            
            if self.scoring_summary is None:
                raise Exception(f'No scoring stats available for {self.first_name} {self.last_name}.')
        return self.scoring_summary

    def get_game_logs(self, year):
        '''Get game logs for a given year.

        This method will return a pandas data frame with specific game
        information for the given year. If the year is not within the player's
        career range, it will raise an error.
        '''
        year_range = []
        split_years = self.years.split('-')
        if len(split_years) > 1:
            year_range = list(range(int(split_years[0]), int(split_years[1]) + 1))

        if year not in year_range:
            raise Exception(f'No game logs available for {year}.')

        r = requests.get(f'http://www.sports-reference.com{self.player_url.split(".")[0]}/gamelog/{year}')
        soup = BeautifulSoup(r.text, 'lxml')
        
        return pd.read_html(str(soup.find(id='gamelog')))[0].fillna(0)


    def get_splits(self, year):
        '''Get season splits for a given year.

        This method will return a pandas data frame with season split
        information for the given year. If the year is not within the player's
        career range, it will raise an error.
        '''
        year_range = []
        split_years = self.years.split('-')
        if len(split_years) > 1:
            year_range = list(range(int(split_years[0]), int(split_years[1]) + 1))

        if year not in year_range:
            raise Exception(f'No splits available for {year}.')

        r = requests.get(f'http://www.sports-reference.com{self.player_url.split(".")[0]}/splits/{year}')
        soup = BeautifulSoup(r.text, 'lxml')
        
        return pd.read_html(str(soup.find(id='splits')))[0].fillna(0)


if __name__ == '__main__':
    # example is Julian Edelman, incorrect team and years chosen to
    # showcase flexibility in search
    p = Player('Julian', 'Edelman', 'Ohio State', '2018-2020')
    print(p.player_url)
    print(p.last_name)
    print(p.get_passing_summary())
    print(p.get_rushing_receiving_summary())
    print(p.get_punting_kicking_summary())
    print(p.get_return_summary())
    print(p.get_defense_summary())
    print(p.get_scoring_summary())
    print(p.get_game_logs(2008))
    print(p.get_splits(2008))
