import numpy as np
from scipy.optimize import minimize, LinearConstraint

def estimate_c0(y, gam):
  n = y.shape[0]
  gseq = gam ** np.arange(n)
  return(np.sum(y * gseq) / np.sum(gseq ** 2))

def estimate_chats(y, gam):
  n = y.shape[0]
  gseq = gam ** np.arange(n)
  c0 = estimate_c0(y, gam)
  return(c0 * gseq)

def rss_fit(y, gam):
  chats = estimate_chats(y, gam)
  return(0.5 * np.sum((y - chats) ** 2))

#' yy is a list of decaying areas
def total_error(gam, yy):
  err = 0
  for y in yy:
    err = err + rss_fit(y, gam)
  return(err)

def estimate_gam(dat, min_data_points = 10):
  '''
  Given n bins where there is at least one spike t_{1}, t_{2}, ... , t_{n},
  define M as the index between t_{i} and t_{i+1} with maximal fluorescence value and
  m the index with minimal fluorescence value. These indices segment the fluorescence trace
  from peak-to-trough between spikes.
  Of these segments we consider segments whose peak-to-trough distance is >= min_data_points
  Then we estimate the decay rate by finding the decay_rate that minimizes the residual sum of squares of
  the best exponential curve to each of these segments

  return: dict of estimated decay rate (gam_hat), number of segments used, and two lists of the y values within each segment
  and the indices of the original gcamp that correspond to these y values
  '''
  y = dat['calcium']
  spike_by_bin = dat['spikes_per_bin']
  spike_ind = np.where(spike_by_bin > 0)[0]
  n_spike_ind = spike_ind.shape[0]
  yys = []
  yys_indices = []

  for i in range(n_spike_ind - 1): # do not use data from the last spike to end of series
    max_ind = np.argmax(y[np.arange(spike_ind[i],spike_ind[i + 1])]) + spike_ind[i]
    min_ind = np.argmin(y[np.arange(spike_ind[i],spike_ind[i + 1])]) + spike_ind[i]

    if min_ind - max_ind > min_data_points:
      yys.append(y[np.arange(max_ind, min_ind + 1)])
      yys_indices.append(np.arange(max_ind, min_ind + 1))

  lin_cons = LinearConstraint(np.array([1]), 0, 1)
  out = minimize(fun = total_error, x0 = 0.9, args = yys, method='COBYLA', constraints = lin_cons)
  return({'gam_hat':float(out['x']), 'n_segments':len(yys), 'y_segments':yys, 'yys_indices':yys_indices})