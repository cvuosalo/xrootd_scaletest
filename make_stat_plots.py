import sys
import ROOT
import os
import math

if (len(sys.argv) != 6):
    print "Usage: python make_stat_plots.py test_files test_duration size_of_time_bins test_start_time site_name"
    sys.exit(1)

target_rate = 2

print "Opening list of test files..." + sys.argv[1]
#test_files = open(sys.argv[1])
test_length = float(sys.argv[2])
bin_size = float(sys.argv[3])
nbins = int(test_length/bin_size)
overall_start_time = float(sys.argv[4])

# setup interval mapping structure
intervals = {}
for i in range(nbins):
    intervals[str(i)] = [ i*bin_size, (i+1)*bin_size ]
#print "printing dictionary 'intervals'..."
#print intervals

print "Assuming test of length %f seconds, bin size %f seconds, yielding %f bins" % (int(test_length), int(bin_size), nbins)
print "Further assuming that the test began at time %f seconds" % overall_start_time
hist_active_jobs = ROOT.TH1F("hist_active_jobs", "concurrent active jobs as a function of time", nbins, 0, test_length)
hist_job_failures = ROOT.TH1F("hist_job_failures", "concurrent job failures as a function of time", nbins, 0, test_length)
hist_job_successes = ROOT.TH1F("hist_job_successes", "concurrent job successes as a function of time", nbins, 0, test_length)
hist_opentimes = ROOT.TH1F("hist_opentimes", "concurrent job successes as a function of time", nbins, 0, test_length)
hist_opentimes.Sumw2()
#hist_active_jobs.SetMaximum(1)

test_files = open(sys.argv[1])
binjoblist = []
for job_num in xrange(201):
	binjoblist.append([]) 
	for bin_num in xrange(nbins + 1):
		binjoblist[job_num].append(0) 
# print 'bjl ', binjoblist
job_num = 0
for filename in test_files:
    filename = filename.rstrip('\n')
    # print "opening file %s ..." % filename
    file = open(filename)
    job_in_bin = 0
    for line in file:
	if ("RESULT" in line):
	    #print line
	    results = line.split()
	    if (len(results) != 5): continue;
	    
	    xrootd_filename = results[1]
	    if (results[2] == "success"):
		job_success = True
	    else: 
		job_success = False
	    start_time = int(results[3]) - overall_start_time
	   
	    # jobs were limited to run at 2 Hz 
	    run_time = float(results[4])
	    if (run_time < 0.5):
		run_time = 0.5

	    if (job_success):
		hist_job_successes.Fill(start_time)
		hist_opentimes.Fill(start_time, run_time)
	    else: 
		hist_job_failures.Fill(start_time)
	    
	    #hist_opentimes.Fill(start_time, run_time)
	    
	    bin_num = hist_active_jobs.FindBin(start_time)
	    if (bin_num > nbins):
		print 'bad bin, start time ', bin_num, start_time
	    elif (binjoblist[job_num][bin_num] == 0):
		# fill each time interval at most once per job
		hist_active_jobs.Fill(round(start_time))
		binjoblist[job_num][bin_num] = 1
    job_num = job_num + 1
    file.close()
test_files.close()
# print 'bjl ', binjoblist

# make plot of success/failure rate vs # clients running concurrently
n_clients = ROOT.TVectorF()
sf_rate = ROOT.TVectorF()

graph1 = ROOT.TGraph() # number of concurrent clients vs. success rate
graph2 = ROOT.TGraph() # time vs. failure rate
#graph3 = ROOT.TGraph()
graph3_b = ROOT.TGraph()
graph3 = ROOT.TGraphErrors() # number of concurrent clients vs. average runtime
graph4 = ROOT.TGraph() # avg runtime vs. time 

for i in range(nbins):
    n_clients = hist_active_jobs.GetBinContent(i+1)
    s = hist_job_successes.GetBinContent(i+1)
    f = hist_job_failures.GetBinContent(i+1)
    if (f > 0):
        rate = s/(s+f)
    elif (s == 0.0):
        print "continue"
        continue
    else: rate = 1.0 #all success, no failures
    f_rate = 1 - rate
    exp_rate = n_clients * target_rate
    graph1.SetPoint(graph1.GetN(), n_clients, f_rate)
    graph2.SetPoint(graph2.GetN(), exp_rate, f_rate*100)

    run_times_combined = hist_opentimes.GetBinContent(i+1)
    run_times_error = hist_opentimes.GetBinError(i+1)
    print 'runtime, successes ', run_times_combined, s
    if (s == 0): continue
    performance_measure = n_clients / ( run_times_combined/(s) ) 
    performance_error = (run_times_error /  run_times_combined) * performance_measure
    graph3_b.SetPoint(graph3.GetN(), n_clients, run_times_combined/(s))
    graph3.SetPoint(graph3.GetN(), exp_rate, performance_measure)
    graph3.SetPointError(graph3.GetN(), 0.0, performance_error )
    print 'njobs, avg time ', n_clients, run_times_combined/(s)
    graph4.SetPoint(graph4.GetN(), i*bin_size, performance_measure )

c1 = ROOT.TCanvas("c1", "c1")
#graph.Draw()
outfilebase = sys.argv[1][:-4]
ofname = outfilebase + ".root"
print "ofname: %s" % ofname
output_file = ROOT.TFile(ofname, "RECREATE")
#hist_active_jobs.Draw()
graph2.SetMarkerStyle(8) # big dot
graph3.SetMarkerStyle(8) # big dot
graph3.SetTitle(sys.argv[5])
graph3.GetXaxis().SetTitle("Expected file-open rate (Hz)")
# graph3.GetXaxis().SetTitle("# of Active clients")
graph3.GetYaxis().SetTitle("Observed file-open rate (Hz)")
graph3.GetYaxis().SetRangeUser(0, 250)
graph3.GetXaxis().SetRangeUser(0, 250)
graph3.Draw("AP")
xmax = graph3.GetXaxis().GetXmax()
graphmax = graph3.GetHistogram().GetMaximum()
print 'graph max ', graphmax, xmax
if graphmax > 250:
	graphmax = 250
if graphmax > xmax:
	graphmax = xmax
evenline = ROOT.TLine(0.0, 0.0, graphmax, graphmax) 
evenline.SetLineColor(8)
evenline.SetLineWidth(2)
evenline.SetLineStyle(1)
evenline.Draw("same")
#os.system("sleep 5")
c1.SaveAs("plots/" + outfilebase + "_exprate_vs_performance.png")
graph2.SetTitle(sys.argv[5])
graph2.GetXaxis().SetTitle("Expected rate (Hz)")
# graph2.GetXaxis().SetTitle("# of Active Clients")
graph2.GetYaxis().SetTitle("Fractional failure rate (%)")
graph2.GetYaxis().SetTitleOffset(1.1)
# graph2.GetYaxis().SetRangeUser(0, 6)
graph2.GetXaxis().SetRangeUser(0, 250)
graph2.Draw("AP")
c1.SaveAs("plots/" + outfilebase + "_frate_vs_exprate.png")
#os.system("sleep 3")
#hist_job_successes.Draw()
#os.system("sleep 3")
#hist_job_failures.Draw()
#os.system("sleep 3")
#c1.SaveAs("canvas.root")
hist_active_jobs.Write()
hist_job_successes.Write()
hist_job_failures.Write()
graph1.Write("nClients_vs_rate")
graph2.Write("rate_vs_exprate")
graph3.Write("exprate_vs_performance")
graph3_b.Write("nClients_vs_avgruntime")
graph4.Write("performance_vs_time")
#output_file.Write()
c1.Close()
output_file.Close()
