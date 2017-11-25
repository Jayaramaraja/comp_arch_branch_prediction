import os
import sys
import re
import csv
import math
import glob
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
#########################################################################################

def plot_graphs_BTB(filename,testname):
	# open the file in universal line ending mode
	plot_dir = './plots/BiModeBP/'+testname+'/BTBEntries/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	BTBEntries_set = [float(i) for i in data['BTBEntries']]
	choicePred_size_set = [float(i) for i in data['choicePred_size']]
	globalPred_size_set = [float(i) for i in data['globalPred_size']]
	lookups_set = [float(i) for i in data['lookups']]
	BTBLookups_set = [float(i) for i in data['BTBLookups']]
	branches_not_stored_in_BTB_set = [float(i) for i in data['Branches_not_in_BTB']]
	BTBHits_set = [float(i) for i in data['BTBHits']]
	BTBHitPct_set = [float(i) for i in data['BTBHitPct']]
	BTBMissPct_set = [float(i) for i in data['BTBMissPct']]
	Branches_set = [float(i) for i in data['Branches']]
	predictedBranches_set = [float(i) for i in data['predictedBranches']]
	BranchMispred_set = [float(i) for i in data['BranchMispred']]
	BranchMispredPerce_set = [float(i) for i in data['BranchMispredPercent']]
	unpredictable_set = [float(i) for i in data['unpredictable']]
	predictable_pct_set = [float(i) for i in data['predictable_pct']]
	unpredictable_pct_set = [float(i) for i in data['unpredictable_pct']]
	cpi_set 	 = [float(i) for i in data['CPI']]
	BTBEntries_uniq = list(set(BTBEntries_set))
	choicePred_size_uniq = list(set(choicePred_size_set))
	globalPred_size_uniq = list(set(globalPred_size_set))
	lookups_uniq = list(set(lookups_set))
	BTBLookups_uniq = list(set(BTBLookups_set))
#branches_not_stored_in_BTB_uniq = list(set(Branches_not_stored_in_BTB_set))
	BTBHits_uniq = list(set(BTBHits_set))
	BTBHitPct_uniq = list(set(BTBHitPct_set))
	BTBMissPct_uniq = list(set(BTBMissPct_set))
	Branches_uniq = list(set(Branches_set))
	predictedBranches_uniq = list(set(predictedBranches_set))
	BranchMispred_uniq = list(set(BranchMispred_set))
	BranchMispredPerce_uniq = list(set(BranchMispredPerce_set))
	unpredictable_uniq = list(set(unpredictable_set))
	predictable_pct_uniq = list(set(predictable_pct_set))
	unpredictable_pct_uniq = list(set(unpredictable_pct_set))	
	full_list = zip(BTBEntries_set,globalPred_size_set,choicePred_size_set,BTBMissPct_set,BranchMispredPerce_set,unpredictable_pct_set,cpi_set)
