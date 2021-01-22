#!/usr/bin/env python3

from . BCScrapper.bcscrapper import BCReport

first_day = '10-10-2020'
last_day = '10-01-2021'
output = 'example.csv'

report = BCReport(first_day, last_day)

report
#.report.to_csv(output)