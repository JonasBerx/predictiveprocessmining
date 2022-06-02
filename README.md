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

#### Minor note about data
The only data captured are the events, this is obvious. However this might not be sufficient to map out the waiting time between activities. I propose that waiting times are also captured for each activity and stored in a different dataset. This will potentially improve the visualisation of the violin graph.


### 2nd June 2022
I spent the majority of the day experimenting with Dash.
I came to the conclusion that the data we are using lacks some key values to fullfil the needs of this project. I need to find an efficient way to parse the different case variants from the dataset. Apromore supports this but it would be an insanely tedious task to manually split the data into logs based on their case variant. I will continue to explore this.

The next issue is capturing waiting time between the activities. As the mock visualizations show the various activities with a grey box signifying waiting time. It would require me to do on the spot calculations to find the average waiting time between each activity or to precalculate this waiting time before running a model. Efficiency of calculation will define this.
