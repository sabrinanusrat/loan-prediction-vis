import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesClassifier
import settings

def read():
    train = pd.read_csv(os.path.join(settings.PROCESSED_DIR, "train.csv"))
    return train

def get_predictors(train, target):
    predictors = train.columns.tolist()
    #predictors = [p for p in predictors if p not in settings.NON_PREDICTORS]
    predictors = [p for p in predictors if p in settings.PREDICTORS[target]]
    return predictors

def removeNegativeRows(train, predictors):
    for column in predictors:
        train = train[(train[column]>=0)]
    return train

def selectKBestFeatures(train, target, k):
    predictors = get_predictors(train, target)
    train = removeNegativeRows(train, predictors)
    X = train[predictors]
    y = train[target]
    #scaler = StandardScaler(with_mean=False)
    #Z = scaler.fit_transform(X)

    #apply SelectKBest class to extract top k best features
    bestfeatures = SelectKBest(score_func=chi2, k=k)
    fit = bestfeatures.fit(X,y)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(X.columns)

    #concat two dataframes for better visualization 
    featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    featureScores.columns = ['Specs','Score']
    print('---------------------------------')
    print('Best features for '+target)
    print('---------------------------------')
    print(featureScores.nlargest(k,'Score'))

def compute_feature_importances(train, target, k):
    predictors = get_predictors(train)
    train = removeNegativeRows(train, predictors)
    X = train[predictors]
    y = train[target]
    scaler = StandardScaler(with_mean=False)
    Z = scaler.fit_transform(X)

    model = ExtraTreesClassifier()
    model.fit(Z,y)
    #use inbuilt class feature_importances of tree based classifiers
    print(model.feature_importances_)
    #plot graph of feature importances for better visualization
    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    feat_importances.nlargest(k).plot(kind='barh')
    plt.show()

def compute_correlation(train):
    predictors = get_predictors(train)
    train = removeNegativeRows(train, predictors)
    data = train[predictors+[settings.FORECLOSURE_TARGET, settings.DELINQUENCY_TARGET]]

    #get correlations of each features in dataset
    corrmat = data.corr()
    top_corr_features = corrmat.index
    plt.figure(figsize=(10,10))
    #plot heat map
    g=sns.heatmap(data[top_corr_features].corr(),annot=True,cmap="RdYlGn")
    plt.show()

def compute_average(train, column, filter_columns, filter_values):
    data = train
    for i in range(len(filter_columns)):
        data = data[(data[filter_columns[i]]==filter_values[i])]
    foreclosure_data = data[(data[settings.FORECLOSURE_TARGET]==True)][column].tolist()
    nonforeclosure_data = data[(data[settings.FORECLOSURE_TARGET]==False)][column].tolist()
    delinquency_data = data[(data[settings.DELINQUENCY_TARGET]==True)][column].tolist()
    nondelinquency_data = data[(data[settings.DELINQUENCY_TARGET]==False)][column].tolist()

    return foreclosure_data, nonforeclosure_data

    #print('Average '+column+' value for forclosure data='+str(sum(foreclosure_data)/len(foreclosure_data)))
    #print('Average '+column+' value for nonforclosure data='+str(sum(nonforeclosure_data)/len(nonforeclosure_data)))
    #print('Average '+column+' value for delinquency data='+str(sum(delinquency_data)/len(delinquency_data)))
    #print('Average '+column+' value for nondelinquency data='+str(sum(nondelinquency_data)/len(nondelinquency_data)))

if __name__ == "__main__":
    train = read()
    #selectKBestFeatures(train, settings.FORECLOSURE_TARGET, 18)
    #selectKBestFeatures(train, settings.DELINQUENCY_TARGET, 18)
    #compute_feature_importances(train, settings.FORECLOSURE_TARGET, 18)
    #compute_feature_importances(train, settings.DELINQUENCY_TARGET, 5)
    compute_correlation(train)
