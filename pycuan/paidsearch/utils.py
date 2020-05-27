import numpy as np
import pandas as pd


def number_of_clicks(b, alpha, beta):
    return alpha * (1 - np.exp(-beta * b))


def expenditure(b, alpha, beta):
    return b * number_of_clicks(b, alpha, beta)


def profit(b, alpha, beta, LTV, conv_rate):
    return -number_of_clicks(b, alpha, beta) * (LTV * conv_rate - b)


def total_profit(bids):
    ltv_conv = pd.read_excel('data/hw-kw-ltv-conv.rate-data.xlsx')
    params = pd.read_csv('data/params.csv', index_col=0).T

    alphas = params.iloc[:, 0].values
    betas = params.iloc[:, 1].values
    ltvs = ltv_conv.iloc[:, 1].values
    conv_rates = ltv_conv.iloc[:, 2].values

    prof = 0
    for i in range(len(bids)):
        prof += profit(bids[i], alphas[i], betas[i], ltvs[i], conv_rates[i])
    return prof


def total_expenditure(bids):
    params = pd.read_csv('data/params.csv', index_col=0).T
    alphas = params.iloc[:, 0].values
    betas = params.iloc[:, 1].values

    sm = 0
    for i in range(len(bids)):
        sm += expenditure(bids[i], alphas[i], betas[i])

    return sm
