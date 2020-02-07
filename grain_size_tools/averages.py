# ============================================================================ #
#                                                                              #
#    This is part of the "GrainSizeTools Script"                               #
#    A Python script for characterizing grain size from thin sections          #
#                                                                              #
#    Copyright (c) 2014-present   Marco A. Lopez-Sanchez                       #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License");           #
#    you may not use this file except in compliance with the License.          #
#    You may obtain a copy of the License at                                   #
#                                                                              #
#        http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS,         #
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#    See the License for the specific language governing permissions and       #
#    limitations under the License.                                            #
#                                                                              #
#    Version 3.0                                                               #
#    For details see: http://marcoalopez.github.io/GrainSizeTools/             #
#    download at https://github.com/marcoalopez/GrainSizeTools/releases        #
#                                                                              #
# ============================================================================ #

# ============================================================================ #
# Auxiliary functions doing specific tasks used by the GrainSizeTools script   #
# The names of the functions are self-explanatory. They appear in alphabetical #
# order. Save this file in the same directory as GrainSizeTools_script.py      #
# ============================================================================ #

# Imports
from scipy.stats import bayes_mvs, t
import numpy as np


def critical_t(confidence, sample_size):
    """Returns the (two-tailed) t-score based on the t-student distribution
    to set the certainty of the error margin.

    Parameters
    ----------
    confidence : float, scalar between 0 and 1
        the level of confidence. E.g. 0.95 -> 95%

    sample_size : scalar, int
        the sample size

    Assumptions
    -----------
    - t-student assumes that the data is symmetrically distributed

    Call function
    -------------
    scipy.stats.t
    """

    # recalculate confidence for the two-tailed t-distribution
    confidence = confidence + ((1 - confidence) / 2)

    return t.ppf(confidence, sample_size)


def arith_mean(pop, ci=0.95, method='ASTM'):
    """ Estimate the arithmetic mean, the Bessel corrected SD,
    and the confidence interval based on different methods.

    Parameters
    ----------
    pop : array-like
        the population

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95

    method : string
        the method to estimate the confidence interval, either
        'ASTM', 'CGI' or 'mCox'.

    Assumptions
    -----------
    -

    Call functions
    --------------
    - ASTM
    - CGI
    - mod_Cox
    - Numpy mean and std
    """

    n, mean, std = len(pop), np.mean(pop), np.std(pop, ddof=1)

    # confidence interval
    if method == 'ASTM':
        conf_int, length = ASTM()
        return mean, std, conf_int, length

    elif method == 'GCI':
        ci_lower, ci_upper, length = CGI()
        return mean, std, (ci_lower, ci_upper), length

    elif method == 'Cox':
        ci_lower, ci_upper, length = mod_Cox()
        return mean, std, (ci_lower, ci_upper), length

    else:
        raise Exception("methods must be 'ASTM', 'GCI', or 'Cox'")


def gmean(pop, ci=0.95, method='CLT'):
    """ Estimate the geometric mean, the multiplicative (geometric) SD
    and the confidence interval.

    Parameters
    ----------
    pop : array-like
        the population

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95

    method: string
       the method to estimate the confidence interval, either
        'CLT or 'Bayes'

    Call functions
    --------------
    - CLT
    - Bayes
    - Numpy mean, std, log, exp

    Returns
    -------
    the geometric mean, the multiplicative SD, the confidence intervals (tuple),
    and the standard errors (tuple)
    """

    n = len(pop)

    # compute statistics in the log-transformed data
    mean_log = np.mean(np.log(pop))
    sd_log = np.std(np.log(pop), ddof=1)  # SD using n-1 degrees of freedom (Bessel corrected)

    # compute the back-transformed values (gmean and mSD in linear scale)
    gmean = np.exp(mean_log)
    mSD = np.exp(sd_log)

    # estimate the confidence intervals in linear scale
    t_score = critical_t(ci, n)
    upper_ci = np.exp(mean_log + t_score * (sd_log / np.sqrt(n)))
    lower_ci = np.exp(mean_log - t_score * (sd_log / np.sqrt(n)))
    std_err = (lower_ci - gmean, upper_ci - gmean)

    return gmean, mSD, (lower_ci, upper_ci), std_err


