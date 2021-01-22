#!/usr/bin/env python3

import datetime
from typing import Dict, Any, Union
import requests
import pandas as pd
from io import StringIO


class BCException(Exception):
    pass


class BCGetData:
    def __init__(self, url, params):
        self.url = url
        self.params = params

    @property
    def get_data(self, tries=10) -> requests.models.Response:
        for _ in range(tries):
            try:
                request = requests.get(self.url, self.params)
                if request.status_code != 200:
                    continue
                else:
                    return request
            except requests.RequestException:
                continue


def bc_date_format(text):
    """Formatar datas para o formato aceito pelo BC"""
    date_formats = ('%Y/%m/%d', '%Y-%m-%d', '%Y.%m.%d', '%Y,%m,%d', '%Y\%m\%d',
                    '%Y/%d/%m', '%Y-%d-%m', '%Y.%d.%m', '%Y,%d,%m', '%Y\%d\%m',
                    '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%d,%m,%Y', '%d\%m\%Y',
                    '%m/%d/%Y', '%m.%d.%Y', '%m,%d,%Y', '%m\%d\%Y', '%Y-%m-%d %H:%M:%S.%f')
    for fmt in date_formats:
        try:
            formatted_data = datetime.datetime.strptime(text, fmt)
            assert isinstance(formatted_data, datetime.datetime)
            return formatted_data.strftime('%m-%d-%Y')
        except ValueError:
            pass
    raise ValueError('Formato de data invalido')


def set_period(first_day=None, last_day=None):
    try:
        first_day = bc_date_format(first_day)
        last_day = bc_date_format(last_day)
        assert isinstance(first_day, str)
        assert isinstance(last_day, str)
        return first_day, last_day
    except ValueError:
        pass
    raise ValueError()


class BCCambio:
    """Scrapper de cotação de UDS e EUR do Banco Central"""

    def __init__(self):
        self.url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda," \
                   "dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        self.format = "text/csv"

    def get_currency(self, symbol, first_day, last_day=datetime.date.today().isoformat()) -> requests.models.Response:
        parameters: Dict[str, Union[str, Any]] = {
            "@moeda": "'%s'" % symbol,
            "@dataInicial": "'%s'" % bc_date_format(first_day),
            "@dataFinalCotacao": "'%s'" % bc_date_format(last_day),
            "$format": self.format,
            "$select": 'cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim'
        }

        response = BCGetData(url=self.url, params=parameters)

        return response.get_data


def fix_data(data: requests.models.Response):
    data = pd.read_csv(StringIO(data))
    data['dataHoraCotacao'] = data['dataHoraCotacao'].apply(lambda x: bc_date_format(x))
    data['cotacaoCompra'] = data['cotacaoCompra'].replace(',', '.', regex=True).astype(float)
    data['cotacaoVenda'] = data['cotacaoVenda'].replace(',', '.', regex=True).astype(float)
    assert isinstance(data, pd.core.frame.DataFrame)
    return data


class BCReport:

    def __init__(self, first_day, last_day=datetime.date.today().isoformat()):
        self.first_day = first_day
        self.last_day = last_day

    @property
    def report(self) -> pd.core.frame.DataFrame:
        currency = BCCambio()
        euro = currency.get_currency('EUR', self.first_day, self.last_day)
        dollar = currency.get_currency('USD', self.first_day, self.last_day)
        euro = fix_data(euro.text)[['cotacaoCompra', 'cotacaoVenda', 'dataHoraCotacao']]
        euro.columns = ['euroCompra', 'euroVenda', 'dataHoraCotacao']
        dollar = fix_data(dollar.text)[['cotacaoCompra', 'cotacaoVenda', 'dataHoraCotacao']]
        dollar.columns = ['dollarCompra', 'dollarVenda', 'dataHoraCotacao']
        return dollar.groupby('dataHoraCotacao').mean().merge(euro.groupby('dataHoraCotacao').mean(),
                                                              on='dataHoraCotacao')
