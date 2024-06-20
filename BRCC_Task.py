import requests
import matplotlib.pyplot as plt
import pandas as pd
import mplcursors
import datetime
# Read the config file for the parameters
with open('config.txt', 'r') as f:
    start_date, end_date, time_frame_start, time_frame_end, time_zone = f.read().split(',')

START_DATE = start_date
END_DATE = end_date

TIME_FRAME_START = time_frame_start # Goes from 00 to 23, minutes don't matter since the api only allows new data every hour
TIME_FRAME_END = time_frame_end

if datetime.date.fromisoformat(START_DATE) > datetime.date.fromisoformat(END_DATE):
    raise ValueError("Start date cannot be after end date")

if datetime.date.fromisoformat(START_DATE) == datetime.date.fromisoformat(END_DATE) and TIME_FRAME_START == TIME_FRAME_END:
    raise ValueError("Date and time cannot be the same")

TIME_ZONE = time_zone

IMBALANCE_REQUEST = f"https://api-baltic.transparency-dashboard.eu/api/v1/export?id=imbalance_volumes&start_date={START_DATE}T{TIME_FRAME_START}%3A00&end_date={END_DATE}T{TIME_FRAME_END}%3A00&output_time_zone={TIME_ZONE}&output_format=json&json_header_groups=0"
NORMAL_ACTIVATIONS_REQUEST = f"https://api-baltic.transparency-dashboard.eu/api/v1/export?id=normal_activations_total&start_date={START_DATE}T{TIME_FRAME_START}%3A00&end_date={END_DATE}T{TIME_FRAME_END}%3A00&output_time_zone={TIME_ZONE}&output_format=json&json_header_groups=0"

request_impalance_volumes = requests.get(IMBALANCE_REQUEST).json()
request_normal_activations = requests.get(NORMAL_ACTIVATIONS_REQUEST).json()

# Extracting country data from the impalance_volumes request
COUNTRY_NAME_IMBALANCE = [item['group_level_0'] for item in request_impalance_volumes['data']['columns']]
COUNTRY_INDEX_IMBALANCE = [item['index'] for item in request_impalance_volumes['data']['columns']]

# Extracting the values and timestamps from the impalance_volumes request
VALUES = [item['values'] for item in request_impalance_volumes['data']['timeseries']]
TIMESTAMPS = [item['from'] for item in request_impalance_volumes['data']['timeseries']]

# Create a DataFrame from the imbalance_volumes data
df_imbalance = pd.DataFrame(VALUES, columns=COUNTRY_NAME_IMBALANCE, index=TIMESTAMPS)


COUNTRY_LIST = ['Latvia', 'Estonia', 'Lithuania', 'Baltics']
# Extracting the country data from the normal_activations_total request
COUNTRY_NAME_NORMAL = [item['group_level_0'] for item in request_normal_activations['data']['columns'] if item['group_level_0'] in COUNTRY_LIST]
COUNTRY_INDEX_NORMAL = [item['index'] for item in request_normal_activations['data']['columns'] if item['group_level_0'] in COUNTRY_LIST]
COUNTRY_LABEL_NORMAL = [item['label'] for item in request_normal_activations['data']['columns'] if item['group_level_0'] in COUNTRY_LIST]
COUNTRY_DICT = zip(COUNTRY_NAME_NORMAL, COUNTRY_LABEL_NORMAL)


# Extracting the values and timestamps from the normal_activations_total request
VALUES = [item['values'] for item in request_normal_activations['data']['timeseries']]
FILTERED_VALUES = [[sub_array[i] for i in COUNTRY_INDEX_NORMAL] for sub_array in VALUES]
TIMESTAMPS = [item['from'] for item in request_normal_activations['data']['timeseries']]

df_normal_activations = pd.DataFrame(FILTERED_VALUES, columns=COUNTRY_DICT, index=TIMESTAMPS)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plotting the first DataFrame
df_imbalance.plot(ax=ax1)
ax1.set_title('Imbalance Volumes')
ax1.set_ylabel('Values')
ax1.legend(loc='upper left')

# Plotting the second DataFrame
df_normal_activations.plot(ax=ax2)
ax2.set_title('Normal Activations - Total')
ax2.set_ylabel('Values')
ax2.set_xlabel('Timestamps')
ax2.legend(loc='upper left')


line1 = ax1.plot(TIMESTAMPS, df_imbalance, label='Imbalance Volumes')
line2 = ax2.plot(TIMESTAMPS, df_normal_activations, label='Normal Activations - Total')

# Add cursor
cursor1 = mplcursors.Cursor(line1, hover=True)
cursor2 = mplcursors.Cursor(line2, hover=True)



@cursor1.connect("add")
def on_add(sel):
    # Get the index of the hovered point
    index = int(sel.index)
    x_val = TIMESTAMPS[index]
    i = 0
    
    
    # Clear any existing annotations
    sel.annotation.set_text("")
    
    # Create a new annotation with data from all lines at the hovered x-value
    annotation_text = f'Date: {x_val}\n'
    for line in line1:
        
        y_val = line.get_ydata()[index]
        annotation_text += f'{COUNTRY_NAME_IMBALANCE[i]}: {y_val} MWh\n'
        i += 1
        
    # Add the annotation
    sel.annotation.set_text(annotation_text.strip())



@cursor2.connect("add")
def on_add_normal(sel):
    # Get the index of the hovered point
    index = int(sel.index)
    x_val = TIMESTAMPS[index]
    i = 0
    
    # Create a new annotation with data from all lines at the hovered x-value
    annotation_text = f'Date: {x_val}\n'
    for line in line2:
        
        y_val = line.get_ydata()[index]
        annotation_text += f'{COUNTRY_NAME_NORMAL[i]} | {COUNTRY_LABEL_NORMAL[i]}: {y_val} MWh\n'
        i += 1
        
    # Add the annotation
    sel.annotation.set_text(annotation_text.strip())


# Adjust layout and show plot
plt.tight_layout()
plt.xticks(rotation=-45)  
plt.show()