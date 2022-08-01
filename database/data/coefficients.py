import pandas as pn
import statsmodels.formula.api as sm


def calculate_coefficients(value=[], k=[]):
    dates = {
        "value": value,
        "c": k,
    }
    dataframe = pn.DataFrame(dates).dropna()
    result = sm.ols(formula="value ~ c", data=dataframe).fit()
    coefficient = result.params['c']
    intercept = result.params['Intercept']
    correlation = dataframe.dropna().corr()['value']['c']

    return {'coefficient': coefficient, 'intercept': intercept, 'correlation': correlation}
