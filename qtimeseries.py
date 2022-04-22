from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Qtimeseries(object):
    """
    This samples from a distribution of discharges to create a time series
    """

    def __init__(self):
        pass

    def create_distribution_from_data(self, csv_in, cfs=True, annual = True,
                                        log10_q = True, dist_name_list=['pearson3',
                                        'gamma','weibull_min','genextreme'],
                                        p_max=0.001):
        '''
        can check this out as a reference
        https://www.earthdatascience.org/courses/use-data-open-source-python/use-time-series-data-in-python/floods-return-period-and-probability/
        import data and find best fit distribution using Kolmogorov-Smirnov test
        :param csv_in: filename for csv of discharge values to find distribution
        :type param: str
        :param cfs: if 1 units are in cfs otherwise they are in m3s
        :type param: bool
        :param dist_name_list: a list of distribution to test goodness of fit
        :type param: str array
        :param p_max:
        '''
        #variables
        cfs_to_m3s = 0.0283168466

        self.log10_q =log10_q

        if csv_in is not None:
            discharge_in =pd.read_csv(csv_in)
        else:
            #TODO raise error here
            discharge_in = None

        #find non-finite values and remove zero values because not looking at
        #non flow conditions
        discharge_in = discharge_in[discharge_in['Discharge (cfs)'].notna()]
        discharge_in = discharge_in[discharge_in['Discharge (cfs)'] > 0]

        #convert timestamp column to index for resampling
        discharge_in['Timestamp'] = pd.to_datetime(discharge_in['Timestamp'])
        discharge_in= discharge_in.set_index('Timestamp')

        #use peak annual discharge if prefered
        if annual is True:
            self.discharge_in_annual = discharge_in.resample('AS').max()
            self.Q_in= list(self.discharge_in_annual['Discharge (cfs)'])
        else:
            self.Q_in = list(discharge_in['Discharge (cfs)'])

        # change from cfs to m3s
        if cfs is True:
            self.Q_in = list(np.array(self.Q_in) * cfs_to_m3s)

        #convert to log10_q if especially for LP3 Distribution
        if log10_q is True:
            self.Q_in = np.log10(self.Q_in)

        # find best fit to data taken from https://www.hackdeploy.com/
        # fitting-probability-distributions-with-python/
        self.dist_results =[]
        self.params = {}
        self.DistributionName = ''
        self.PValue = None
        Param = None
        isFitted = False

        #loop through distributions.
        for dist_name in dist_name_list:
            dist = getattr(stats,dist_name)
            param = dist.fit(self.Q_in)

            self.params[dist_name] = param

            # TODO check for low outliers by making a Q-Q plot

            #Applying the Kolmogorov-Smirnov test
            D,p = stats.kstest(self.Q_in, dist_name,args = param);
            self.dist_results.append((dist_name,D,p))

        #select the best fitted distribution
        sel_dist,D,p = (min(self.dist_results,key = lambda item:item[1]))
        param = self.params[sel_dist]
        #store the distribution, its name and p=value if p value less than p_max
        if p < p_max:
            sel_dist_att = getattr(stats,sel_dist)
            self.rv = sel_dist_att(*param[:-2],loc=param[-2], scale = param[-1])
            self.DistributionName = sel_dist
            self.PValue = p

    def create_distribution_from_moments(self, log10_q = True,
        param=[0.11164261721356633, 1.8073093184360132, 0.5883575109420136], dist_name='pearson3', loc=0,scale=1):

        '''
        Consider the parameters and methods here:
        https://doi.org/10.1061/(ASCE)1084-0699(2007)12:5(482)
        :param params: shape parameters, location offset and scaling for distributions
        :type param: arrray of float
        :param loc: is the location which the distribution is shifted
        :type param: float
        :param scale:is how the distribution can be scaled
        :type param: float
        :param size: is the
        '''
        self.log10_q =log10_q
        #maybe genextreme is the best to use from scipy.stats
        dist = getattr(stats,dist_name)
        self.rv = dist(*param[:-2],loc=param[-2], scale = param[-1])
        self.DistributionName = dist_name
        self.PValue = None

    def sample_from_distribution(self,n):
        """
        right now previous doesn't affect future but that's not realy life
        for daily discharges would need to do a power spectrum as described
        https://doi.org/10.1016/j.jhydrol.2016.03.015
        :param n: number of discharges to create for timeseries
        :type param: float
        """
        self.n = n
        if self.log10_q is True:
            self.Qn=10**(self.rv.rvs(size=self.n))
        else:
            self.Qn=self.rv.rvs(size=self.n)
