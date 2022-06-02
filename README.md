# Library comparison setup guide - DASH

## Setup:
Run the following commands to set up the virtual environment:
- venv/Scripts/Activate.bat
- pip install -r requirements.txt

## General information
The dataset used for this demo can be found in /data/
The origination of the data is the event log, split into two groups:
- Conform SLA (within 14 days)
- Non conform SLA

#### Minor note aobut data
The only data captured are the events, this is obvious. However this might not be sufficient to map out the waiting time between activities. I propose that waiting times are also captured for each activity and stored in a different dataset. This will potentially improve the visualisation of the violin graph.


