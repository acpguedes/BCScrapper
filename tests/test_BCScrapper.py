#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from BCScrapper.bcscrapper import BCCambio, BCGetData, BCReport


def request_ok():
    return MagicMock(status_code=200)


def request_fail():
    return MagicMock(status_code=500)


class BCTest(unittest.TestCase):

    def __init__(self):
        self.getdata = BCGetData("http://my.url", {'param1': 'param1', 'param2': 'param2'})
        self.cambio = BCCambio()
        self.report = BCReport()

    """get"""

    @patch('BCScrapper.bcscrapper.request.get', return_value=request_ok())
    def on_request_success(self, mock_request):
        response = self.getdata.get_data
        self.assertEqual(self.getdata.get_data, 200)

    @patch('BCScrapper.bcscrapper.request.get', return_value=request_fail())
    def on_request_error(self, mock_request):
        self.assertIsNone(self.getdata.get_data)

    """report"""

    def test_cambio(self):
        self.assertIsNotNone(self.report.report())


if __name__ == '__main__':
    unittest.main()