####################  		BTBEnt 		################################
	for choicePred_size_var in choicePred_size_uniq :
		for globalPred_size_var in globalPred_size_uniq :
			index_set = []
			sorted_index = []
			needed_list = []
			needed_BTBent = []
			needed_BTBmiss = []
			needed_mispred = []
			needed_unpred = []
			needed_cpi = []
			for index in range(len(choicePred_size_set)):
				if ( (choicePred_size_var == choicePred_size_set[index]) & (globalPred_size_var == globalPred_size_set[index]) ):
					index_set.append(index)
					needed_list.append((index,full_list[index]))
			if len(index_set)>=3:
				needed_list = sorted(needed_list, key=lambda x:x[1][0])
				sorted_index = [item[0] for item in needed_list]
				for index in sorted_index:
					needed_BTBent.append(BTBEntries_set[index])
					needed_BTBmiss.append(BTBMissPct_set[index])
					needed_mispred.append(BranchMispredPerce_set[index])
					needed_unpred.append(unpredictable_pct_set[index])
					needed_cpi.append(cpi_set[index])
				print 'choicePred_size_var=',choicePred_size_var,'\n','indexes=',index_set,sorted_index
				print needed_list
				print needed_BTBent
				print needed_BTBmiss
				print needed_mispred
				print needed_unpred
				#fig, ax1 = plt.subplots()
				#ax1.plot(needed_l1i, needed_cpi, 'b*-')
				#ax1.set_xlabel('l1i size with l1dsize='+str(int(l1dsize_var))+'kB '+str(int(l1assoc_var))+'way l2size='+str(int(l2size_var))+'kB '+str(int(l2assoc_var))+'way line_size='+str(int(linesize_var))+'B')
				## Make the y-axis label and tick labels match the line color.
				#ax1.set_ylabel('CPI', color='b')
				#for tl in ax1.get_yticklabels():
				    #tl.set_color('b')
				
				#ax2 = ax1.twinx()
				#ax2.plot(needed_l1i, needed_cost, 'r*-')
				#ax2.set_ylabel('COST', color='r')
				#for tl in ax2.get_yticklabels():
				    #tl.set_color('r')
				
				host = host_subplot(111, axes_class=AA.Axes)
				plt.subplots_adjust(right=0.75)
				
				par1 = host.twinx()
				par2 = host.twinx()
				
				offset = 60
				new_fixed_axis = par2.get_grid_helper().new_fixed_axis
				par2.axis["right"] = new_fixed_axis(loc="right",
				                                    axes=par2,
				                                    offset=(offset, 0))
				
				par2.axis["right"].toggle(all=True)
				
				host.set_xlim(min(needed_BTBent)-16, max(needed_BTBent)+256)
				#host.set_ylim(min(needed_cpi), max(needed_cpi))
				#host.set_xticks(needed_BTBent)
				host.set_xlabel('BTBentries with globalPred_size='+str(int(globalPred_size_var))+'_choicePred_size='+str(int(choicePred_size_var)))
				host.set_ylabel("mispred_pct")
				par1.set_ylabel("BTBmiss")
				#par2.set_ylabel("unpred_pct")
				par2.set_ylabel("CPI")
				
				p1, = host.plot(needed_BTBent, needed_mispred, '+-', label="mispred_pct")
				p2, = par1.plot(needed_BTBent, needed_BTBmiss, 'x-',label="BTBmiss")
				#p3, = par2.plot(needed_BTBent, needed_unpred, '.-',label="unpred_pct")
				p3, = par2.plot(needed_BTBent, needed_cpi, '.-',label="CPI")
				
				#par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
				#par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
				
				#host.legend(loc='upper left')
				
				host.axis["left"].label.set_color(p1.get_color())
				par1.axis["right"].label.set_color(p2.get_color())
				par2.axis["right"].label.set_color(p3.get_color())
				plt.savefig(plot_dir+testname+"_globalPred_size="+str(int(globalPred_size_var))+"_choicePred_size="+str(int(choicePred_size_var))+".png")
				plt.close('all')

				#fig, ax1 = plt.subplots()
				#ax1.plot(needed_BTBent, needed_cpi, 'b*-')
				#ax1.set_xlabel('BTBentries with choicePred_size='+str(int(choicePred_size_var)))
				## Make the y-axis label and tick labels match the line color.
				#ax1.set_ylabel('CPI', color='b')
				#for tl in ax1.get_yticklabels():
				    #tl.set_color('b')
				
				#ax2 = ax1.twinx()
				#ax2.plot(needed_BTBent, needed_mispred, 'r*-')
				#ax2.set_ylabel('Mispred Percent', color='r')
				#for tl in ax2.get_yticklabels():
				    #tl.set_color('r')
				
				#plt.savefig(plot_dir+testname+"_CPI_localpred_size="+str(int(choicePred_size_var))+".png")
				#plt.close('all')

