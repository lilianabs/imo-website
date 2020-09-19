# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from scrapper_imo import IMOWebsiteScrapper
import os
import errno

def main():
    try:
        os.makedirs('../data')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
    sc = IMOWebsiteScrapper()
    sc.get_all_tables()
    
    
if __name__ == '__main__':
    main()