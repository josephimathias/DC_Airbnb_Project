import pandas as pd
import numpy as np


def describe_numeric_variables(dataframe, column_list=None):
    '''This function takes an optional list of numeric variables and returns descriptive statistics'''
    if column_list is not None:
        dataframe = dataframe.loc[:,column_list]
    return dataframe.describe()


def describe_categorical_variables(dataframe, column_list=None):
    '''This function takes an optional list of categorical/discrete variables and returns statistics'''
    
    # If a variable list is specified, filter dataframe to only include those
    if column_list is not None:
        dataframe = dataframe.loc[:,column_list]
     
    # Iterate through each column to show some stats
    for col in dataframe.columns:
    	print(f"{col} has {len(dataframe[col].unique())} values")
    	print(dataframe[col].value_counts()[:5])
    	print("\n")


def clean_money_column(dataframe, column):
    '''This function converts a 'believed-to-be' price column to a numeric column'''
    
    # Strips dollar sign and comma and converts to numeric
    dataframe[column+'_clean'] = pd.to_numeric(dataframe[column].str.replace("$","").str.replace(",",""))
    
    return dataframe


def make_dummy_variable_from_categorical_dummy_variable(dataframe, column):
	'''This function takes a column with values of 't'/'f' and converts to 1/0'''

	# Create copy of column: if value is 't' return 1 else 0
	dataframe[column+'_EQ_T'] = np.where(dataframe[column]=='t',1,0)
	return dataframe

def get_dummies(dataframe, column):
	'''This function creates dummy columns from categorical variable
	This is identical to pandas get_dummies EXCEPT we want to keep
	the original column'''
	# Create copy of the column
	column_copy = column+"_EQ"
	dataframe[column_copy] = dataframe[column]

	# Create dummy columns
	dataframe = pd.get_dummies(dataframe, columns=[column_copy], prefix = column_copy, drop_first=True)

	return dataframe

def get_dummies_from_multivalue_column(dataframe, column, character_list=None, sep=","):
	'''This function takes a column with multiple values, gets list of unique values
	and then creates dummy columns.
	Optional char_list argument is specified to strip column of any characters 
	if need be'''

	# Strip characters from column
	if character_list is not None:
		for char in character_list:
			dataframe[column] = dataframe[column].str.replace(char, "")

	# Create list of unique values
	unique_list = list(set([x for l in dataframe[column].str.split(sep) for x in l]))
	unique_list.sort()

	# Iterate through our unique list (except 0th element) to create columns
	for element in unique_list[1:]:
		dataframe[column+"_EQ_"+element] = dataframe[column].apply(lambda x: (element in x)*1)

	return dataframe












