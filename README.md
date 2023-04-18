# Funnel plots to present cross-sectional data on county level
In this repository you will find a Python script for creating funnel plots to present cross-sectional data (proportions, e.g. crude rates) on county level

## Example

<img src="plot.png">

The plot shows the adult population of a county in North-Rhine Westfalia, Germany, in 2011 on the x-axis and the crude rate of diabetes hospitalizations in these counties in 2011 on the y-axis. Counties above the upper control limit and below the lower control show a remarkably high or low rate of diabetes hospitalizations which cannot be explained by chance. 

## Background 
Spatial variation in cross-sectional data on area levels can be explained from two perspectives: variation due to chance and variation due to systematic influence of known or unknown factors. In statistical process control, variation by chance is known as "common cause variation", while variation related to some extrinsic predictors is known as "special cause variation" (Mohammed et al. 2001). Funnel plots are one application of statistical process control that has been used in public health and health services research. Starting with a target that determines the expected value of an indicator and an a priori defined probability distribution, control limits are calculated (Spiegelhalter 2005). Those control limits can be interpreted as prediction intervals; indicator results within the control limits are consistent with common cause variation, whereas results beyond these limits differ significantly from the estimated distribution and are consistent with special cause variation. Therefore, funnel plots act as statistical tests for every county based on the null hypothesis that the indicators follow the specific probability distribution.

The Python script in this repository calculates funnel plots for cross sectional data on county level and can be adapted to any area level. Following Spiegelhalter's suggestion for cross-sectional data, a county's population is used as a measure of precision. Control limits are obtained from the inverse Binomial distribution and based on two-sigma limits (approximately equivalent to a 95 percent confidence interval). To adress multiple statistical testing, a second interval with Bonferroni correction is calculated. 

You can find this background and an example of the use of funnel plots in Pollmanns et al. 2018.

## Using the script

a. The following data is needed in xlsx-format for input (sheet=tab1). Notice EXACT column names in square brackets:
    number of county [area_id] AND/OR name of county [area_name] 
    number of events [events]
    population [population] 
    
b. Insert paths (3x) for input and output (see main-function).

c. Adjust title, axes etc. for plot (see funnel-function)

## References
Mohammed MA, Cheng KK, Rouse A, Marshall T. Bristol, Shipman, and clinical governance: Shewhart's forgotten lessons. Lancet. 2001 Feb 10;357(9254):463-7. doi: 10.1016/s0140-6736(00)04019-8.

Pollmanns J, Romano PS, Weyermann M, Geraedts M, Drösler SE. Impact of Disease Prevalence Adjustment on Hospitalization Rates for Chronic Ambulatory Care-Sensitive Conditions in Germany. Health Serv Res. 2018 Apr;53(2):1180-1202. doi: 10.1111/1475-6773.12680. Epub 2017 Mar 22.

Spiegelhalter DJ. Funnel plots for comparing institutional performance. Stat Med. 2005 Apr 30;24(8):1185-202. doi: 10.1002/sim.1970.

