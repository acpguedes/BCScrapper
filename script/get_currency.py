#!/usr/bin/env python3

from BCScrapper import bcscrapper
import argparse
from datetime import datetime


def parse_cli():
    # Process the command line
    parser = argparse.ArgumentParser(
        description='Scrapper de cotação de moedas doBanco Central do Brasil'
    )

    parser.add_argument(
        "-i", "--data_inicial",
        default="",
        help='Defina a data inicial de consulta',
        type=str
    )

    parser.add_argument(
        "-f", "--data_final",
        default=datetime.today().date().isoformat(),
        help='Defina a data inicial de consulta. (default: data atual)',
        type=str
    )

    parser.add_argument(
        "-o", "--output",
        help="Saida",
        default="output.csv",
        type=str
    )
    args = parser.parse_args()
    args.file = input_to_set(parser,args.file)
    return(args)


args = parse_cli()

report = bcscrapper.BCReport(args.data_inicial, args.data_final)

report.report.to_csv(args.output)