def plot_graphs_choice(filename,testname):
	# open the file in universal line ending mode
	plot_dir = './plots/BiModeBP/'+testname+'/choicePred_size/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	BTBEntries_set = [float(i) for i in data['BTBEntries']]
	choicePred_size_set = [float(i) for i in data['choicePred_size']]
	globalPred_size_set = [float(i) for i in data['globalPred_size']]
	lookups_set = [float(i) for i in data['lookups']]
	BTBLookups_set = [float(i) for i in data['BTBLookups']]
	branches_not_stored_in_BTB_set = [float(i) for i in data['Branches_not_in_BTB']]
	BTBHits_set = [float(i) for i in data['BTBHits']]
	BTBHitPct_set = [float(i) for i in data['BTBHitPct']]
	BTBMissPct_set = [float(i) for i in data['BTBMissPct']]
	Branches_set = [float(i) for i in data['Branches']]
	predictedBranches_set = [float(i) for i in data['predictedBranches']]
	BranchMispred_set = [float(i) for i in data['BranchMispred']]
	BranchMispredPerce_set = [float(i) for i in data['BranchMispredPercent']]
	unpredictable_set = [float(i) for i in data['unpredictable']]
	predictable_pct_set = [float(i) for i in data['predictable_pct']]
	unpredictable_pct_set = [float(i) for i in data['unpredictable_pct']]
	cpi_set 	 = [float(i) for i in data['CPI']]
	BTBEntries_uniq = list(set(BTBEntries_set))
	choicePred_size_uniq = list(set(choicePred_size_set))
	globalPred_size_uniq = list(set(globalPred_size_set))
	lookups_uniq = list(set(lookups_set))
	BTBLookups_uniq = list(set(BTBLookups_set))
#branches_not_stored_in_BTB_uniq = list(set(Branches_not_stored_in_BTB_set))
	BTBHits_uniq = list(set(BTBHits_set))
	BTBHitPct_uniq = list(set(BTBHitPct_set))
	BTBMissPct_uniq = list(set(BTBMissPct_set))
	Branches_uniq = list(set(Branches_set))
	predictedBranches_uniq = list(set(predictedBranches_set))
	BranchMispred_uniq = list(set(BranchMispred_set))
	BranchMispredPerce_uniq = list(set(BranchMispredPerce_set))
	unpredictable_uniq = list(set(unpredictable_set))
	predictable_pct_uniq = list(set(predictable_pct_set))
	unpredictable_pct_uniq = list(set(unpredictable_pct_set))	
	full_list = zip(BTBEntries_set,globalPred_size_set,choicePred_size_set,BTBMissPct_set,BranchMispredPerce_set,unpredictable_pct_set,cpi_set)
