***************************************************************
		ALL SCRIPTS
***************************************************************

bimode.py & local.py:
These scripts are used to run gem5 simulation for various branch predictor parameters related to LocalBP & BiModeBP .
e.g. in local.py BTBEntries and localPredsize is modified through script and gem5 is built each time before running simulation for a new configuration.

final_script.py :
This is also similar to the previous scripts, but this is used for the baseline configuration. Thus gem5 is built once for each branch predictor and then run for each simulation.

get_data*.py :
these scripts are used to collect the benchmark results and dump the needed parameters to a .csv file which is easily readable by excel for further analysis.

plot_data*.py :
these scripts make use of the .csv files to plot the trend for various parameters like BTBEntries, localPredsize, choicePredsize, etc vs mispredict percent, CPI ,etc.
