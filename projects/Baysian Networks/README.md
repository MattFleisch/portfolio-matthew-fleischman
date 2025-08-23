# Bayesian Networks for Accident Prediction

## Purpose

* Loads UK accident data (```accidents_2012_to_2014.csv```) and builds an Influence Diagram (Bayesian network + decision + utility) with ```pyAgrum```.
* Learns probability tables (PTs/CPTs) from the CSV.
* Sets evidence for ```Road_Surface_Conditions``` and infers:
  * Posterior of ```Accident_Severity```
  * Optimal decision for ```Level_of_Response```.

## Requirements

* Python 3.8+
* Dataset: ```accidents_2012_to_2014.csv```
* Packages: pyagrum, pandas, numpy, matplotlib

### Install:
```bash
pip install pyagrum pandas numpy matplotlib
```

## How to Run

* In the terminal, navigate to the directory containing ```AccidentPrediction.ipynb```.
* Ensure ```accidents_2012_to_2014.csv``` is in this directory.
* Run jupyter notebooks:
```bash
pip install jupyter
jupyter notebook
```
* Open ```AccidentPrediction.ipynb``` and run all cells.

## Data

* This dataset combines UK government traffic flow statistics (2000–2016) 
with 1.6M police-reported accidents (2005–2014, excluding 2008), providing one 
of the most comprehensive views of road safety and traffic patterns in the UK.
* Link: https://www.kaggle.com/datasets/daveianhickey/2000-16-traffic-flow-england-scotland-wales
* Columns used: ```Accident_Severity, Number_of_Vehicles, Number_of_Casualties, Road_Type, 
Speed_limit, Light_Conditions, Weather_Conditions, Road_Surface_Conditions, 
Urban_or_Rural_Area```
* Note: ```Number_of_Casualties``` is capped at 3; ```Number_of_Vehicles``` at 7.

## What to expect

* A printed list of possible values for the evidence variable (Road_Surface_Conditions).
* Posterior distribution for Accident_Severity.
* An integer mapping for the target variable’s states.
* The computed optimalDecision("Level_of_Response").

## Changing the evidence

* Replace 'Frost/Ice' with any value shown in the printed list for ```Road_Surface_Conditions``` in the line:
```
ie.setEvidence({evidence_var: evidence_dict['Frost/Ice']})
```

## Report

See [Bayesian Networks for Car Accident Predictions](Bayesian%20Networks%20for%20Car%20Accident%20Predictions.pdf) for the written report on this project.
