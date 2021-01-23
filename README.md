# BCSrapper

Package to fetch data of currency exchange of USD and EUR against BRL from [Banco Central do Brasil](https://www.bcb.gov.br/).

## Installation
> pip3 install git+https://github.com/acpguedes/BCScrapper.git

## Usage:
```{python3}
from . BCScrapper.bcscrapper import BCCambio, BCReport
from datetime import datetime, timedelta

today = datetime.today()

less_ten_days = timedelta(10)
less_twenty_days = timedelta(20)

ten_days_before = today - less_ten_days
twenty_days_before = today - less_twenty_days

ten_days_before = ten_days_before.date().isoformat()
twenty_days_before = twenty_days_before.date().isoformat()

cambio = BCCambio()
cambio1 = cambio.get_currency(ten_days_before)
cambio2 = cambio.get_currency(twenty_days_before, ten_days_before)

print(cambio1.status_code)
print(cambio1.url)
print(cambio1.text)

print(cambio2.status_code)
print(cambio2.url)
print(cambio2.text)

report = BCReport(ten_days_before)
report1 = report.report
print(report1)

report = BCReport(twenty_days_before, ten_days_before)
report2 = report.report
print(report2)
```

See the docker app to run on terminal at https://github.com/acpguedes/BCScrapper_docker.
