import numpy as np
from scipy.stats import expon
from scipy import stats
import random

iterations  = 10
inter_ass = 20
arrse = int(540/inter_ass)
sys_time = 20
n = arrse
idle = 0
c_idle = 0
n_idle = 0
e_idle = 0
l_idle = 0
c2_idle = 0

#arrivals follow Poisson
arrivals = list(np.random.poisson(inter_ass, arrse))

#initialise base case
base_times = []
temp = arrivals[0]
mean_response_base = 0 
mean_response_nurse=0
mean_response_clerk = 0
table = []


f = open("outsms.txt", "w")
f.write("For 10 iterations:\n")
arrivals2 = []
for ele in arrivals:
	arrivals2.append(temp)
	temp+=ele
arrivals = arrivals2
print(arrivals)

for i in range(iterations):
  times = np.random.normal(sys_time, 5, arrse)
  times = list(times.astype(np.int))
  for i in times:
    if (i<0):
      i = 8
  #print("times: ",times)

  responses = []
  waits = []
  waits.append(0)
  starts = []
  starts.append(arrivals[0])
  ends = []
  ends.append(starts[0]+times[0])



  #base case
for i in range(1,n):
    waits.append(max(0,ends[i-1]-arrivals[i]))
    idle+=min(0,ends[i-1]-arrivals[i])
    starts.append(waits[i] + arrivals[i])
    ends.append(starts[i] + times[i])
  #print(waits,starts,ends)
  for i in range(n):
    responses.append(waits[i]+ends[i]-starts[i])
  #print("waits: ", waits)
  #print("responses: ",responses)
  #print("ends: ", ends)
  mean_response_base = sum(responses)/n
  print(mean_response_base)
  msrb = str(mean_response_base)
  f.write("Base time: " + msrb)
  f.write("\n")
  if(ends[-1]<540):
    close_base = "9 : 00 pm"
  else:
    close_base = str(int((ends[-1]-540)/60)+9) + ":" + str((ends[-1]-540)%60) +  "pm"
base_times.append(mean_response_base)

	
#clerk
clerks = np.array(expon.rvs(scale = 1.5,  size = n, loc=2))
clerks = list(clerks.astype(np.int))
c_responses = []
c_waits = []
c_waits.append(0)
c_starts = []
c_starts.append(arrivals[0])
c_ends = []
c_ends.append(c_starts[0]+times[0])
for i in range(1,n):
	c_waits.append(max(0,c_ends[i-1]-arrivals[i]))
	c_idle+=min(0,c_ends[i-1]-arrivals[i])
	c_starts.append(c_waits[i] + arrivals[i])
	c_ends.append(c_starts[i] + times[i])
#print(c_waits,c_starts,c_ends)
for i in range(n):
	c_responses.append(c_waits[i]+c_ends[i]-c_starts[i]+clerks[i])
#print(c_responses)
#print(clerks)
mean_response_clerk = sum(c_responses)/n
#print(mean_response_clerk)
#print(((np.var(c_responses)/n)+(np.var(responses)/n))**0.5)
vvc = int((((np.var(c_responses)/n)+(np.var(responses)/n))**2)/(((np.var(c_responses)/n)**2)/(n-1))+(((np.var(responses)/n)**2)/(n-1)))
#print(vvc)
multc = stats.t.ppf(1-0.025,vvc)
rangc = (((np.var(c_responses)/n)+(np.var(responses)/n))**0.5)*multc
uplowc = [(mean_response_base - mean_response_clerk)-rangc, (mean_response_base - mean_response_clerk)+rangc]
print(uplowc)
f.write(str(uplowc[0])+", "+str(uplowc[1]))
f.write("\n")
if((0 > uplowc[0]) and (0 < uplowc[1])):
	f.write("Statistically Insignificant i.e. data insufficient to determine result\n")
elif(uplowc[0]>0 and uplowc[0]>0):
	f.write("Statistically significant, and Alternative is better for average time than base case\n")
else:
	f.write("Statistically significant, and Alternative is worse for average time than base case, but other factors should be considered\n")



#nurse
nurses = np.array(expon.rvs(scale = 1.5,  size = n, loc=5))
nurses = list(nurses.astype(np.int))
n_times = []
for i in range(n):
	n_times.append(max(4,times[i] - nurses[i]))
n_responses = []
n_waits = []
n_waits.append(0)
n_starts = []
n_starts.append(arrivals[0])
n_ends = []
n_ends.append(n_starts[0]+n_times[0])
for i in range(1,n):
	n_waits.append(max(0,n_ends[i-1]-arrivals[i]))
	n_idle+=min(0,n_ends[i-1]-arrivals[i])
	n_starts.append(n_waits[i] + arrivals[i])
	n_ends.append(n_starts[i] + n_times[i])
