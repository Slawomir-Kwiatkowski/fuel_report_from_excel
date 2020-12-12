#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@ author: Sławomir Kwiatkowski
@ date: 2019.10.11
'''

import os
import glob
import locale
import calendar
import pandas as pd
import importlib_resources


class Reports:
	
    def __init__(self):
        self.load_resources()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'Data')
        list_of_files = glob.glob(os.path.join(data_dir, '*.xlsx'))
        latest_file = max(list_of_files, key=os.path.getctime)
        path_to_file = os.path.join(data_dir, latest_file)
        self.df = pd.read_excel(path_to_file)
        self.my_parser()
    
    def load_resources(self):
        self.locale, encoding = locale.getdefaultlocale()
        r = importlib_resources.files('Resources')
        try:
            r_strings = (r / f'strings_{self.locale}.txt').read_text(encoding='utf-8').splitlines()
        except:
            r_strings = (r / f'strings_en_US.txt').read_text(encoding='utf-8').splitlines()
            self.locale = 'en_US'
        self.r_str = dict(x.split(':') for x in r_strings)


    
    def my_parser(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print()
        f_date = self.df['Date'].min()
        l_date = self.df['Date'].max()

        with calendar.different_locale(self.locale):
            print(self.r_str['title'], f'({f_date.day} -  {l_date.day} {calendar.month_abbr[int(l_date.month)]} {l_date.year})')
        self.df['Amount'] = self.df['Amount'].astype(str)
        self.df['Amount'] = self.df['Amount'].str.replace(',', '.')
        self.df['Amount'] = self.df['Amount'].astype(float)
        print()
        print(self.r_str['fuel_total'], self.df['Amount'].sum())
        cars_group = self.df.groupby('Registration number')
        print()
        # print(cars_group['Amount'].sum()) #standard output
        for item in zip(cars_group.groups, cars_group['Amount'].sum().values):
            name, value = item
            print(f'{name}    {value}')


        print()
        while True:
            choice = input(self.r_str['choice'] + ': ')
            os.system('cls' if os.name == 'nt' else 'clear')
            if choice == '/q': raise SystemExit
            if choice == '/m': self.my_parser()
            for key, value in cars_group['Amount']:
                if choice.upper() in key:
                    print(self.r_str['refueling'], key)
                    total = 0
                    for i, v in zip(value.index, value.values):
                        print(f"{self.df.loc[i, 'Date']}   {v}")
                        total +=v
                    print(self.r_str['ref_sum'] + f' {key}: {total}')
                    print()


if __name__ == "__main__":
    reports = Reports()