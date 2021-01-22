#!/usr/bin/env python3

from BCScrapper.bcscrapper import BCCambio, BCReport
from datetime import datetime, timedelta

today = datetime.today()

less_ten_days = timedelta(10)
less_twenty_days = timedelta(20)

ten_days_before = today - less_ten_days
twenty_days_before = today - less_twenty_days

ten_days_before = ten_days_before.isocalendar()
twenty_days_before = twenty_days_before.isocalendar()

cambio = BCCambio()
cambio1 = cambio.get_currency(ten_days_before)
cambio2 = cambio.get_currency(twenty_days_before, ten_days_before)

print(cambio1.status_code)
print(cambio1.url)
print(cambio1.text)

print(cambio2.status_code)
print(cambio2.url)
print(cambio2.text)

report = BCReport()
report1 = report(ten_days_before)
report2 = report(twenty_days_before, ten_days_before)
print(report1)
print(report2)