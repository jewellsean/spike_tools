import numpy as np
from scipy.signal import resample
from copy import deepcopy
from sklearn import linear_model

def time_adjustment(cam_times, factor, fps):
    n = cam_times.shape[0]
    cam_times_up = np.zeros(n * factor)
    cam_times_up[np.arange(0, n * factor, factor)] = cam_times
    avg_vector = (cam_times[np.arange(1, n)] - cam_times[np.arange(n - 1)]) / factor
    for i in range(1, factor):
        cam_times_up[np.arange(i, factor * (n - 1), factor)] = i * avg_vector + cam_times[np.arange(n - 1)]
    cam_times_up[np.arange(factor * (n  - 1) + 1, factor * n)] = (1.0 / fps) * (np.arange(0, factor - 1) + 1) + cam_times_up[factor * (n  - 1)]
    return(cam_times_up)


def preprocess(data, factor, low_perc = 5, up_perc = 80):
    '''
    Preprocess gcamp data based on https://github.com/lucastheis/c2s/blob/master/c2s/c2s.py#L166
    Main differences:
        - Simple linear regression to remove trends
        - Allows standardization to differ in lower and upper percentiles
        - Additional tools for managing camera and spike times

    :param data: dict containing
    'calcium' input gcamp (required) [n]
    'fps' original fps (required) [1]
    'cam_times' original camera times (optional) [n]
    'spike_times' spike times in seconds (optional) [m]
    :param factor: factor to upsample data. will produce upsampled data of size [factor * n]
    :param low_perc: lower percentile to normalize dff
    :param up_perc: upper percentile to normalize dff
    :return: dict with upsampled data and binned spikes (if spike_times provided)
    '''

    if 'cam_times' in data:
        assert data['calcium'].shape[0] == data['cam_times'].shape[0], "gcamp and camera times must be same length"

    data = deepcopy(data)

    x = np.arange(data['calcium'].shape[0])

    regr = linear_model.LinearRegression()
    regr.fit(x.reshape(-1, 1), data['calcium'])

    a = regr.coef_
    b = regr.intercept_

    data['calcium'] = data['calcium'] - (a * x + b)

    calcium_low_perc = np.percentile(data['calcium'], low_perc)
    calcium_high_perc = np.percentile(data['calcium'], up_perc)

    if calcium_high_perc - calcium_low_perc > 0.:
        data['calcium'] = (data['calcium'] - calcium_low_perc) / float(calcium_high_perc - calcium_low_perc)

    # normalize sampling rate
    if factor > 1:
        # number of samples after update of sampling rate
        num_samples = data['calcium'].shape[0] * factor
        # resample calcium signal
        data['calcium'] = resample(data['calcium'].ravel(), num_samples)
        data['fps'] = data['fps'] * factor
        if 'cam_times' in data:
            data['cam_times'] = time_adjustment(data['cam_times'], factor, data['fps'])
        else:
            data['cam_times'] = np.arange(0, data['calcium'].shape[0] / data['fps'], (1.0 / data['fps']))
            data['cam_times'] = data['cam_times'][np.arange(data['calcium'].shape[0])]
        if 'spike_times' in data:
            data['spikes_per_bin'] = bin_spikes(data['cam_times'], data['spike_times'])
    return data


def bin_spikes(cam_times, spike_times):
  nn = cam_times.shape[0]
  n_spikes_bin = np.zeros(nn)
  for i in range(nn-1):
    n_spikes_bin[i] = np.sum((spike_times >= cam_times[i]) * (spike_times < cam_times[i + 1]))
  return(n_spikes_bin)