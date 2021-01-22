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

def input_to_set(parser,largs):
    # Process sys.stdin
    if sys.stdin.isatty():
        if len(largs) == 0:
            parser.error("No input!")
    elif not "-" in largs:
        largs.insert(0,sys.stdin)

    # Process sys.argv
    myset=set()
    for iohandle in largs:
        try:
            iohandle = open(iohandle, mode="r")
            myset=myset.union(iohandle.read().splitlines())
            iohandle.close
        except:
            try:
                myset=myset.union(iohandle.read().splitlines())
            except:
                if iohandle == "-":
                    if sys.stdin.isatty():
                        parser.error("No input!")
                    else:
                        myset=myset.union(sys.stdin.read().splitlines())
                else:
                    myset.add(iohandle)
    return(myset)


if __name__ == "__main__":
    args = parse_cli()
    report = bcscrapper.BCReport(args.data_inicial, args.data_final)
    report.report.to_csv(args.output)
