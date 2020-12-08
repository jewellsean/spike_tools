Tools for analyzing calcium imaging with L0 Optimization
-----

Code from Fleming & Jewell et al. (2020). https://www.biorxiv.org/content/10.1101/2020.12.05.412965v1

### Data preprocessing 

Inspired and built off of the preprocessing toolkits of Theis et al (2016). 
Three main steps: 

1. Remove linear trends from the data 
2. Upsample data by a constant factor 
3. Normalize the data by percentiles  

... plus a few additional formatting tools.

Preprocessing is applied to in vitro and in vivo imaging data (via data_preprocessing.py) prior to further analysis. See Examples 1 and 2 in the Demo Notebok (demo.ipynb).

### Estimate AR1 decay rate from calibration data 

Assuming that the underlying calcium concentration decays exponentially between spikes, that is c_t = decay_rate * c_{t-1},
we use the true spike times to estimate the decay_rate. 

Decay rate estimation is performed on in vitro data consisting of simultaneously recorded imaging data and spike times (via estimate_decay_rates.py). See Example 1 in the Demo Notebook (demo.ipynb). 

### Estimate spikes with a target average firing rate via L0 optimization 

Given a target firing rate and decay we estimate spikes so that the average estimated firing rate is *close* to the target firing rate. 

Spike estimation is performed on in vitro and in vivo imaging data (via estimate_spikes.py). See Examples 1 and 2 in the Demo Notebook (demo.ipynb).

A target firing rate (in Hz) and decay rate must be inputted by the user to perform spike estimation. We provide recommended median decay rates for GCaMP6f and GCaMP6m for in vivo data, since decay rates are not directly observed in vivo (see recommended_decay_rates.txt). Note that these recommended decay rates are for spike estimation on 60 Hz data. Imaging data can be upsampled in the preprocessing step. If estimating spikes at a final sampling rate other than 60 Hz, the decay rate must be adjusted (see note in recommended_decay_rates.txt).