#print(n_waits,n_starts,n_ends)
for i in range(n):
	n_responses.append(n_waits[i]+n_ends[i]-n_starts[i])
#print(n_responses)
mean_response_nurse = sum(n_responses)/n
#print(mean_response_nurse)
#print(((np.var(n_responses)/n)+(np.var(responses)/n))**0.5)
vvv = int((((np.var(n_responses)/n)+(np.var(responses)/n))**2)/(((np.var(n_responses)/n)**2)/(n-1))+(((np.var(responses)/n)**2)/(n-1)))
#print(vvv)
mult = stats.t.ppf(1-0.025,vvv)
rang = (((np.var(n_responses)/n)+(np.var(responses)/n))**0.5)*mult
uplow = [(mean_response_base - mean_response_nurse)-rang, (mean_response_base - mean_response_nurse)+rang]
print(uplow)
f.write(str(uplow[0])+", "+str(uplow[1]))
f.write("\n")
if((0 > uplow[0]) and (0 < uplow[1])):
	f.write("Statistically Insignificant i.e. data insufficient to determine result\n")
elif(uplow[0]>0 and uplow[0]>0):
	f.write("Statistically significant, and Alternative is better for average time than base case\n")
else:
	f.write("Statistically significant, and Alternative is worse for average time than base case, but other factors should be considered\n")



	
#exam room
chan = bool(random.getrandbits(1))
exams = np.random.normal(sys_time, 7, arrse)
exams = list(exams.astype(np.int))
e_times = []
for i in range(n):
	e_times.append(times[i] + chan*exams[i])
e_responses = []
e_waits = []
e_waits.append(0)
e_starts = []
e_starts.append(arrivals[0])
e_ends = []
e_ends.append(e_starts[0]+e_times[0])
for i in range(1,n):
	e_waits.append(max(0,e_ends[i-1]-arrivals[i]))
	e_idle+=min(0,e_ends[i-1]-arrivals[i])
	e_starts.append(e_waits[i] + arrivals[i])
	e_ends.append(e_starts[i] + e_times[i])
#print(e_waits,e_starts,e_ends)
for i in range(n):
	e_responses.append(e_waits[i]+e_ends[i]-e_starts[i])
#print(e_responses)
mean_response_exam = sum(e_responses)/n
#print(mean_response_exam)
#print(((np.var(e_responses)/n)+(np.var(responses)/n))**0.5)
vve = int((((np.var(e_responses)/n)+(np.var(responses)/n))**2)/(((np.var(e_responses)/n)**2)/(n-1))+(((np.var(responses)/n)**2)/(n-1)))
#print(vve)
multe = stats.t.ppf(1-0.025,vve)
rangex = (((np.var(e_responses)/n)+(np.var(responses)/n))**0.5)*multe
uplowe = [(mean_response_base - mean_response_exam)-rangex, (mean_response_base - mean_response_exam)+rangex]
print(uplowe)
f.write(str(uplowe[0])+", "+str(uplowe[1]))
f.write("\n")
if((0 > uplowe[0]) and (0 < uplowe[1])):
	f.write("Statistically Insignificant i.e. data insufficient to determine result\n")
elif(uplowe[0]>0 and uplowe[0]>0):
	f.write("Statistically significant, and Alternative is better for average time than base case\n")
else:
	f.write("Statistically significant, and Alternative is worse for average time than base case, but other factors should be considered\n")



	
	
#lab
labs = np.array(expon.rvs(scale = 1.5,  size = n, loc=10))
labs = list(labs.astype(np.int))
l_times = []
for i in range(n):
	l_times.append(max(4,times[i] + labs[i]))
l_responses = []
l_waits = []
l_waits.append(0)
l_starts = []
l_starts.append(arrivals[0])
l_ends = []
l_ends.append(l_starts[0]+l_times[0])
for i in range(1,n):
	l_waits.append(max(0,l_ends[i-1]-arrivals[i]))
	l_idle+=min(0,l_ends[i-1]-arrivals[i])
	l_starts.append(l_waits[i] + arrivals[i])
	l_ends.append(l_starts[i] + l_times[i])
#print(l_waits,l_starts,l_ends)
for i in range(n):
	l_responses.append(l_waits[i]+l_ends[i]-l_starts[i])