def median(pop, ci=0.95):
    """ Estimate the arithmetic mean, the SD and the confidence intervals
    using the t-score and the margin of error formula as follows:

    ci = mean ± t * (SD / sqrt(n))

    Parameters
    ----------
    pop : array-like
        the population

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95
    """
    pop = np.sort(pop)
    n, median, IQ_range = len(pop), np.median(pop), iqr(pop)

    # compute confidence intervals
    t_score = critical_t(ci, n)
    id_upper = 1 + (n / 2) + (t_score * np.sqrt(n)) / 2
    id_lower = (n / 2) - (t_score * np.sqrt(n)) / 2
    upper_ci, lower_ci = pop[int(np.ceil(id_upper))], data[int(np.floor(id_lower))]
    std_err = (lower_ci - median, upper_ci - median)

    return median, IQ_range, (lower_ci, upper_ci), std_err


def calc_freq_peak(diameters, bandwidth, max_precision):
    """ Estimate the peak of the frequency ("mode") of a continuous
    distribution based on the Gaussian kernel density estimator. It
    uses Scipy's gaussian kde method.

    Parameters
    ----------
    diameters : array_like
        the diameters of the grains

    bandwidth : string, positive scalar or callable
        the method to estimate the bandwidth or a scalar directly defining the
        bandwidth. Methods can be 'silverman' or 'scott'.

    max_precision : positive scalar
        the maximum precision expected for the "peak" estimator.

    Call functions
    --------------
    - gen_xgrid from tools
    - kde (from scipy)

    Returns
    -------
    The x and y values to contruct the kde, the peak grain size,
    the maximum density value,, and the bandwidth
    """

    # check bandwidth and estimate Gaussian kernel density function
    if isinstance(bandwidth, (int, float)):
        bw = bandwidth / diameters.std(ddof=1)
        kde = gaussian_kde(diameters, bw_method=bw)

    elif isinstance(bandwidth, str):
        kde = gaussian_kde(diameters, bw_method=bandwidth)
        bw = round(kde.covariance_factor() * diameters.std(ddof=1), 2)

    else:
        raise ValueError("bandwidth must be integer, float, or plug-in methods 'silverman' or 'scott'")

    # locate the peak
    xgrid = tools.gen_xgrid(diameters.min(), diameters.max(), max_precision)
    densities = kde(xgrid)
    y_max, peak_grain_size = np.max(densities), xgrid[np.argmax(densities)]

    return xgrid, densities, peak_grain_size, y_max, bw


def ASTM(data, ci=0.95):
    """ Estimate the error margin for the arithmetic mean according
    to the ASTM norm E112-12.

    Parameters
    ----------
    data : numpy array
        the dataset

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95

    Reference
    ---------
    ASTM-E112-12 (1996) Standard test methods for determining
    average grain size.

    Call
    ----
    calc_t

    Returns
    -------
    the lower and upper confidence intervals and the length
    """
    n = len(data)
    t = critical_t(confidence=ci, sample_size=n)
    mu, SD = np.mean(data), np.std(data)
    err = t * SD / np.sqrt(n)

    lower = mu - err
    upper = mu + err
    interval = upper - lower

    return lower, upper, interval


def mod_Cox(data, ci=0.95):
    """ Estimate the error margin for the arithmetic mean using the modified
    Cox method. This is a method optimized from lognormal populations. The
    method implemented below uses the Bessel corrected SD as it produces safer
    results for small sample sizes

    Parameters
    ----------
    data : numpy array
        the dataset

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95

    Reference
    ---------
    Anderson....
    Lopez-Sanchez (2020)

    Call
    ----
    calc_t

    Returns
    -------
    the lower and upper confidence intervals and the length
    """
    n = len(data)
    t = critical_t(confidence=ci, sample_size=n)
    data = np.log(data)
    mu_log, SD_log = np.mean(data), np.std(data, ddof=1)

    lower = np.exp(mu_log + 0.5 * SD_log**2 - t * (SD_log / np.sqrt(n)) * np.sqrt(1 + (SD_log**2 * n) / (2 * (n + 1))))
    upper = np.exp(mu_log + 0.5 * SD_log**2 + t * (SD_log / np.sqrt(n)) * np.sqrt(1 + (SD_log**2 * n) / (2 * (n + 1))))
    interval = upper - lower

    return lower, upper, interval


