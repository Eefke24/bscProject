import matplotlib.pyplot as plt
from ipywidgets import interact, widgets
import mne
from mne import Epochs
import pyxdf
import numpy as np
import pandas as pd
import time

# Path to your XDF file
xdf_path_marker = 'C:/Users/vanst/bscproject/eegData/sub-P001/ses-S001/eeg/par18.xdf'

# Load the XDF file
streams, fileheader = pyxdf.load_xdf(xdf_path_marker)

# check streams
# streams


"""Data Checking"""

for stream in streams:
    name = stream['info']['name'][0] if 'name' in stream['info'] else 'Unknown'
    stream_type = stream['info']['type'][0] if 'type' in stream['info'] else 'Unknown'
    print(f"Stream Name: {name}, Type: {stream_type}")


for stream in streams:
    name = stream['info']['name'][0] if 'name' in stream['info'] else 'Unknown'
    print(f'name: {name}')
    print('\n')

    # Extract stream data
    marker_value = stream['time_series']
    # Extract timestamps
    marker_time = stream['time_stamps']

    # Convert to NumPy arrays
    marker_value_np = np.array(marker_value)
    marker_time_np = np.array(marker_time)

    # Now you have the data and timestamps as NumPy arrays
    # You can process or analyze them as needed
    print(f"Data shape: {marker_value_np.shape}")
    print(f"Timestamps shape: {marker_time_np.shape}")
    print(marker_time_np.min())
    print(marker_time_np.max())
    print(f'unique values in the marker stream: {np.unique(marker_value)}')
    print('\n')


"""Array with time-aligned EEG and Marker signals"""

def align(streams):
  eeg_data = None
  eeg_timestamps = None
  marker_data = None
  marker_timestamps = None

  for stream in streams:
    print('for-loop initialised')

    if stream['info']['name'][0] == 'Muse-062B (00:55:da:b8:06:2b) EEG':
      print('accessing the muse stream data')
      eeg_data = np.array(stream['time_series']).T
      #print(f'eeg_data np array was created: {eeg_data}')
      eeg_timestamps = np.array(stream['time_stamps'])
      #print(f'eeg_timestamps np array was created: {eeg_timestamps}')

    elif stream['info']['name'][0] == 'MyMarkerStream':
      print('acessing the marker stream data')
      marker_data_temp = np.array(stream['time_series']).T
      #print(f'marker data np array was created: {marker_data_temp}')
      marker_data = marker_data_temp.flatten()  # Ensures marker_data is 1D
      #print(f'marker data np array was flattened: {marker_data}')
      marker_timestamps = np.array(stream['time_stamps'])
      #print(f'marker timestamps np array was created: {marker_timestamps}')

    else:
      print('stream in streams could not be found')

  ## This is for debugging
  #print(f'eeg_data {eeg_data.shape}, eeg_timestamps{eeg_timestamps.shape}, marker_data {marker_data.shape}, marker_timestamps {marker_timestamps.shape}')
  #print(f'marker data OG: {marker_data_temp.shape}')
  #print(f'marker data flattened: {marker_data.shape}')
  #print(f'unique marker values before combining: {np.unique(marker_data)}')

  print('\n')
  num_channels = 5
  num_samples = len(eeg_timestamps)

  combined_data = np.full((num_channels + 1, num_samples), np.nan)
  combined_data[:num_channels, :] = eeg_data

  for marker, marker_time in zip(marker_data, marker_timestamps):
    differences = np.abs(eeg_timestamps - marker_time)
    closest_idx = np.argmin(differences)
    print(f"Marker: {marker}, Marker Time: {marker_time}, Closest EEG Timestamp: {eeg_timestamps[closest_idx]}, Closest Index: {closest_idx}, Difference: {differences[closest_idx]}")
    combined_data[num_channels, closest_idx] = marker

  print('\n')
  print(f'shape = {combined_data.shape}')

  #removing the AUX channel (row 4) for now:
  i = 4
  # Remove the row at index i
  combined_data = np.concatenate((combined_data[:i], combined_data[i+1:]), axis=0)
  return combined_data


data_aligned = align(streams)

print(f'unique markers after combining the data: {np.unique(data_aligned[4])}')

def convert_nans(data_aligned):
  #Changing nan values due to incompatibility with MNE
  arr = data_aligned
  row_idx = 4

  print(f'unique markers before removing nans from the data: {np.unique(arr[4])}')
  #first change nans to -1's
  arr[row_idx, np.isnan(arr[row_idx])] = 0

  print(f'Maximum number in the reformed marker row: {arr[4, :].max()}')
  print(f'Minimum number in the reformed marker row: {arr[4, :].min()}')

  print(f'unique markers after removing nans from the data: {np.unique(arr[4])}')

  return arr

transformed_data = convert_nans(data_aligned)


"""# Plotting"""

def plot(transformed_data):
  eeg_data = transformed_data[0:4, :]
  time_points = np.arange(eeg_data.shape[1])
  markers = transformed_data[4, :]

  plt.figure(figsize=(16,10))
  channel_colors = ['blue', 'green', 'red', 'cyan']
  channel_labels = ['TP9', 'AF7', 'AF8', 'TP10']

  for i in range(eeg_data.shape[0]):
    plt.plot(time_points, eeg_data[i, :] + (i * 200),
             label=channel_labels[i], color=channel_colors[i], linewidth=1)  # Offset added for clarity

  filtered_time_points = time_points[markers > 0]

  for marker_time in filtered_time_points:
    plt.axvline(x=marker_time, color='k', linestyle='--', alpha=0.5, linewidth=1)  # Corrected to ensure vertical lines
  #for marker_time in time_points[markers != 0]:
    #plt.axvline(x=marker_time, color='k', linestyle='--', alpha=0.5)

  plt.title('EEG + markers')
  plt.xlabel('timepoints')
  plt.ylabel('amplitude + offset')
  plt.legend()
  plt.tight_layout()
  plt.show()

plot(transformed_data)


"""# MNE for proper visualization"""

mnedata = transformed_data

sfreq = 255
ch_names = ['TP9', 'AF7', 'AF8', 'TP10', 'Markers']
ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'stim']

info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
print(info)
raw = mne.io.RawArray(mnedata, info)

# TODO: check
def epochs(raw):
  # output: determines whether to report onset, offset or both of events
  # consecutive=True: for events in form [4,4,4,5,5,5,6,6,6...]
  # consecutive=False: for events in form [4,0,0,5,0,0,6,0,0...]
  events = mne.find_events(raw, stim_channel='Markers', output='onset',
                          consecutive=False, min_duration=0,
                          initial_event=False, verbose=True)


  #Picks, Reject and Flat cant be used here to filter data
  #filter data based on specific channels (picks)
  #filter data based on maximum peak-to-peak signal amplitude (reject)
  #filter data based on minimum peak-to-peak signal amplitude (flat)

  epochs = mne.Epochs(raw, events=events,
                      tmin=0, tmax=2,
                      picks=None, baseline=None,
                      preload=True, reject=None,
                      flat=None, verbose=True)

  return events, epochs

events, epochs = epochs(raw)

for digit in range(1,12):
    event_label = digit
    print(f'trigger {event_label}')
    epochs[event_label].average().plot(picks=ch_names[:4])

fig = mne.viz.plot_events(
    events, sfreq=raw.info["sfreq"], first_samp=raw.first_samp)

raw.compute_psd(picks='TP9').plot()

