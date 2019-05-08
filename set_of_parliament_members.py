#! /usr/bin/env python3
# coding: utf-8

import os
import pprint
import logging as lg

import pandas as pd
import matplotlib as mil
mil.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

class SetOfParliamentMember:
    def __init__(self, name):
        self.name = name

    def data_from_csv(self, csv_file):
        self.dataframe = pd.read_csv(csv_file, sep=";")

    def data_from_dataframe(self, dataframe):
        self.dataframe = dataframe

    def display_chart(self):
        data = self.dataframe
        female_mps = data[data.sexe == "F"]
        male_mps = data[data.sexe == "H"]

        counts = [len(female_mps), len(male_mps)]
        counts = np.array(counts)
        nb_mps = counts.sum()
        proportions = counts / nb_mps

        labels = ["Female ({})".format(counts[0]), "Male ({})".format(counts[1])]
        fig, ax = plt.subplots()
        ax.axis("equal")
        ax.pie(
            proportions,
            labels=labels,
            autopct="%1.1f pourcents"
        )
        plt.title("{} ({} MPs)".format(self.name, nb_mps))
        plt.show()

    def split_by_political_party(self):
        result = {}
        data = self.dataframe

        all_parties = data["parti_ratt_financier"].dropna().unique()

        for party in all_parties:
            data_subset = data[data.parti_ratt_financier == party]
            subset = SetOfParliamentMember("MPs from party '{}'".format(party))
            subset.data_from_dataframe(data_subset)
            result[party] = subset

        return result

    def __str__(self):
        names = []
        for row_index, mp in self.dataframe.iterrows():
            names += [mp.nom]
        return str(names)

    def __repr__(self):
        return "SetOfParliamentMember: {} members".format(len(self.dataframe))

    def __len__(self):
        return self.number_of_mps

    def __contains__(self, mp_name):
        return mp_name in self.dataframe["nom"].values

    def __getitem__(self, index):
        try:
            result = dict(self.dataframe.iloc[index])
        except:
            if index < 0:
                raise Exception("Please select a positive index")
            elif index >= len(self.dataframe):
                raise Exception("There are only {} MPs !".format(len(self.dataframe)))
            else:
                raise Exception("Wrong index")
        return result

    def __add__(self, other):
        if not isinstance(other, SetOfParliamentMember):
            raise Exception("Can not add a SetOfParliamentMember with an object of type {}".format(type(other)))

        df1, df2 = self.dataframe, other.dataframe
        df = df1.append(df2)
        df = df.drop_duplicates()

        s = SetOfParliamentMember("{} - {}".format(self.name, other.name))
        s.data_from_dataframe(df)
        return s

    def __radd__(self, other):
        return self

    def __lt__(self, other):
        return self.number_of_mps < other.number_of_mps

    def __gt__(self, other):
        return self.number_of_mps > other.number_of_mps

    def __getattr__(self, attr):
        if attr == "number_of_mps":
            return len(self.dataframe)

    def __setattr__(self, attr, value):
        if attr == "number_of_mps":
            raise Exception("You can not set the number of MPs !")
        self.__dict__[attr] = value

    
def launch_analysis(data_file, by_party = False, displaynames = False, searchname = None, index = None, groupfirst = None):
    sopm = SetOfParliamentMember("All MPs")
    sopm.data_from_csv(os.path.join("data", data_file))
    sopm.display_chart()

    if by_party:
        for party, s in sopm.split_by_political_party().items():
            s.display_chart()

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
        parties_by_size = sorted(parties, reverse = True)

        print()
        print("Info: the {} biggest groups are :".format(groupfirst))
        for p in parties_by_size[0:groupfirst]:
            print(p.name)

        s = sum(parties_by_size[0:groupfirst])

        s.display_chart()
