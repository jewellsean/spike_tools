Tools for analyzing calcium imaging with L0 Optimization
-----

Code from Fleming & Jewell et al. (2020). https://www.biorxiv.org/content/10.1101/2020.12.05.412965v1

### Data preprocessing 

Inspired and built off of the preprocessing toolkits of Theis et al (2016). 
Three main steps: 

1. Remove linear trends from the data 
2. Upsample data by a constant factor 
3. Normalize the data by percentiles  

... plus a few additional formatting tools 

### Estimate AR1 decay rate from calibration data 

Assuming that the underlying calcium concentration decays exponentially between spikes, that is c_t = decay_rate * c_{t-1},
we use the true spike times to estimate the decay_rate. 

### Estimate spikes with a target average firing rate via L0 optimization 

Given a target firing rate and decay we estimate spikes so that the average estimated firing rate is *close* to the target firing rate. 
