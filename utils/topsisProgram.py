import pandas as pd
import numpy as np
import streamlit as st

def checkValidation(df,weights,criteria,result_file) :
    if weights.__contains__(',') == False:
        st.error("Weights should be separated by comma")
        return False
    if criteria.__contains__(',') == False:
        st.error("Impacts should be separated by comma")
        return False
    if result_file.__contains__('.csv') == False:
        st.error("Result file should be csv")
        return False
    weights = weights.split(',')
    criteria = criteria.split(',')
    weights = [float(x) for x in weights]
    rows,cols = df.shape
    if cols<3:
        st.error("File should have atleast 3 columns")
        return False
    if(len(weights) != cols-1):
        st.error("Number of weights should be " + str(cols-1))
        return False
    if(len(criteria) != cols-1):
        st.error("Number of criteria should be " + str(cols-1))
        return False
    return True


def topsis(df, weights, criteria,result_file):
    weights = weights.split(',')
    criteria = criteria.split(',')
    weights = [float(x) for x in weights]
    df2 = df.iloc[:, 1:]
    
    df2 = df2.apply(lambda x: x / np.sqrt(np.sum(np.square(x))), axis=0)
    
    df2 = df2 * weights
    
    rows, cols = df2.shape
    df2_ideal_best = []
    df2_ideal_worst = []

    for i in range(cols):
        if criteria[i] == '-':
            df2_ideal_best.append(df2.iloc[:, i].min())
            df2_ideal_worst.append(df2.iloc[:, i].max())
        else:
            df2_ideal_best.append(df2.iloc[:, i].max())
            df2_ideal_worst.append(df2.iloc[:, i].min())
    df2_s_best = []
    df2_s_worst = []
    for i in range(rows):
        df2_s_best.append(np.sqrt(np.sum(np.square(df2.iloc[i, :] - df2_ideal_best))))
        df2_s_worst.append(np.sqrt(np.sum(np.square(df2.iloc[i, :] - df2_ideal_worst))))

    topsis_score = [x/(x+y) for x, y in zip(df2_s_worst, df2_s_best)]

    sorted_score = sorted(topsis_score, reverse=True)

    topsis_rank = [sorted_score.index(x)+1 for x in topsis_score]

    df = df.assign(topsis_score=topsis_score, topsis_rank=topsis_rank)
    df = df.rename(columns={'topsis_score': 'Topsis Score', 'topsis_rank': 'Rank'})
    df.to_csv(result_file, index=False)
    
