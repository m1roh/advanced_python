#! /usr/bin/env python3
# coding: utf-8
import argparse
import logging as lg
import re

import analysis.csv as c_an
import analysis.xml as x_an

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--byage", help="""displays a graph for the MPs splitted between those who are over and those who are under the value of --byage""")
    parser.add_argument("-d","--datafile",help="""CSV file containing pieces of information about the members of parliament""")
    parser.add_argument("-e", "--extension", help="""Kind of file to analyse. Is it a CSV or an XML?""")
    parser.add_argument("-g","--groupfirst", help="""displays a graph groupping all the 'g' biggest political parties""")
    parser.add_argument("-i","--info", action='store_true', help="""information about the file""")
    parser.add_argument("-I","--index", help="""displays information about the Ith mp""")
    parser.add_argument("-n","--displaynames", action='store_true', help="""displays the names of all the mps""")
    parser.add_argument("-p","--byparty", action='store_true', help="""displays a graph for each political party""")
    parser.add_argument("-s","--searchname", help="""search for a mp name""")
    parser.add_argument("-v", "--verbose", action='store_true', help="""Make the application talk!""")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.verbose:
        lg.basicConfig(level=lg.DEBUG)

    try:
        datafile = args.datafile
        if datafile == None:
            raise Warning("You must indicate a datafile !")
    except Warning as e:
        lg.warning(e)
    else:
        try:
            e = re.search(r'^.+\.(\D{3})$', args.datafile)
            extension = e.group(1)

            if extension == "xml":
                x_an.launch_analysis(datafile)
            elif extension == "csv":
                c_an.launch_analysis(datafile, args.byparty, args.info, args.displaynames, args.searchname, args.index, args.groupfirst, args.byage)
        except FileNotFoundError as e:
            lg.error("Ow :( The file was not found. Here is the original message of the exception : {}".format(e))
        finally:
            lg.info('#################### Analysis is over ######################')


if __name__ == "__main__":
    main()
