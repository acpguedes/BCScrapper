#!/usr/bin/env python3
import datetime
from typing import Dict, Any, Union

import requests


class BCException(Exception):
    pass


class BCGetData:
    def __init__(self, url, params):
        self.url = url
        self.params = params

    @property
    def get_data(self, tries=10) -> object:
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
                    '%m/%d/%Y', '%m.%d.%Y', '%m,%d,%Y', '%m\%d\%Y')
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

    def get_currency(self, symbol, first_day, last_day=datetime.date.today().isoformat()):
        parameters: Dict[str, Union[str, Any]] = {
            "@moeda": "'%s'" % symbol,
            "@dataInicial": "'%s'" % bc_date_format(first_day),
            "@dataFinalCotacao": "'%s'" % bc_date_format(last_day),
            "$format": self.format
        }

        response = BCGetData(url=self.url, params=parameters)

        return response.get_data
