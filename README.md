# Library comparison setup guide - DASH

## Setup:
Run the following commands to set up the virtual environment:
- venv\Scripts\activate (WIN) | source venv/bin/activate (MAC / LINUX)
- pip install -r requirements.txt

## General information
The dataset used for this demo can be found in /data/
The origination of the data is the event log, split into two groups:
- Conform SLA (within 14 days)
- Non conform SLA


## Small showcase:

The webpage resulting in running the script contains a separate diagram for each case varaint found in the dataset.
Dash' simple UI that makes it possible to isolate 1 or more events from a plot to study in depth.
Some sample showcase's below:

#### Case Variant 1
![Case Variant 1](./pics/case_variant_1.PNG)

#### Case Variant 2
![Case Variant 2](./pics/case_variant_2.PNG)

#### Isolation of a single activity from one case variant
![Register Activity Isolated](./pics/reg_claim_cv1.PNG)

#### Isolation of three activities from the same case variant
![Three activities from CV1 isolated](./pics/act_1_2_3_cv1.PNG)


#### Minor note about data
The only data captured are the events, this is obvious. However, this might not be sufficient to map out the waiting time between activities. I propose that waiting times are also captured for each activity and stored in a different dataset. This will potentially improve the visualisation of the violin graph.


# Predictive Process Mining: Preprocessing and visualisation

This project preprocesses an event log and calculates the activity process time, the cumulative process time and waiting time between activities.
This DataFrame will then be written to a .CSV log that can be used as output or can be shown in a rudimentary web app. (with (Plotly) Dash)

## Setup:

There is a dependency: [Start time estimator](https://github.com/AutomatedProcessImprovement/start-time-estimator) that has to be installed separate.
I'm currently manually adding this dependency through PyCharm.
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Execution:
To execute the preprocessing only and retrieve the extended output log. This log can be found in data\results\data.csv __(Subject to change)__
```
python src\preprocessing.py
```

To show the violin plot results of each case variant:
```
python src\app.py
```

## Showcase:
- Data showcase: ![Dataset sample](./pics/datasample.PNG)
After running the [preprocessing.py](./src/preprocessing.py) script on this dataset we receive an event log with the following information added to it:
![Resulting dataset](./pics/dataresult.PNG)

If you choose to run the [app.py](./src/app.py) script, a local Flask server will be started where you can see the visual results of this log.
The data is split by case variant and individually visualised using (Plotly) Dash. Each case variant is represented by a violin plot.
Some examples:
![Case V 1](./pics/case_variant_x.PNG)
![Case V 2](./pics/case_variant_y.PNG)
![Case V 3](./pics/case_variant_z.PNG)

In each violin plot, you can isolate or filter certain activities out or in to get a better comparative insight between case variants.
Each activity should have its own representative color, making it easier to identify.
Some examples:
![Case Isolated 1](./pics/isolated_x.png)
![Case Isolated 2](./pics/isolated_y.png)
![Case Isolated 3](./pics/isolated_z.png)