import math
import re
import subprocess
import fileinput
import os

gem5_dir   = '/proj/engclasses/ce6304/kxm162730/comp_arch/gem5/'
gem5_exec  = gem5_dir + 'build/X86/gem5.opt' 
gem5_se    = gem5_dir + 'configs/example/se.py' 
bench_dir  = '/proj/engclasses/ce6304/kxm162730/comp_arch/Project1_SPEC/'

bp_setup_file = gem5_dir + 'src/cpu/simple/BaseSimpleCPU.py'
bp_param_file = gem5_dir + 'src/cpu/pred/BranchPredictor.py'

#TODO: function to loop over all tests & write results to corresponding output directories
test_name  = ['401.bzip2','429.mcf','456.hmmer','458.sjeng','470.lbm','scimark']
test_true_name  = ['bzip2','mcf','hmmer','sjeng','lbm','scimark'] 
test=[]
for test_var in test_name:
	test.append(bench_dir + test_var + '/src/benchmark')
test_arg=[]
test_arg.append(bench_dir + str(test_name[0]) + '/data/input.program 10')
test_arg.append(bench_dir + str(test_name[1]) +'/data/inp.in')
test_arg.append('--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 '+ bench_dir + str(test_name[2]) + '/data/bombesin.hmm')
test_arg.append(bench_dir + str(test_name[3])+'/data/test.txt') 
test_arg.append('20 ' + bench_dir +str(test_name[4]) +'/data/reference.dat 0 1 ' + bench_dir +str(test_name[4]) + '/data/100_100_130_cf_a.of')
test_arg.append('')
test_dir=[]

for test_var in test_name:
	test_dir.append( bench_dir + test_var+'/')
output_dir=[]
for out_var in test_dir:
	output_dir.append(out_var+'m5out')	
bp_name = ['local']
BP_name = ['LocalBP']
cpu_type   = 'timing'	
l1dsize_set 	=[128]
l1isize_set 	=[128]
l1assoc_set 	=[2]
l2size_set 	=[1024]
l2assoc_set 	=[4]
linesize_set 	=[64]
inst_cnt   = '500000000'


def update_gem5_src(BTBEntriesval = '2048',localPredictorval = '1024',globalPredictorval = '4096',choicePredictorval = '4096', which_BP = 'TournamentBP',BPfile = '',BP_paramfile = '',gem5_build_dir = '',update_BP=0,update_BP_params=0):
	BTBEntries = '(.*BTBEntries.*Param.Unsigned)\(\w+(.*)'
	BTBEntriesToReplace = '\\1('+(BTBEntriesval)+'\\2'
	localPredictorSize = '(.*localPredictorSize.*)\(\w+(.*)'
	globalPredictorSize = '(.*globalPredictorSize.*)\(\w+(.*)'
	choicePredictorSize = '(.*choicePredictorSize.*)\(\w+(.*)'
	localPredToReplace= '\\1('+(localPredictorval)+'\\2'
	globalPredToReplace= '\\1('+(globalPredictorval)+'\\2'
	choicePredToReplace= '\\1('+(choicePredictorval)+'\\2'
	if (update_BP_params):	
		subprocess.call(['sed','-i.bak','-E',"s/"+str(BTBEntries)+'/'+str(BTBEntriesToReplace)+"/g",BP_paramfile])
		subprocess.call(['sed','-i.bak','-E',"s/"+str(localPredictorSize)+'/'+str(localPredToReplace)+"/g",BP_paramfile])
		subprocess.call(['sed','-i.bak','-E',"s/"+str(globalPredictorSize)+'/'+str(globalPredToReplace)+"/g",BP_paramfile])
		subprocess.call(['sed','-i.bak','-E',"s/"+str(choicePredictorSize)+'/'+str(choicePredToReplace)+"/g",BP_paramfile])
	
	BP_match = "(.*branchPred.*BranchPredictor)\(\w+(.*)"
	BP_replace = "\\1("+(which_BP)+"\\2"
	if (update_BP):	
		subprocess.call(['sed','-i.bak','-E',"s/"+str(BP_match)+'/'+str(BP_replace)+"/",BPfile])
	
	if (update_BP | update_BP_params):
		subprocess.call(['scons','build/X86/gem5.opt'])

#changing the name of the python

#BTBEntriesValue=['16','32','64','128','256','512','1024','2048','8192','32768']
BTBEntriesValue=['2048','8192','32768']
localPredictorValue=['16','32','64','128','256','512','1024','2048','8192','32768']
globalPredictorValue=['4096']
choicePredictorValue=['4096']

for bp_var in BP_name:
	for BTB_var in BTBEntriesValue:
		for local_var in localPredictorValue:
			for global_var in globalPredictorValue:
				for choice_var in choicePredictorValue:
					update_gem5_src(BTBEntriesval = BTB_var,localPredictorval = local_var,globalPredictorval = global_var,choicePredictorval = choice_var, which_BP = bp_var,BPfile = bp_setup_file,BP_paramfile = bp_param_file,gem5_build_dir = gem5_dir,update_BP=1,update_BP_params=1)
					processes = []
					for index in range(len(test_name)):
						for number in range(len(l1dsize_set)):
							final_out_dir = str(output_dir[index])+'/'+str(bp_var)+'_'+str(test_true_name[index])+'_'+str(BTB_var)+'BTBEntries_'+str(local_var)+'local'
							processes.append(subprocess.Popen([gem5_exec,'-d',final_out_dir,gem5_se,'-c',str(test[index]),'-o',str(test_arg[index]),'-I',inst_cnt,'--cpu-type='+cpu_type,'--caches','--l2cache','--l1d_size='+str(l1dsize_set[number])+'kB','--l1i_size='+str(l1isize_set[number])+'kB','--l2_size='+str(l2size_set[number])+'kB','--l1d_assoc='+str(l1assoc_set[number]),'--l1i_assoc='+str(l1assoc_set[number]),'--l2_assoc='+str(l2assoc_set[number]),'--cacheline_size='+str(linesize_set[number])]))
					for p in processes:
						p.wait()


