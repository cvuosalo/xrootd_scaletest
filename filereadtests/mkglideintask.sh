#!/bin/sh

logerror() {
  echo 2>&1 "$@"
}

check_proxy() {
  hours=$1
  proxy=$2
  if ! [ -f "$proxy" ]; then
    logerror
    logerror "NOTE: No grid proxy found.  (Expecting to find it here: $proxy.)"
    return 1
  fi

  #Issue a warning if less than this many seconds remain:
  min_proxy_lifetime=$((3600*$hours))

  seconds_left="`voms-proxy-info --timeleft --file=$proxy 2>/dev/null`"

  if [ "$seconds_left" = "" ]; then
    echo "WARNING: cannot find time remaining for grid proxy."
    voms-proxy-info -all -path $proxy
    return 0
  fi
  if [ "$seconds_left" -lt "$min_proxy_lifetime" ]; then
    logerror
    logerror "NOTE: grid proxy is about to expire:"
    logerror "voms-proxy-info"
    voms-proxy-info --file=$proxy
    return 1
  fi

}

if [ "$#" -lt 4 ]; then
  echo "USAGE: $0 jobs max_jobs file_list url_prefix site_name [vread]"
  exit 2
fi

proxy=$X509_USER_PROXY
test -z "$proxy" && proxy=/tmp/x509up_u$UID
if ! check_proxy 2 $proxy; then
  exit 1
fi

jobs="$1"
# rtt="$2"
file_list="$2"
xrootd_URL_prefix="$3"
site="$4"
vread="$5"

test -z "$vread" || vread="--vread $vread"

export TMPDIR=`pwd`

# file_count=$(wc -l $file_list | awk '{print $1}')
# files_per_job=$((file_count/jobs))

jobname=$(basename $file_list | sed 's|\.files||')-$(echo $xrootd_URL_prefix | sed 's|root://\([^/]*\).*|\1|')

# sed "s|^|$xrootd_URL_prefix|" $file_list | sort -R > $jobname.randsort
rm -rf ${jobname}.jobs
mkdir ${jobname}.jobs
# split --numeric-suffixes --suffix-length=4 --lines=$files_per_job ${jobname}.randsort ${jobname}.jobs/files
# rm -f ${jobname}.randsort
job=0
cat > ${jobname}.jobs/submit.all<<EOF
executable = ${HOME}/xrdfragcp
+DESIRED_Sites = "${site}"
stream_output = true
stream_error = true
log = ulog
notification = never
should_transfer_files = yes
when_to_transfer_output = on_exit
x509userproxy = $proxy
EOF
for f in `cat $file_list`; do
  jobstr=`printf "%05d" $job`
  cat >> ${jobname}.jobs/submit.all<<EOF
  arguments = --cmsclientsim 2.5 2 30 $vread --verbose ${xrootd_URL_prefix}${f}
  output = stdout.$jobstr.\$(Cluster)
  error = stderr.$jobstr.\$(Cluster)
  queue
EOF
  job=`expr $job + 1`
  if test $job -gt $jobs
  then
  	  exit 0
  fi
done

# arguments = --cmsclientsim 2.4 1 40 ${xrootd_URL_prefix}${f}
# arguments = --cmsclientsim 9.6 4 40 ${xrootd_URL_prefix}${f}
# arguments = --cmsclientsim 2.5 10 80 --rtt $rtt --verbose ${xrootd_URL_prefix}${f}
