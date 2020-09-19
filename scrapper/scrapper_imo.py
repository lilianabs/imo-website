#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 14:45:06 2020

@author: lilianabs
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

class IMOWebsiteScrapper():
    
    def __init__(self):
        #We save the links to the tables from the IMO Website we want to obtain
        self.IMO_tables = {'Timeline': 'https://www.imo-official.org/organizers.aspx',
                           'Countries': 'https://www.imo-official.org/countries.aspx',
                           'Results': 'https://www.imo-official.org/results.aspx'}
    

    def get_timeline_table(self):
        
        result = requests.get(self.IMO_tables['Timeline'])
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        
        table_columns = []
        
        for col in soup.findAll('th'):
            #We remove the column Contestants since it comprises All,M and F columns
            if not col.find(text=True) == 'Contestants':
                table_columns.append(col.find(text=True))

        table = []

        for row in soup.findAll("tr"):
            cells = row.findAll('td')
            if len(cells) == len(table_columns):
                table.append([cell.find(text=True) for cell in cells])
        
        df = pd.DataFrame(table, columns=table_columns)
        df.to_csv("../data/timeline.csv",index=False)
        
    def get_results_table(self):
        
        result = requests.get(self.IMO_tables['Results'])
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        
        columns_table = [col.find(text=True) for col in soup.findAll('th')]
        
        #The structure of the table needs to be sliced
        #We find and remove the columns that we dont need         
        indices_col_year=[i for i,j in enumerate(columns_table) if j == 'Year']
       
        table = []
       
        for row in soup.findAll("tr"):
            cells = row.findAll('td')
            if len(cells) == len(columns_table[0:indices_col_year[1]]) + 1:
                row_to_append = [cell.find(text=True) for cell in cells]
                #We remove the last element
                table.append(row_to_append[:-1])
        
        df = pd.DataFrame(table, columns=columns_table[0:indices_col_year[1]])
        df.to_csv("../data/results.csv", index=False)


    def get_countries_table(self):
        
        result = requests.get(self.IMO_tables['Countries'])
        src = result.content
        soup = BeautifulSoup(src, 'lxml')

        columns_table = [col.find(text=True) for col in soup.findAll('th')]
        
        table = []

        for row in soup.findAll("tr"):
            cells = row.findAll('td')
            if len(cells) == len(columns_table):
                table.append([cell.find(text=True) for cell in cells])
        
  
        df = pd.DataFrame(table, columns=columns_table)
        
        #We save columns Code and Country
        df[['Code', 'Country']].to_csv("../data/countries.csv",index=False)
        
        
    def get_all_tables(self):
        
        try:

            self.get_timeline_table()
            self.get_results_table()
            self.get_countries_table()
            
            print("IMO website scraped succesfully!")
        except:
            print("Error in the scraping process.")


if __name__=='__main__':
    
    sc = IMOWebsiteScrapper()
    sc.get_all_tables()