####################  		choicepredsize 		################################
	for BTBEntries_var in BTBEntries_uniq:
		for globalPred_size_var in globalPred_size_uniq :
			index_set = []
			sorted_index = []
			needed_list = []
			needed_choice = []
			needed_BTBmiss = []
			needed_mispred = []
			needed_unpred = []
			needed_cpi = []
			for index in range(len(choicePred_size_set)):
				if( (BTBEntries_var== BTBEntries_set[index]) & (globalPred_size_var == globalPred_size_set[index])):
					index_set.append(index)
					needed_list.append((index,full_list[index]))
			if len(index_set)>=3:
				needed_list = sorted(needed_list, key=lambda x:x[1][2])
				sorted_index = [item[0] for item in needed_list]
				for index in sorted_index:
					needed_choice.append(choicePred_size_set[index])
					needed_BTBmiss.append(BTBMissPct_set[index])
					needed_mispred.append(BranchMispredPerce_set[index])
					needed_unpred.append(unpredictable_pct_set[index])
					needed_cpi.append(cpi_set[index])
				print 'BTBEntries_var=',BTBEntries_var,'\n','indexes=',index_set,sorted_index
				print needed_list
				print needed_choice
				print needed_BTBmiss
				print needed_mispred
				print needed_unpred
				#fig, ax1 = plt.subplots()
				#ax1.plot(needed_l1i, needed_cpi, 'b*-')
				#ax1.set_xlabel('l1i size with l1dsize='+str(int(l1dsize_var))+'kB '+str(int(l1assoc_var))+'way l2size='+str(int(l2size_var))+'kB '+str(int(l2assoc_var))+'way line_size='+str(int(linesize_var))+'B')
				## Make the y-axis label and tick labels match the line color.
				#ax1.set_ylabel('CPI', color='b')
				#for tl in ax1.get_yticklabels():
				    #tl.set_color('b')
				
				#ax2 = ax1.twinx()
				#ax2.plot(needed_l1i, needed_cost, 'r*-')
				#ax2.set_ylabel('COST', color='r')
				#for tl in ax2.get_yticklabels():
				    #tl.set_color('r')
				
				host = host_subplot(111, axes_class=AA.Axes)
				plt.subplots_adjust(right=0.75)
				
				par1 = host.twinx()
				par2 = host.twinx()
				
				offset = 60
				new_fixed_axis = par2.get_grid_helper().new_fixed_axis
				par2.axis["right"] = new_fixed_axis(loc="right",
				                                    axes=par2,
				                                    offset=(offset, 0))
				
				par2.axis["right"].toggle(all=True)
				
				host.set_xlim(min(needed_choice)-16, max(needed_choice)+256)
				#host.set_ylim(min(needed_cpi), max(needed_cpi))
				#host.set_xticks(needed_choice)
				host.set_xlabel('choicePred_size with BTBentries='+str(int(BTBEntries_var))+'_globalPred_size='+str(int(globalPred_size_var)))
				host.set_ylabel("mispred_pct")
				par1.set_ylabel("BTBmiss")
				#par2.set_ylabel("unpred_pct")
				par2.set_ylabel("CPI")
				
				p1, = host.plot(needed_choice, needed_mispred, '*-', label="mispred_pct")
				p2, = par1.plot(needed_choice, needed_BTBmiss, '+-',label="BTBmiss")
				#p3, = par2.plot(needed_choice, needed_unpred, '.-',label="unpred_pct")
				p3, = par2.plot(needed_choice, needed_cpi, '.-',label="CPI")
				
				#par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
				#par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
				
				#host.legend(loc='upper left')
				
				host.axis["left"].label.set_color(p1.get_color())
				par1.axis["right"].label.set_color(p2.get_color())
				par2.axis["right"].label.set_color(p3.get_color())
				plt.savefig(plot_dir+testname+"_BTBEntries="+str(int(BTBEntries_var))+"_globalPred_size="+str(int(globalPred_size_var))+".png")
				plt.close('all')
				
				#fig, ax1 = plt.subplots()
				#ax1.plot(needed_choice, needed_cpi, 'b*-')
				#ax1.set_xlabel('choicePred_size with BTBentries='+str(int(BTBEntries_var)))
				## Make the y-axis label and tick labels match the line color.
				#ax1.set_ylabel('CPI', color='b')
				#for tl in ax1.get_yticklabels():
				    #tl.set_color('b')
				
				#ax2 = ax1.twinx()
				#ax2.plot(needed_choice, needed_mispred, 'r*-')
				#ax2.set_ylabel('Mispred Percent', color='r')
				#for tl in ax2.get_yticklabels():
				    #tl.set_color('r')
				
				#plt.savefig(plot_dir+testname+"_CPI_BTBEntries="+str(int(BTBEntries_var))+".png")
				#plt.close('all')

