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


file_path= "./data/candidate_donations.csv"

def load_file(file_path):
		donation_data=pd.read_csv(file_path)
		X=donation_data[["year","is_after_2016","house","senate","dem","rep","northeast","midwest", "south","west"]].values
		y=donation_data["amount"].values
		return X, y


X, y = load_file("./data/candidate_donations.csv")


x_train,x_test,y_train,y_test=train_test_split(X, y, p)


constant_train = sm.add_constant(x_train)
constant_test = sm.add_constant(x_test)
model=sm.OLS(y_train, constant_train)
results=model.fit()
print(results.summary())
print(results.rsquared)
ypred_tr=results.predict(constant_train)
ypred_t=results.predict(constant_test)
print(eval_measures.mse(ypred_t,y_test))
print(eval_measures.mse(ypred_tr,y_train))
