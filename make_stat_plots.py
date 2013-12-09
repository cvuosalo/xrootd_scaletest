import sys
import ROOT
import os
import math

if (len(sys.argv) != 5):
    print "Usage: python make_stat_plots.py test_files test_duration size_of_time_bins test_start_time"
    sys.exit(1)

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
#hist_active_jobs.SetMaximum(1)

# this extra for loop destroys computation time and seems stupid,
# but I have yet to come up with a better way to only fill the histogram
# once per job per time interval
for i in range(nbins):
    test_files = open(sys.argv[1])
    for filename in test_files:
        filename = filename.rstrip('\n')
        #print "opening file %s ..." % filename
        file = open(filename)
        ## I want this h to be temporary and have maximum bin value of one so that we count 
        ## the number of jobs actually running during the time period rather than simply the 
        ## number of jobs that started (a job can have multiple file i/o's in a time interval).
        ##h = ROOT.TH1F("h", "h",  nbins, overall_start_time, overall_start_time + test_length) 
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
                
                if (start_time > intervals[str(i)][0] and start_time < intervals[str(i)][1] ):
                    # fill each time interval at most once per job
                    hist_active_jobs.Fill(round(start_time))
          
                    break;
        file.close()
    test_files.close()

# make plot of success/failure rate vs # clients running concurrently
n_clients = ROOT.TVectorF()
sf_rate = ROOT.TVectorF()

graph1 = ROOT.TGraph() # number of concurrent clients vs. success rate
graph2 = ROOT.TGraph() # time vs. failure rate
#graph3 = ROOT.TGraph()
graph3_b = ROOT.TGraph()
graph3 = ROOT.TGraph() # number of concurrent clients vs. average runtime
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
    graph1.SetPoint(graph1.GetN(), n_clients, f_rate)
    graph2.SetPoint(graph2.GetN(), n_clients, f_rate*100)

    run_times_combined = hist_opentimes.GetBinContent(i+1)
    if (s == 0): break
    performance_measure = n_clients / ( run_times_combined/(s) ) 
    graph3_b.SetPoint(graph3.GetN(), n_clients, run_times_combined/(s))
    graph3.SetPoint(graph3.GetN(), n_clients, performance_measure)
    #graph3.SetPointError(graph3.GetN()-1, 0.0, (1/(math.sqrt(n_clients))) * performance_measure )
    print run_times_combined/(s)
    graph4.SetPoint(graph4.GetN(), i*bin_size, performance_measure )

c1 = ROOT.TCanvas("c1", "c1")
#graph.Draw()
ofname = sys.argv[1][11:-4] + ".root"
print "ofname: %s" % ofname
output_file = ROOT.TFile(ofname, "RECREATE")
#hist_active_jobs.Draw()
graph3.Draw("AP")
graph3.GetXaxis().SetTitle("# of Active Clients")
graph3.GetYaxis().SetTitle("Performance (Hz)")
#os.system("sleep 5")
c1.SaveAs("plots/" + sys.argv[1][11:-4] + "_nClients_vs_performance.png")
graph2.Draw("AP")
graph2.GetXaxis().SetTitle("# of Active Clients")
graph2.GetYaxis().SetTitle("fractional failure rate (%)")
c1.SaveAs("plots/" + sys.argv[1][11:-4] + "_frate_vs_time.png")
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
graph2.Write("rate_vs_time")
graph3.Write("nClients_vs_performance")
graph3_b.Write("nClients_vs_avgruntime")
graph4.Write("performance_vs_time")
#output_file.Write()
c1.Close()
output_file.Close()
