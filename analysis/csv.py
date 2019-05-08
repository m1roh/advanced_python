#! /usr/bin/env python3
# coding: utf-8

"""
============================================
  Set the SetOfParliamentMember class
============================================
"""

from os import path
import pprint

from set_of_parliament_members import SetOfParliamentMember

def launch_analysis(data_file,
                    by_party=False,
                    info=False,
                    displaynames=False,
                    searchname=None,
                    index=None,
                    groupfirst=None,
                    by_age=None):
    """
    Launch an analysis on the current_mps.csv file
    """
    sopm = SetOfParliamentMember("All MPs")
    sopm.data_from_csv(path.join("data", data_file))
    sopm.display_chart()

    if by_party:
        print("by_party")
        for party, party_set in sopm.split_by_political_party().items():
            print(party)
            party_set.display_chart()

    if info:
        print()
        print(repr(sopm))

    if displaynames:
        print()
        print(sopm)

    if searchname is not None:
        is_present = searchname in sopm
        print()
        print("Testing if {} is present: {}".format(searchname, is_present))

    if index is not None:
        index = int(index)
        print()
        pprint.pprint(sopm[index])

    if groupfirst is not None:
        groupfirst = int(groupfirst)
        parties = sopm.split_by_political_party()
        parties = parties.values()
        parties_by_size = sorted(parties, reverse=True)

        print()
        print("Info: the {} biggest groups are :".format(groupfirst))
        for party in parties_by_size[0:groupfirst]:
            print(party.name)

        party_set = sum(parties_by_size[0:groupfirst])

        party_set.display_chart()

    if by_age is not None:
        groupfirst = int(groupfirst)
        by_age = int(by_age)
        for age_group, party_set in sopm.split_by_age(by_age).items():
            print()
            print("-" * 50)
            print(age_group + ":")
            party_set.display_chart()
            print()
            print("{} : Distribution by party :".format(age_group))
            print()
            pprint.pprint(party_set.number_mp_by_party())


if __name__ == "__main__":
    launch_analysis("current_mps.csv")