#########################################################################################
def plot_graphs_global(filename,testname):
	# open the file in universal line ending mode
	plot_dir = './plots/BiModeBP/'+testname+'/globalPred_size/'
	with open(filename, 'rU') as infile:
	# read the file as a dictionary for each row ({header : value})
		reader = csv.DictReader(infile)
		data = {}
		for row in reader:
			for header, value in row.items():
				try:
					data[header].append(value)
				except KeyError:
					data[header] = [value]
	
	# extract the variables you want
	BTBEntries_set = [float(i) for i in data['BTBEntries']]
	choicePred_size_set = [float(i) for i in data['choicePred_size']]
	globalPred_size_set = [float(i) for i in data['globalPred_size']]
	lookups_set = [float(i) for i in data['lookups']]
	BTBLookups_set = [float(i) for i in data['BTBLookups']]
	branches_not_stored_in_BTB_set = [float(i) for i in data['Branches_not_in_BTB']]
	BTBHits_set = [float(i) for i in data['BTBHits']]
	BTBHitPct_set = [float(i) for i in data['BTBHitPct']]
	BTBMissPct_set = [float(i) for i in data['BTBMissPct']]
	Branches_set = [float(i) for i in data['Branches']]
	predictedBranches_set = [float(i) for i in data['predictedBranches']]
	BranchMispred_set = [float(i) for i in data['BranchMispred']]
	BranchMispredPerce_set = [float(i) for i in data['BranchMispredPercent']]
	unpredictable_set = [float(i) for i in data['unpredictable']]
	predictable_pct_set = [float(i) for i in data['predictable_pct']]
	unpredictable_pct_set = [float(i) for i in data['unpredictable_pct']]
	cpi_set 	 = [float(i) for i in data['CPI']]
	BTBEntries_uniq = list(set(BTBEntries_set))
	choicePred_size_uniq = list(set(choicePred_size_set))
	globalPred_size_uniq = list(set(globalPred_size_set))
	lookups_uniq = list(set(lookups_set))
	BTBLookups_uniq = list(set(BTBLookups_set))
#branches_not_stored_in_BTB_uniq = list(set(Branches_not_stored_in_BTB_set))
	BTBHits_uniq = list(set(BTBHits_set))
	BTBHitPct_uniq = list(set(BTBHitPct_set))
	BTBMissPct_uniq = list(set(BTBMissPct_set))
	Branches_uniq = list(set(Branches_set))
	predictedBranches_uniq = list(set(predictedBranches_set))
	BranchMispred_uniq = list(set(BranchMispred_set))
	BranchMispredPerce_uniq = list(set(BranchMispredPerce_set))
	unpredictable_uniq = list(set(unpredictable_set))
	predictable_pct_uniq = list(set(predictable_pct_set))
	unpredictable_pct_uniq = list(set(unpredictable_pct_set))	
	full_list = zip(BTBEntries_set,globalPred_size_set,choicePred_size_set,BTBMissPct_set,BranchMispredPerce_set,unpredictable_pct_set,cpi_set)
