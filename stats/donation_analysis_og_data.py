# import statsmodels.api as sm
# import statsmodels.formula.api as smf
#
# # M has column headers w/ names
# M = read_data()
# X = sm.add_constant(X)
# eq = “amount ~ race + state + year”
# model = smf.ols(formula=eq, data=M)
# results = model.fit()
# print(results.summary())

import numpy as np
import pandas as pd
import random
import csv
from scipy import stats
import statsmodels.api as sm
from statsmodels.tools import eval_measures

def split_data(data, prob):
    random.shuffle(data)
    total_count=len(data)
    train_count=int((1-prob)*total_count)
    training_pairs=data[:train_count]
    testing_pairs=data[train_count:]
    return training_pairs,testing_pairs


def train_test_split(x, y, test_pct):
    split=split_data(list(zip(x,y)),test_pct)
    x_train=[]
    x_test=[]
    y_train=[]
    y_test=[]
    for tuple in split[1]:
        x_test.append(tuple[0])
        y_test.append(tuple[1])
    for tuple in split[0]:
        x_train.append(tuple[0])
        y_train.append(tuple[1])
    return x_train, x_test, y_train, y_test



if __name__=='__main__':

    random.seed(1)
    p = 0.2


    #file_path= "./candidate_donations.csv"

    def load_file(file_path):
            df=pd.read_csv(file_path, usecols=['race', 'party', 'state', \
            'amount', 'year'])
            # x0 = race, x1 = party, x2 = state, x3 = year
            X = [df['race'].values.tolist(), \
                df['party'].values.tolist(), df['state'].values.tolist(), \
                df['year'].values.tolist()]
            # X=donation_data[["year","is_after_2016","house","dem","rep","Northeast",
            # "Midwest", "South","West"]].values
            y = df['amount'].values.tolist()

            xlen = len(X[0])

            is_house = [0]*xlen
            is_senate = [0]*xlen

            is_dem = [0]*xlen
            is_repub = [0]*xlen

            northeast = [0]*xlen
            midwest = [0]*xlen
            west = [0]*xlen
            south = [0]*xlen

            # region = ['']*xlen

            modified_year = [0]*xlen
            is_after_2016 = [0]*xlen
            is_2020 = [0]*xlen

            for i in range(xlen):
                # parse out x0 = race into separate lists
                race = X[0]
                if race[i] == 'House':
                    is_house[i] = 1
                elif race[i] == 'Senate':
                    is_senate[i] = 1

                #parse out x1 = party into separate lists
                party = X[1]
                if party[i] == 'D':
                    is_dem[i] = 1
                elif party[i] == 'R':
                    is_repub[i] = 1

                # parse out x2=state to region list
                # regions: 0 = Northeast; 1 = Midwest; 2 = West; 3 = South
                state = X[2]
                if state[i] in ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA']:
                    northeast[i] = 1
                elif state[i] in ['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', \
                'IL', 'WI', 'IN', 'OH', 'MI']:
                    midwest[i] = 1
                elif state[i] in ['WA', 'MT', 'WY', 'ID', 'OR', 'CA', 'NV', \
                'UT', 'CO', 'NM', 'AZ']:
                    west[i] = 1
                elif state[i] != '':
                    south[i] = 1

                # parse out x3 = year to modified year (subtract 2010) and is_after_2016
                year = X[3]
                nuyr = year[i] - 2010
                modified_year[i] = nuyr
                if nuyr > 6:
                    is_after_2016[i] = 1
                if nuyr == 10:
                    is_2020[i] = 1
            # insert is_house, is_senate, region, is_after_2016, modified year to X list
            X = [modified_year, is_after_2016, is_house, is_senate, is_dem, \
            is_repub, northeast, midwest, south, west, is_2020]
            # change dimensions of list - yea super hacky but it works?
            xList = []
            for i in range(xlen):
                nulist = []
                for li in X:
                    nulist.append(li[i])
                xList.append(nulist)
            X = xList
            return X, y


    X, y = load_file("../data/candidate_donations.csv")
    X = sm.add_constant(X)
    # print(X)


    x_train,x_test,y_train,y_test=train_test_split(X, y, p)

    model=sm.OLS(y_train, x_train)
    results=model.fit()

    print(results.summary())
    print('R2: ', results.rsquared)

    ypred_tr=results.predict(x_train)
    ypred_t=results.predict(x_test)
    print('test MSE: ', eval_measures.mse(ypred_t,y_test))
    print('train MSE: ', eval_measures.mse(ypred_tr,y_train))