#print(l_responses)
mean_response_labs = sum(l_responses)/n
#print(mean_response_labs)
#print(((np.var(n_responses)/n)+(np.var(responses)/n))**0.5)
vvl = int((((np.var(l_responses)/n)+(np.var(responses)/n))**2)/(((np.var(l_responses)/n)**2)/(n-1))+(((np.var(responses)/n)**2)/(n-1)))
#print(vvl)
multl = stats.t.ppf(1-0.025,vvl)
rangl = (((np.var(l_responses)/n)+(np.var(responses)/n))**0.5)*multl
uplowl = [(mean_response_base - mean_response_labs)-rangl, (mean_response_base - mean_response_labs)+rangl]
print(uplowl)
f.write(str(uplowl[0])+", "+str(uplowl[1]))
f.write("\n")
if((0 > uplowl[0]) and (0 < uplowl[1])):
	f.write("Statistically Insignificant i.e. data insufficient to determine result\n")
elif(uplowl[0]>0 and uplowl[0]>0):
	f.write("Statistically significant, and Alternative is better for average time than base case\n")
else:
	f.write("Statistically significant, and Alternative is worse for average time than base case, but other factors should be considered\n")



	
#clerk_out
clerks2 = np.array(expon.rvs(scale = 1.5,  size = n, loc=2))
clerks2 = list(clerks2.astype(np.int))
c2_responses = []
c2_waits = []
c2_waits.append(0)
c2_starts = []
c2_starts.append(arrivals[0])
c2_ends = []
c2_ends.append(c2_starts[0]+times[0])
for i in range(1,n):
	c2_waits.append(max(0,c2_ends[i-1]-arrivals[i]))
	c2_idle+=min(0,c2_ends[i-1]-arrivals[i])
	c2_starts.append(c2_waits[i] + arrivals[i])
	c2_ends.append(c2_starts[i] + times[i])
for i in range(n):
	c2_responses.append(c2_waits[i]+c2_ends[i]-c2_starts[i]+clerks2[i])
#print(c_responses)
#print(clerks)
mean_response_clerk2 = sum(c2_responses)/n
#print(mean_response_clerk)
#print(((np.var(c_responses)/n)+(np.var(responses)/n))**0.5)
vvc2 = int((((np.var(c2_responses)/n)+(np.var(responses)/n))**2)/(((np.var(c2_responses)/n)**2)/(n-1))+(((np.var(responses)/n)**2)/(n-1)))
#print(vvc2)
multc2 = stats.t.ppf(1-0.025,vvc2)
rangc2 = (((np.var(c2_responses)/n)+(np.var(responses)/n))**0.5)*multc2
uplowc2 = [(mean_response_base - mean_response_clerk2)-rangc2, (mean_response_base - mean_response_clerk2)+rangc2]
print(uplowc2)
f.write(str(uplowc2[0])+", "+str(uplowc2[1]))
f.write("\n")
if((0 > uplowc2[0]) and (0 < uplowc2[1])):
	f.write("Statistically Insignificant i.e. data insufficient to determine result\n\n")
elif(uplowc2[0]>0 and uplowc2[0]>0):
	f.write("Statistically significant, and Alternative is better for average time than base case\n\n")
else:
	f.write("Statistically significant, and Alternative is worse for average time than base case, but other factors should be considered\n\n")

	
	
#closing times
if(ends[-1]<540):
	close_c = "6 : 00 pm"
else:
	close_c = str(int((c_ends[-1]-540)/60)+6) + ":" + str((c_ends[-1]-540)%60) +  "pm"

if(ends[-1]<540):
	close_n = "6 : 00 pm"
else:
	close_n = str(min(int(((n_ends[-1]-540)/60)+6),7)) + ":" + str((n_ends[-1]-540)%60) +  "pm"

if(ends[-1]<540):
	close_e = "6 : 00 pm"
else:
	close_e = str(min(int(((e_ends[-1]-540)/60)+6),7)) + ":" + str((e_ends[-1]-540)%60) +  "pm"

if(ends[-1]<540):
	close_l = "6 : 00 pm"
else:
	close_l = str(min(int(((l_ends[-1]-540)/60)+6),7)) + ":" + str((l_ends[-1]-540)%60) +  "pm"

if(ends[-1]<540):
	close_c2 = "6 : 00 pm"
else:
	close_c2 = str(min(int(((c2_ends[-1]-540)/60)+6),10)) + ":" + str((c2_ends[-1]-540)%60) +  "pm"

f.write("clerk closing: "+ close_c)
f.write("\n")
f.write("nurse closing: "+ close_n)
f.write("\n")
f.write("exam closing: "+ close_e)
f.write("\n")
f.write("lab closing: "+ close_l)
f.write("\n")
f.write("clerk2 closing: "+ close_c2)
f.write("\n")
