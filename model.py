

from sklearn import preprocessing
import itertools
import statsmodels.api as sm
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from statsmodels.stats.outliers_influence import variance_inflation_factor



def see_multicollinearity(dataframe, column_list=None):

	if column_list is not None:
		dataframe = dataframe.loc[:, column_list]

	vif = pd.DataFrame()
	# For each column,run a variance_inflaction_factor against all other columns to get a VIF Factor score
	vif["VIF Score"] = [variance_inflation_factor(dataframe.values, i) for i in range(dataframe.shape[1])]
	# label the scores with their related columns
	vif["features"] = dataframe.columns
	vif.round(1)

	return vif

def see_columns_with_nulls(dataframe):
	'''This function returns columns with null values and number of null values'''
	
	# Create a list of columns with null values
	null_cols = dataframe.columns[dataframe.isnull().any()].tolist()

	# Iterate through each column to get number of null values
	for col in null_cols:
		print(f"{col} has {dataframe[col].isnull().sum()} values")

def standardize_x_data(column_list, X_train, X_test):
	'''This function standardizes traning and test data by training calculations'''
	
	# Iterate through each column and adjust column values by train data calculation
	for col in column_list:
		
		X_train[col] = (X_train[col] - X_train[col].mean()) / X_train[col].std()
		X_test[col] = (X_test[col] - X_test[col].mean()) / X_test[col].std()

	return X_train, X_test


def linear_regression_sklearn(x_data, y_data):
	'''This  function applys sklearn linear regression'''
	lin = LinearRegression().fit(x_data, y_data)
	return lin


def linear_regression_sm(x_data, y_data):
    '''This function runs a 'simple' multiple linear regression'''
    # Turn into values
    X = x_data.values
    y = y_data.values
    
    # Add constant
    X = sm.add_constant(X)
    
    mod = sm.OLS(y, X, hascont=True)
    res = mod.fit()
    labels = ['intercept'] + list(x_data.columns)
    return res


# def see_regression_output_as_table(regression, x_data, y_data):
# 	'''This function takes output from regression and shows significant variables'''
# 	summary = regression(x_data, y_data)
# 	p_table = summary.tables[1]
# 	p_table = pd.DataFrame(p_table.data)
# 	p_table.columns = p_table.iloc[0]
# 	p_table = p_table.drop(0)
# 	p_table = p_table.set_index(p_table.columns[0])
# 	p_table['P>|t|'] = p_table['P>|t|'].astype(float)
# 	return p_table

# def see_significant_variables_from_regression(regression, x_data, y_data):
# 	'''This function returns variables whos pvalue is less than 0.05'''
# 	reg_table = see_regression_output_as_table(regression, x_data, y_data)
# 	return list(reg_table.loc[reg_table['P>|t|']<0.05].index)

def grid_search(model, alpha_array, x_data, y_data):
	'''This function finds the best alpha for Ridge or Lasso'''
	grid = GridSearchCV(estimator = model, param_grid = dict(alpha = alpha_array))
	grid.fit(x_data, y_data)
	return grid



def lasso_regression(x_data, y_data, alpha=0.5):
    '''This function runs a lasso regression'''
    # Turn into values
    X = x_data.values
    y = y_data.values
    
    # Add constant
    X = sm.add_constant(X)
    
    # Construct lasso model
    lasso = Lasso(alpha=alpha).fit(x_data, y_data)
    return lasso


def ridge_regression(x_data, y_data, alpha=0.5):
    '''This function runs a ridge regression'''
    # Turn into values
    X = x_data.values
    y = y_data.values
    
    # Add constant
    X = sm.add_constant(X)
    
    # Construct ridge model
    ridge = Ridge(alpha=alpha).fit(x_data, y_data)
    return ridge
    