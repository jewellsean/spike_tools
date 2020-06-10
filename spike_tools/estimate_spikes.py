import numpy as np
from FastLZeroSpikeInference import fast

def l2_distance(nbin_spike_target, nbin_estimated_spikes):
    '''
    Absolute difference between number of target spikes and estimated spikes
    '''
    return np.abs(nbin_spike_target - nbin_estimated_spikes)

def loss_function_n_spikes(lam, gcamp, decay_rate, nbin_spike_target):
    '''
    Estimate spikes from gcamp with specified decay rate and tuning parameter lambda.
    Assess how far the estimated firing rate is from a target firing rate (as measured by the total
    number of spikes)

    :param gcamp:
    :param decay_rate:
    :param lam:
    :param nbin_spike_target:
    :return:
    '''
    fit = fast.estimate_spikes(gcamp, decay_rate, lam, True)
    nbin_estimated_spikes = len(fit['spikes'])
    return l2_distance(nbin_spike_target, nbin_estimated_spikes)

def one_d_binary_search(gcamp, decay_rate, lam_min, lam_max, nbin_spike_target, max_iters=50, tolerance=5):
    verbose = 0
    iter_i = 0
    loss_i = np.inf

    while iter_i <= max_iters and loss_i > tolerance:

        lam_1 = (3 * lam_min + lam_max) / 4
        lam_2 = (3 * lam_max + lam_min) / 4

        loss_lam_1 = loss_function_n_spikes(lam_1, gcamp, decay_rate, nbin_spike_target)
        loss_lam_2 = loss_function_n_spikes(lam_2, gcamp, decay_rate, nbin_spike_target)

        if verbose:
            print('at iteration i = ' + str(iter_i))
            print("\t \t loss at lam 1 (" + str(lam_1) + ") = " + str(loss_lam_1))
            print("\t \t loss at lam 2 (" + str(lam_2) + ") = " + str(loss_lam_2))

        if loss_lam_1 < loss_lam_2:
            if loss_lam_1 < tolerance:
                return {'n_iters': iter_i, 'lam_star':lam_1}
            lam_max = (lam_min + lam_max) / 2
        else:
            if loss_lam_2 < tolerance:
                return {'n_iters': iter_i, 'lam_star':lam_2}
            lam_min = (lam_min + lam_max) / 2

        iter_i = iter_i + 1

    lam_star = (lam_min + lam_max) / 2

    return {'n_iters': iter_i, 'lam_star':lam_star}

def estimate_spikes_by_firing_rate(dat, decay_rate, target_firing_rate, lam_min = 1e-6, lam_max = 1e0, max_iters=50, tolerance=5):
    '''
    Estimate spikes based on a target firing rate. Estimates spikes with FastLZeroSpikeInference.fast based on tuning
    parameter lambda. Uses 1D binary search to find a value of the tuning parameter that results in a number of estimated
    spikes that is close to the target_firing_rate

    :param dat: data dict, see data_preprocessing
    :param decay_rate: AR1 decay rate
    :param target_firing_rate: target firing rate in fps
    :param lam_min: minimal tuning parameter value for binary search
    :param lam_max: maximal tuning parameter value for binary search
    :param max_iters: maximum number of binary search iterations
    :param tolerance: stop binary search if difference in number of target and estimated spikes is less than tolerance
    :return: dict of the FastLZeroSpikeInference.fast on the optimal tuning parameter, the optimal parameter (lam_star)
    and details from the binary search
    '''
    gcamp = dat['calcium']
    fps = dat['fps']
    # transform target firing rate into a number of spikes
    n = gcamp.shape[0]
    nbin_spike_target = np.floor(target_firing_rate * n / fps)
    bs_search = one_d_binary_search(gcamp, decay_rate, lam_min, lam_max, nbin_spike_target, max_iters, tolerance)
    lam_star = bs_search['lam_star']
    fit = fast.estimate_spikes(gcamp, decay_rate, lam_star, True, True)
    return {'fit':fit, 'lam_star': lam_star, 'minimizer':bs_search}