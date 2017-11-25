import os
import sys
import re
import csv
import math
walk_dir = ['401.bzip2/m5out/','429.mcf/m5out/','456.hmmer/m5out/','458.sjeng/m5out/','470.lbm/m5out/','scimark/m5out/']
test_true_name  = ['bzip2','mcf','hmmer','sjeng','lbm','scimark'] 

bpred_lookups = '.*system.cpu.branchPred.lookups\s+(\S+)\s+'
bpred_BTBLookups = '.*system.cpu.branchPred.BTBLookups\s+(\S+)\s+'
bpred_BTBHits = '.*system.cpu.branchPred.BTBHits\s+(\S+)\s+'
bpred_BTBHitPct = '.*system.cpu.branchPred.BTBHitPct\s+(\S+)\s+'
bpred_BTBMissPct = '.*system.cpu.branchPred.BTBMissPct\s+(\S+)\s+'
bpred_Branches = '.*system.cpu.Branches\s+(\S+)\s+'
bpred_predictedBranches = '.*system.cpu.predictedBranches\s+(\S+)\s+'
bpred_BranchMispred = '.*system.cpu.BranchMispred\s+(\S+)\s+'
bpred_BranchMispredPercent = '.*system.cpu.BranchMispredPercent\s+(\S+)\s+'
l1i_miss_rate = '.*system.cpu.icache.overall_misses::total\s+(\S+)\s+' 
l1d_miss_rate = '.*system.cpu.dcache.overall_misses::total\s+(\S+)\s+' 
l2_miss_rate  = '.*system.l2.overall_misses::total\s+(\S+)\s+'

#branches_not_stored_in_BTB = lookups - BTBLookups 
#predictable = predictedBranches + BranchMispred 
#unpredictable = Branches - predictable 

inst_cnt_re   = '.*sim_insts\s+(\S+)\s+'
bp_var = 'BiModeBP'
for index in range(len(walk_dir)):
	line_match = '.*'+str(bp_var)+'_'+str(test_true_name[index])+'_(\d+)BTBEntries_(\d+)global_(\d+)choice'
	resultFile = open(bp_var+"_"+test_true_name[index]+".csv",'wb')
	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow(["BTBEntries", "globalPred_size", "choicePred_size", "lookups", "BTBLookups", "Branches_not_in_BTB", "BTBHits", "BTBHitPct", "BTBMissPct","CPI","Branches", "predictedBranches", "BranchMispred", "BranchMispredPercent", "unpredictable", "predictable_pct", "unpredictable_pct"])
	for root, subdirs, files in os.walk(walk_dir[index]):
		print('--\nroot = ' + root)
		for filename in files:
			file_path = os.path.join(root, filename)
			if ( filename == 'stats.txt'):
				line_matched = re.match(line_match, root)
				if (line_matched):
					BTBEntries= float(line_matched.groups()[0])
					globalPredictorSize = float(line_matched.groups()[1])
					choicePredictorSize = float(line_matched.groups()[2])
					print('\t- file %s (full path: %s)' % (filename, file_path))
					with open(file_path) as f:
						for line in f:
							match_bpred_lookups = re.match(bpred_lookups, line)
							match_bpred_BTBLookups = re.match(bpred_BTBLookups, line)
							match_bpred_BTBHits = re.match(bpred_BTBHits, line)
							match_bpred_BTBHitPct = re.match(bpred_BTBHitPct, line)
							match_bpred_BTBMissPct = re.match(bpred_BTBMissPct, line)
							match_bpred_Branches = re.match(bpred_Branches, line)
							match_bpred_predictedBranches = re.match(bpred_predictedBranches, line)
							match_bpred_BranchMispred = re.match(bpred_BranchMispred, line)
							match_bpred_BranchMispredPercent = re.match(bpred_BranchMispredPercent, line)
							l1i_miss_match = re.match(l1i_miss_rate, line)
							l1d_miss_match = re.match(l1d_miss_rate, line)
							l2_miss_match  = re.match(l2_miss_rate, line)
							inst_cnt_match = re.match(inst_cnt_re, line)
							if inst_cnt_match:
								inst_cnt = float(inst_cnt_match.groups()[0])
							if match_bpred_lookups:
								lookups = float(match_bpred_lookups.groups()[0])
							if match_bpred_BTBLookups:
								BTBLookups = float(match_bpred_BTBLookups.groups()[0])
							if match_bpred_BTBHits:
								BTBHits = float(match_bpred_BTBHits.groups()[0])
							if match_bpred_BTBHitPct:
								BTBHitPct = float(match_bpred_BTBHitPct.groups()[0])
							if match_bpred_BTBMissPct:
								BTBMissPct = float(match_bpred_BTBMissPct.groups()[0])
							if match_bpred_Branches:
								Branches = float(match_bpred_Branches.groups()[0])
							if match_bpred_predictedBranches:
								predictedBranches = float(match_bpred_predictedBranches.groups()[0])
							if match_bpred_BranchMispred:
								BranchMispred = float(match_bpred_BranchMispred.groups()[0])
							if match_bpred_BranchMispredPercent:
								BranchMispredPercent = float(match_bpred_BranchMispredPercent.groups()[0])
							if l1d_miss_match:
								l1d_miss_value = float(l1d_miss_match.groups()[0])
								print 'l1d_miss =',l1d_miss_value
							if l1i_miss_match:
								l1i_miss_value = float(l1i_miss_match.groups()[0])
								print 'l1i_miss =',l1i_miss_value
							if l2_miss_match:
								l2_miss_value = float(l2_miss_match.groups()[0])
								cpi = 1 + ((((l1i_miss_value+l1d_miss_value)*4)+(l2_miss_value*80))/float(inst_cnt)) + ((BranchMispredPercent/100)*15)
								print 'l2_miss =',l2_miss_value
								print 'CPI =',cpi
								print 'lookups = ',lookups
								print 'BTBLookups = ',BTBLookups
								print 'BTBHits = ',BTBHits
								print 'BTBHitPct = ',BTBHitPct
								print 'BTBMissPct = ',BTBMissPct
								print 'Branches = ',Branches
								print 'predictedBranches = ',predictedBranches
								print 'BranchMispred = ',BranchMispred
								print 'BranchMispredPercent = ',BranchMispredPercent
								branches_not_stored_in_BTB = lookups - BTBLookups 
								unpredictable = Branches - predictedBranches
								predictable_pct = (predictedBranches/Branches)*100
								unpredictable_pct = (unpredictable/Branches)*100
								print 'branches_not_stored_in_BTB =',branches_not_stored_in_BTB
								print 'unpredictable =',unpredictable
								print 'predictable_pct =',predictable_pct
								print 'unpredictable_pct =',unpredictable_pct,'\n\n'
								wr.writerow([BTBEntries,globalPredictorSize,choicePredictorSize,lookups,BTBLookups,branches_not_stored_in_BTB,BTBHits,BTBHitPct,BTBMissPct,cpi,Branches,predictedBranches,BranchMispred,BranchMispredPercent,unpredictable,predictable_pct,unpredictable_pct])