def CGI(data, ci=0.95, runs=10000):
    """ Estimate a confidence interval for the lognormal arithmetic mean
    using the generalized confidence interval (GCI) method of Krishnamoorthy
    and Mathew (2003). This is a method optimized from lognormal populations.

    Parameters
    ----------

    data : numpy array
        the dataset

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95

    runs : integer, default=10000
        the number of (Monte Carlo) iterations to generate z and u**2 values

    Reference
    ---------
    Krishnamoorthy and Mathew (2003) https://doi.org/10.1016/S0378-3758(02)00153-2

    Assumptions
    -----------
    - The population follows a lognormal distribution

    Call
    ----
    GCI_equation

    Returns
    -------
    the lower and upper confidence intervals and the length
    """

    # estimate the log-transformed population y = ln(x) and the degrees of freedom
    data = log(data)
    mu_log, var_log, n = mean(data), var(data), len(data)
    ddof = n - 1
    alpha = 0.05

    # Generate random values from the normal N(0,1) distribution
    z_array = np.random.normal(loc=0, scale=1.0, size=runs)

    # Generate random values from (non-central) chi-square distribution
    # with n-1 degrees of freedom
    u2_array = np.random.noncentral_chisquare(df=ddof, nonc=0, size=runs)
    u_array = sqrt(u2_array)

    # Compute the test statistic T values and sort them
    T_array = GCI_equation(mu_log, var_log, z_array, u_array, n)
    T_array = np.sort(T_array)

    # Estimate confidence limits
    lower = np.percentile(T_array, 100 * (alpha / 2))
    upper = np.percentile(T_array, 100 * (1 - (alpha / 2)))
    interval = upper - lower

    return lower, upper, interval


def GCI_equation(mu_log, var_log, z, u, n):
    """ Generalized confidence interval (GCI) equation.

    Parameters
    ----------
    mu_log : integer, float
        the mean of the log-transformed population
    var_log : integer, float
        the variance of the log-transformed population
    z : array-like
        random values of the normal N(0,1) distribution
    u : array-like
        random values of the chi-square distribution with n-1 degrees
        of freedom
    n : integer, float
        size of the dataset

    Returns
    -------
    [type]
        [description]
    """

    # estimate the second and third terms of the equation
    second_term = (z / (u / sqrt(n - 1))) * (sqrt(var_log) / sqrt(n))
    third_term = 0.5 * var_log / (u**2 / (n - 1))

    return exp(mu_log - second_term + third_term)


def CLT_based(data, ci=0.95):
    """ Estimate the ci 95% error margins of the geometric mean based
    on the central limit theorem and the standard error of the mean of
    the log-transformed population. It uses the t-score and Bessel
    corrected standard deviation.

    Parameters
    ----------
    data : numpy array
        the dataset

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95    

    Returns
    -------
    the lower and upper confidence intervals and the length
    """
    data, n = np.log(data), len(data)
    t = calc_t(confidence=0.95, sample_size=n)
    mu_log, SD_log = np.mean(data), np.std(data, ddof=1)
    err = t * SD_log / np.sqrt(n)

    lower_log = mu_log - err
    upper_log = mu_log + err

    lower, upper = np.exp(lower_log), np.exp(upper_log)
    interval = upper - lower

    return lower, upper, interval


def bayesian(data, ci=0.95):
    """ Use a bayesian approach to estimate the confidence intervals
    of the geometric mean. For this it estimates the bayesian error
    intervals of the log-transformed data using the scipy bayes_msv
    routine for then estimate the back-transformed values.

    Parameters
    ----------
    data : numpy array
        the dataset

    ci : float, scalar between 0 and 1
        the confidence interval, default = 0.95

    Reference
    ---------
    Oliphant (2006) https://scholarsarchive.byu.edu/facpub/278

    Assumptions
    -----------
    - The population follows a lognormal distribution

    Call
    ----
    bayes_mvs from scipy.stats module

    Returns
    -------
    the lower and upper confidence intervals and the length
    """

    data = np.log(data)
    mu_log, var_log, SD_log = bayes_mvs(data, alpha=0.95)
    mu, (lower_log, uppper_log) = mu_log
    lower, upper = np.exp(lower_log), np.exp(uppper_log)
    interval = upper - lower

    return lower, upper, interval


def median_em(data, ci=0.95):
    """ Estimate the approximate ci 95% error margins for the median
    using a rule of thumb based on Hollander and Wolfe (1999).

    Parameters
    ----------
    data : numpy array
        the dataset

    Reference
    ---------
    Hollander and Wolfe (1999) Nonparametric Statistical Methods.
    3rd ed. John Wiley, New York. 787 pp.

    Call
    ----

    Returns
    -------
    the lower and upper confidence intervals and the length
    """

    data, n = np.sort(data), len(data)
    z = TODO

    # compute confidence intervals
    id_upper = 1 + (n / 2) + z * sqrt(n) / 2
    id_lower = (n / 2) - z * sqrt(n) / 2
    upper, lower = data[int(np.ceil(id_upper))], data[int(np.floor(id_lower))]
    interval = upper - lower

    return lower, upper, interval
