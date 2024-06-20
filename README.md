# BRCC_TASK_2

![alt text](C:\Users\Mareks\Desktop\result.png "Title")

## Brief textual analysis

Based on the image above it is visible that the imbalance did not always decrease after activation time, sometimes it even increased. The most notable correct adjustment happened on the 28th of May at 7PM and on the 1st of June at 10AM. But there were also moments were the adjustments increased the imbalance, it is visible at the 31st of May at 5PM.

## Results - Steps to recreate

- Install the necessary modules for the project: ```pip install -r requirements.txt```

- Start the UI file: ```python BRCC_UI.py```, this will start the UI for the user, where they can select the date range and time for the data selection and the time zone.

![BRCC_UI.png]

- After selecting the date range and setting the time and the time zone, press the "Start plotting" button. This will start the collection and plotting of the data.

- After the data has been plotted it will show it to you on the screen. There you can select certain data point by hovering over it with your mouse.

![BRCC_RESULT.png]

- After inspecting the graph you can close it and start selecting new date ranges.