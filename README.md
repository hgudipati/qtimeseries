# qtimeseries
Create discharge time series

## Purpose 
This script generates a discharge time series based on a distribution. The the parameters of the distribution can either be calculated from 
an exisiting timeseries of discharges or given as an input. 

## Assumptions
The assumption is that the previous step and next step of discharge is randomly selected from a distribution. This is often not true for daily
discharge.

##Inputs and Outputs 

### Inputs 
* create_distribution_from_data
  * `csv_in`
  * `cfs`
  * `annual`
  * `log10_q`
  * `dist_name_list`
  * `p_max`
* create_distribution_from_moment
  * `log10_q`
  * `dist_name`
* sample_from_distribution
  * `n`
  
  #### Key input parameters

| **Variable** 	| **Description**                                                                                                                                                     | **Typical value(s)**        	|
|--------------	|--------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------	|
| `csv_in`    	| filename for csv of discharge values to find distribution                                                                                                           | example file for running the code: 'MN_Jordan_daily.csv'                          	|
| `cfs`       	| if 1 units are in cfs otherwise they are in m3s                                                                                                                     | 1        	|
| `annual`   	  | if 1 units find the peak annual discharge for distribution	                                                                                                        | 0                     	|
| `log10_q`   	| if 1 discharge will be converted to loq10_q otherwise they are not going to be transformed. This is epsecially useful if log pearson3 distribution is desired.   	  | 0	|
| `dist_name_list`| for create_distribution_from_data: a list of distribution to test goodness of fit                                                                                 | ['pearson3','gamma','weibull_min','genextreme'] |
| `dist_name`  	| for create_discharge_from_moment the name for which the parameters were inputed                                                                                    	| ['pearson3']         	|
|`param`        | Shape parameters for distributin. This includes location which the distribution is shifted and scale with which the distribution is scaled, which are 2nd and 1st to last values | [0.11, 1.81, 0.59]|
| `p_max`  	    | p_value below which fit is hypothesized to be good                                                                                                                	| 0.001    	|
| `n`           | number of discharges to create for timeseries                                                                                                                       |1000|
### Outputs
This program outputs a time series of discharge for each step, `q(n)`.
