#! /usr/bin/env python3
# coding: utf-8

import os
import pprint
import logging as lg
import datetime as dt

import pandas as pd
import matplotlib as mil
mil.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

AGE_COLUMN_NAME = "age"
AGE_YEARS_COLUMN_NAME = "age_in_years"
BIRTH_COLUMN_NAME = "birth"
MINIMUM_MP_AGE = 18

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

    @property
    def number_of_mps(self):
        return len(self.dataframe)

    @number_of_mps.setter
    def number_of_mps(self, value):
        raise Exception("You can not set the number of MPs!")

    @classmethod
    def _register_parties(cl, parties):
        cl.ALL_REGISTERED_PARTIES = cl._group_two_lists_of_parties(cl.ALL_REGISTERED_PARTIES, list(parties))

    @classmethod
    def get_all_registered_parties(cl):
        return cl.ALL_REGISTERED_PARTIES

    @staticmethod
    def _group_two_lists_of_parties(original, new):
        return list(set(original + new))

    def number_mp_by_party(self):
        data = self.dataframe
        result = {}

        for party in self.get_all_registered_parties():
            mps_of_this_party = data[data["parti_ratt_financier"] == party]
            result[party] = len(mps_of_this_party)

        return result

    @staticmethod
    def display_histogram(values):
        fig, ax = plt.subplots()
        ax.hist(values, bins = 20)
        plt.title("Ages ({} MPs)".format(len(values)))
        plt.show()

    def _compute_age_column(self):
        now = dt.datetime.now()
        data = self.dataframe

        if not BIRTH_COLUMN_NAME in data.columns:
            data[BIRTH_COLUMN_NAME] = \
                data["date_naissance"].apply(lambda string: dt.datetime.strptime(string, "%Y-%m-%d"))

        if not AGE_COLUMN_NAME in data.columns:
            data[AGE_COLUMN_NAME] = data[BIRTH_COLUMN_NAME].apply(lambda date: now-date)

        new_column = []
        for age in data[AGE_COLUMN_NAME]:
            # age is of type datetime.timedelta (because it was
            # calculated from a difference between two dates)
            # Here, we want to convert it to an integer containing
            # the the age, expressed in years.
            age_in_years = int(age.days / 365)
            new_column += [age_in_years]
        data[AGE_YEARS_COLUMN_NAME] = new_column

    def split_by_age(self, age_split):
        data = self.dataframe
        self._compute_age_column()
        self.display_histogram(data[AGE_YEARS_COLUMN_NAME].values)

        result = {}

        if age_split < MINIMUM_MP_AGE:
            categ = "Under (or equal) {} years old".format(MINIMUM_MP_AGE)
            s = SetOfParliamentMember(categ)
            s.data_from_dataframe(data)
            result = {categ: s}
        else:
            categ1 = "Under (or equal) {} years old".format(age_split)
            categ2 = "Over {} years old".format(age_split)
            s1, s2 = SetOfParliamentMember(categ1), SetOfParliamentMember(categ2)
            condition = data[AGE_YEARS_COLUMN_NAME] <= age_split
            data1 = data[condition]
            data2 = data[~condition]
            s1.data_from_dataframe(data1)
            s2.data_from_dataframe(data2)
            result = {
                categ1: s1,
                categ2: s2
            }

        return result