####################  		globalpredsize 		################################
	for BTBEntries_var in BTBEntries_uniq:
		for choicePred_size_var in choicePred_size_uniq :
			index_set = []
			sorted_index = []
			needed_list = []
			needed_global = []
			needed_BTBmiss = []
			needed_mispred = []
			needed_unpred = []
			needed_cpi = []
			for index in range(len(choicePred_size_set)):
				if( (BTBEntries_var== BTBEntries_set[index]) & (choicePred_size_var == choicePred_size_set[index])):
					index_set.append(index)
					needed_list.append((index,full_list[index]))
			if len(index_set)>=3:
				needed_list = sorted(needed_list, key=lambda x:x[1][1])
				sorted_index = [item[0] for item in needed_list]
				for index in sorted_index:
					needed_global.append(globalPred_size_set[index])
					needed_BTBmiss.append(BTBMissPct_set[index])
					needed_mispred.append(BranchMispredPerce_set[index])
					needed_unpred.append(unpredictable_pct_set[index])
					needed_cpi.append(cpi_set[index])
				print 'BTBEntries_var=',BTBEntries_var,'\n','indexes=',index_set,sorted_index
				print needed_list
				print needed_global
				print needed_BTBmiss
				print needed_mispred
				print needed_unpred
				#fig, ax1 = plt.subplots()
				#ax1.plot(needed_l1i, needed_cpi, 'b*-')
				#ax1.set_xlabel('l1i size with l1dsize='+str(int(l1dsize_var))+'kB '+str(int(l1assoc_var))+'way l2size='+str(int(l2size_var))+'kB '+str(int(l2assoc_var))+'way line_size='+str(int(linesize_var))+'B')
				## Make the y-axis label and tick labels match the line color.
				#ax1.set_ylabel('CPI', color='b')
				#for tl in ax1.get_yticklabels():
				    #tl.set_color('b')
				
				#ax2 = ax1.twinx()
				#ax2.plot(needed_l1i, needed_cost, 'r*-')
				#ax2.set_ylabel('COST', color='r')
				#for tl in ax2.get_yticklabels():
				    #tl.set_color('r')
				
				host = host_subplot(111, axes_class=AA.Axes)
				plt.subplots_adjust(right=0.75)
				
				par1 = host.twinx()
				par2 = host.twinx()
				
				offset = 60
				new_fixed_axis = par2.get_grid_helper().new_fixed_axis
				par2.axis["right"] = new_fixed_axis(loc="right",
				                                    axes=par2,
				                                    offset=(offset, 0))
				
				par2.axis["right"].toggle(all=True)
				
				host.set_xlim(min(needed_global)-16, max(needed_global)+256)
				#host.set_ylim(min(needed_cpi), max(needed_cpi))
				#host.set_xticks(needed_global)
				host.set_xlabel('globalPred_size with BTBentries='+str(int(BTBEntries_var))+'_choicePred_size='+str(int(choicePred_size_var)))
				host.set_ylabel("mispred_pct")
				par1.set_ylabel("BTBmiss")
				#par2.set_ylabel("unpred_pct")
				par2.set_ylabel("CPI")
				
				p1, = host.plot(needed_global, needed_mispred, '*-', label="mispred_pct")
				p2, = par1.plot(needed_global, needed_BTBmiss, '+-',label="BTBmiss")
				#p3, = par2.plot(needed_global, needed_unpred, '.-',label="unpred_pct")
				p3, = par2.plot(needed_global, needed_cpi, '.-',label="CPI")
				
				#par1.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
				#par2.set_ylim(min(needed_wc)-200, max(needed_cost)+300)
				
				#host.legend(loc='upper left')
				
				host.axis["left"].label.set_color(p1.get_color())
				par1.axis["right"].label.set_color(p2.get_color())
				par2.axis["right"].label.set_color(p3.get_color())
				plt.savefig(plot_dir+testname+"_BTBEntries="+str(int(BTBEntries_var))+"_choicePred_size="+str(int(choicePred_size_var))+".png")
				plt.close('all')
				
				#fig, ax1 = plt.subplots()
				#ax1.plot(needed_global, needed_cpi, 'b*-')
				#ax1.set_xlabel('choicePred_size with BTBentries='+str(int(BTBEntries_var)))
				## Make the y-axis label and tick labels match the line color.
				#ax1.set_ylabel('CPI', color='b')
				#for tl in ax1.get_yticklabels():
				    #tl.set_color('b')
				
				#ax2 = ax1.twinx()
				#ax2.plot(needed_global, needed_mispred, 'r*-')
				#ax2.set_ylabel('Mispred Percent', color='r')
				#for tl in ax2.get_yticklabels():
				    #tl.set_color('r')
				
				#plt.savefig(plot_dir+testname+"_CPI_BTBEntries="+str(int(BTBEntries_var))+".png")
				#plt.close('all')

#########################################################################################

for filename in glob.glob("./BiModeBP*.csv"):
	(f_path, f_name) = os.path.split(filename)
	(f_short_name, f_extension) = os.path.splitext(f_name)
	f_short_name = f_short_name.replace("BiModeBP_","",1)
	print f_short_name
	print filename
	if not os.path.exists("./plots/BiModeBP/"+f_short_name):
		os.makedirs("./plots/BiModeBP/"+f_short_name)
	if not os.path.exists("./plots/BiModeBP/"+f_short_name+"/BTBEntries"):
		os.makedirs("./plots/BiModeBP/"+f_short_name+"/BTBEntries")
	if not os.path.exists("./plots/BiModeBP/"+f_short_name+"/choicePred_size"):
		os.makedirs("./plots/BiModeBP/"+f_short_name+"/choicePred_size")
	if not os.path.exists("./plots/BiModeBP/"+f_short_name+"/globalPred_size"):
		os.makedirs("./plots/BiModeBP/"+f_short_name+"/globalPred_size")
	plot_graphs_BTB(filename,f_short_name)
	plot_graphs_choice(filename,f_short_name)
	plot_graphs_global(filename,f_short_name)


