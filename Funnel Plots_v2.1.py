"""
Python script for creating Funnel Plots to present cross-sectional data (proportions, e.g. crude rates) on county level

@author: Polli85(GitHub)
Version: 2.1

-------
Prerequisites:
    
a. The following data is needed in xlsx-format for input (sheet=tab1). Notice EXACT column names in square brackets:
    number of county [area_id] AND/OR name of county [area_name] 
    number of events [events]
    population [population] 
    
b. Insert paths (3x) for input and output (see main-function).

c. Adjust title, axes etc. for plot (see funnel-function)


"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom
from pathlib import Path

plt.style.use('seaborn-v0_8-ticks')

def main():
    """
    Loads data from an input file, processes the data, computes control limits and outliers,
    exports the results to an output file, and creates a funnel plot based on the data.
    
    Adjust the input_path, output_results_path, and output_plot_path variables
    to set the appropriate file paths for the input data, exported results, and saved plot.
    
    The main function calls the following functions:
    - load_data: Reads the data from the input file
    - observ: Computes the number of observations
    - limits: Calculates control limits for the funnel plot
    - outliers_excel: Tags outliers in the data and creates a DataFrame with the results
    - Funnel: Generates the funnel plot
    """
    input_path = Path('INSERT INPUT PATH HERE')
    output_results_path = Path('INSERT OUTPUT RESULTS PATH HERE')
    output_plot_path = Path('INSERT OUTPUT PLOT PATH HERE')

    # Load data
    data = load_data(input_path)
    #compute observed proportions
    data['rate'] = (data.events / data.population) * 100000
    #compute overall proportion
    theta = (sum(data.events) / sum(data.population))

    # Compute limits and export results
    sum_obs = observ(data)
    # Bonferroni correction
    low = 0.025 / sum_obs
    high = 1 - low
    #export results into excel-worksheet
    sheet = outliers_excel(data, low, high, theta)
    sheet.to_excel(output_results_path)

    # Create funnel plot
    limit_data = limits(data, low, high, theta)
    funnel_plot = Funnel(data, limit_data)
    plt.savefig(output_plot_path)
    plt.show()


def load_data(input_path):
    # Load import data into df
    df = pd.read_excel(input_path, sheet_name='tab1')
    return df

def observ(Data):
    #compute number of observations
    obs = 0
    for i in Data.events:
        if i != 0:
            obs += 1
    return obs
  
def limits (Data, LowBon, HighBon, average):
    #limits do not depend on data, although we use theta = average proportion as targetline
    """
    Calculates control limits for proportions according to Spiegelhalter 2005 (appendix A.1.1) 
    based on inverse binomial distribution and a list of population values. Results can be used to draw control 
    limits into a plot. 95% control limits with and without bonferroni correction are calculated.
     
    Parameters
    ----------
    Data : Dataframe with data import (see prerequisites).
    LowBon : float
        P-value for a lower control limit, here: 95% with bonferroni correction.
    HighBon : float
        P-value for an upper control limit, here: 95% with bonferroni correction.
    average : float
        Target proportion theta for control limits.

    Returns
    -------
    lim : Dataframe with control limits.

    """
    minN = min(Data.population)
    maxN = max(Data.population)
    p = [LowBon, 0.025, 0.975, HighBon]
    n, i = [], 100
    step = round((maxN-minN)/500)
    while i < 16000000:
        n.append(i)
        i += step
    n = np.array(n)
    quantiles = []
    for quan in p:
        r = binom.ppf(quan, n, average) 
        quantiles.append(r)
    quantiles = np.array(quantiles)
    numer = binom.cdf(quantiles, n, average)
    for i in range(4):
        numer[i] = numer[i] - p[i]
    denom = (binom.cdf(quantiles, n, average)) - (binom.cdf((quantiles - 1), n, average))
    limits = (quantiles - (numer/denom))/n     
    lim = pd.DataFrame.from_records(limits*100000)
    lim = lim.transpose()
    lim.columns = ['L2sd_bon','L2sd','U2sd','U2sd_bon']
    lim['N'] = n
    lim['average'] = (average*100000)
    return lim
    
def outliers_excel (Data, LowBon, HighBon, average):
    """
    Calculates control limits for proportions according to Spiegelhalter 2005 (appendix A.1.1) 
    based on inverse binomial distribution and population for each area. 95% control limits  
    with and without bonferroni correction are calculated. Areas outside of control limits are tagged in
    a separate dataframe which can be exported, e.g. as Excel-file. 

    Parameters
    ----------
    See function limits.

    Returns
    -------
    results : Dataframe with comparison of area performance.

    """
    p = [LowBon, 0.025, 0.975, HighBon]
    n = np.array(Data.population)
    quantiles = []
    for quan in p:
        r = binom.ppf(quan, n, average) 
        quantiles.append(r)
    quantiles = np.array(quantiles)
    numer = binom.cdf(quantiles, n, average)
    for i in range(4):
        numer[i] = numer[i] - p[i]
    denom = (binom.cdf(quantiles, n, average)) - (binom.cdf((quantiles - 1), n, average))
    limits = (quantiles - (numer/denom))/n     
    lim = pd.DataFrame.from_records(limits*100000)
    lim = lim.transpose()
    lim.columns = ['L2sd_bon','L2sd','U2sd','U2sd_bon']
    frames = [Data, lim]
    results = pd.concat(frames, axis=1)
    results.loc[results['rate'] < results['L2sd_bon'], 'comparison'] = 'Very low (<0.025_Bonferroni)'
    results.loc[results['rate'] >= results['L2sd_bon'], 'comparison'] = 'Low (<0.025)'
    results.loc[results['rate'] >= results['L2sd'], 'comparison'] = ''
    results.loc[results['rate'] > results['U2sd'], 'comparison'] = 'High (>0.975)'
    results.loc[results['rate'] > results['U2sd_bon'], 'comparison'] = 'Very high (>0.975_Bonferroni)'
    return results

def Funnel (Data, limits):
    """
    Draws funnel plot. 

    Parameters
    ----------
    Data : Dataframe with data import (see prerequisites).
    limits : Dataframe from function limits.

    Returns
    -------
    None.

    """  
    #Adjust plot
    plt.title('Crude rate of hospitalizations with diabetes, on county level 2011')
    plt.xlabel('Population')
    plt.ylabel('Rate per 100,000 population')
    plt.axis([0, 1000000, 0, (max(Data.rate)+100)])
    plt.xticks(np.arange(0, 1000000, 200000))
    plt.yticks(np.arange(0, (max(Data.rate)+100), 100)) 
    plt.scatter(Data.population, Data.rate, color='black', marker='.', s=40)
    plt.plot(limits.N, limits.L2sd_bon, linestyle='solid', color='black', linewidth=1.2)
    sd, = plt.plot(limits.N, limits.L2sd, linestyle = 'dashed', color='black', linewidth=1.0)
    plt.plot(limits.N, limits.U2sd, linestyle = 'dashed', color='black', linewidth=1.0)
    sd_bon, = plt.plot(limits.N, limits.U2sd_bon, linestyle='solid', color='black', linewidth=1.2)
    plt.plot(limits.N, limits.average, linestyle='solid', color='black', linewidth=0.5)
    plt.legend([sd, sd_bon],['95% control limits', '95% control limits (Bonferroni correction)']) 
        
if __name__ == "__main__":
    main()



