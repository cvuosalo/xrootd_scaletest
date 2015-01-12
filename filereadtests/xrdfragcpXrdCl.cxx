//
// Get a fragment of a file and write it out to stdout.
//
// Note that one should have a valid GSI proxy, error messages from
//
//
// Example usage:
//   ./xrdfragcp --frag 0 1024 --frag 2048 1024 root://xrootd.unl.edu//store/mc/Summer12/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/00000/E47B9F8B-42EF-E111-A3A4-003048FFD756.root

#include "XrdCl/XrdClFile.hh"
#include "XrdCl/XrdClDefaultEnv.hh"
#include <iostream>
#include <pcrecpp.h>

#include <memory>
#include <string>
#include <list>

#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <fcntl.h>
#include <sys/time.h>

typedef std::string      Str_t;
typedef std::list<Str_t> lStr_t;
typedef lStr_t::iterator lStr_i;

//==============================================================================

struct Frag
{
  long long fOffset;
  int       fLength;

  Frag(long long off, int len) : fOffset(off), fLength(len) {}
};

typedef std::list<Frag>   lFrag_t;
typedef lFrag_t::iterator lFrag_i;

//==============================================================================

class App
{
  lStr_t    mArgs;

  Str_t     mCmdName;
  Str_t     mPrefix;
  Str_t     mUrl;

  bool      bVerbose;

  lFrag_t   mFrags;
  int       mMaxFragLength;

  bool      bCmsClientSim;
  bool      bFixedSleepTm;
  long long mCcsBytesToRead;
  int       mCcsNReqs;
  int       mCcsTotalTime;

  int       mNvread;
  double		mRTT;

public:
  App();

  void ReadArgs(int argc, char *argv[]);
  void ParseArgs();

  void Run();


  // Various modes
  
  void GetFrags();
  void GetChecksum();
  void CmsClientSim();
};

//==============================================================================

App::App() :
  mPrefix       ("fragment"),
  bVerbose      (false),
  mMaxFragLength(0),
  bCmsClientSim (false),
  bFixedSleepTm (false),
  mRTT(0.0),
  mNvread(0)
{}

//------------------------------------------------------------------------------

void App::ReadArgs(int argc, char *argv[])
{
  mCmdName = argv[0];
  for (int i = 1; i < argc; ++i)
  {
    mArgs.push_back(argv[i]);
  }
}

void next_arg_or_die(lStr_t& args, lStr_i& i, bool allow_single_minus=false)
{
  lStr_i j = i;
  if (++j == args.end() || ((*j)[0] == '-' && ! (*j == "-" && allow_single_minus)))
  {
    std::cerr <<"Error: option "<< *i <<" requires an argument.\n";
    exit(1);
  }
  i = j;
}

void App::ParseArgs()
{
  lStr_i i = mArgs.begin();

  while (i != mArgs.end())
  {
    lStr_i start = i;

    if (*i == "-h" || *i == "-help" || *i == "--help" || *i == "-?")
    {
      printf("Arguments: [options] url\n"
             "\n"
             "  url              url of file to fetch the fragments from\n"
             "\n"
             "  --verbose        be more talkative (only for --cmsclientsim)\n"
             "\n"
             "  --prefix <str>   prefix for created fragments, full name will be like:\n"
             "                     prefix-offset-length\n"
             "                   default is 'fragment'\n"
             "                   if '[drop]' is used, nothing is written\n"
             "\n"
             "  --frag <offset> <length>\n"
             "                   get this fragment, several --frag options can be used to\n"
             "                   retrieve several fragments\n"
             "\n"
             "  --cmsclientsim <request size in MB> <request period in sec> <total time in min> <fix, optional to indicated fixed sleep time>\n"
             "                   simulate a client accessing the file with given parameters\n"
             "\n"
             "  --rtt <float>    round-trip time to site in seconds (for cmsclientsim)\n"
             "\n"
             "  --vread <int>    number of vreads, usedoly with cmsclientsim\n"
             );
      exit(0);
    }
    else if (*i == "--verbose")
    {
      bVerbose = true;
      mArgs.erase(start, ++i);
    }
    else if (*i == "--prefix")
    {
      next_arg_or_die(mArgs, i);
      mPrefix = *i;
      mArgs.erase(start, ++i);
    }
    else if (*i == "--frag")
    {
      next_arg_or_die(mArgs, i);
      long long offset = atoll(i->c_str());
      next_arg_or_die(mArgs, i);
      long long sizell = atoll(i->c_str());

      if (offset < 0)
      {
        fprintf(stderr, "Error: offset '%lld' must be non-negative.\n", offset);
        exit(1);
      }
      if (sizell <= 0 || sizell > 1024*1024*1024)
      {
        fprintf(stderr, "Error: size '%lld' must be larger than zero and smaller than 1GByte.\n", sizell);
        exit(1);
      }

      int size = sizell;
      mFrags.push_back(Frag(offset, size));
      if (size > mMaxFragLength) mMaxFragLength = size;

      mArgs.erase(start, ++i);
    }
    else if (*i == "--cmsclientsim")
    {
      next_arg_or_die(mArgs, i);
      double readReqSize = atof(i->c_str());
      if (readReqSize < 0)
      {
        fprintf(stderr, "Error: read request '%d' must be non-negative.\n", readReqSize);
        exit(1);
      }
      next_arg_or_die(mArgs, i);
      int reqPeriod = atoi(i->c_str());
      if (reqPeriod < 0)
      {
        fprintf(stderr, "Error: request period '%d' must be non-negative.\n", reqPeriod);
        exit(1);
      }
      next_arg_or_die(mArgs, i);
      mCcsTotalTime = atoi(i->c_str());
      if (mCcsTotalTime < 0)
      {
        fprintf(stderr, "Error: total time '%d' must be non-negative.\n", mCcsTotalTime);
        exit(1);
      }
      mCcsTotalTime *= 60; // Convert to seconds for internal use
			mCcsNReqs = mCcsTotalTime / reqPeriod;
			mCcsBytesToRead = readReqSize * 1024 * 1024 * mCcsNReqs;
      bCmsClientSim = true;
      ++i;
      if (i != mArgs.end() && *i == "fix") {
      	      bFixedSleepTm = true;
	      ++i;
      }
      mArgs.erase(start, i);
    }
    else if (*i == "--vread")
    {
      next_arg_or_die(mArgs, i);
      mNvread = atoi(i->c_str());
      printf("ReadV enabled. Split reads into %d chunks.\n", mNvread);

      mArgs.erase(start, ++i);
    }
    else if (*i == "--rtt")
    {
      next_arg_or_die(mArgs, i);
      mRTT = atof(i->c_str());

      mArgs.erase(start, ++i);
    }
    else
    {
      ++i;
    }
  }

  if (mFrags.empty() && ! bCmsClientSim)
  {
    fprintf(stderr, "Error: at least one fragment should be requested.\n");
    exit(1);
  }

  if (mArgs.size() != 1)
  {
    fprintf(stderr, "Error: exactly one file should be requested, %d arguments found.\n", (int) mArgs.size());
    exit(1);
  }

  mUrl = mArgs.front();
}

//==============================================================================

void App::Run()
{
  if (bCmsClientSim)
  {
    CmsClientSim();
  }
  else
  {
    GetFrags();
  }
}

//==============================================================================

void App::GetFrags()
{
  std::auto_ptr<XrdCl::File> c( new XrdCl::File() );

  if ( ! c->Open(mUrl, XrdCl::OpenFlags::Read, XrdCl::Access::None).IsOK() )
  {
    fprintf(stderr, "Error opening file '%s'.\n", mUrl.c_str());
    exit(1);
  }

  XrdCl::StatInfo *statInfo = NULL;
  c->Stat(false, statInfo);

  for (lFrag_i i = mFrags.begin(); i != mFrags.end(); ++i)
  {
    if (i->fOffset + i->fLength > statInfo->GetSize())
    {
      fprintf(stderr, "Error: requested chunk not in file, file-size=%lld.\n", statInfo->GetSize());
      exit(1);
    }
  }

  std::vector<char> buf;
  buf.reserve(mMaxFragLength);

  int fnlen = mPrefix.length() + 32;
  std::vector<char> fn;
  fn.reserve(fnlen);

  for (lFrag_i i = mFrags.begin(); i != mFrags.end(); ++i)
  {
    int n = snprintf(&fn[0], fnlen, "%s-%lld-%d", mPrefix.c_str(), i->fOffset, i->fLength);
    if (n >= fnlen)
    {
      fprintf(stderr, "Internal error: file-name buffer too small.\n");
      exit(1);
    }

    int fd = open(&fn[0], O_WRONLY | O_CREAT | O_TRUNC,
                          S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH);
    if (fd == -1)
    {
      fprintf(stderr, "Error opening output file '%s': %s\n", &fn[0], strerror(errno));
      exit(1);
    }

    uint32_t bytesRead;
    c->Read(i->fOffset, i->fLength, &buf[0], bytesRead);

    write(fd, &buf[0], i->fLength);

    close(fd);
  }
}

//------------------------------------------------------------------------------

void App::GetChecksum()
{
  std::string url_proto_host, url_file;
  pcrecpp::RE re("(\\w+://[^/]+)/(/[^?]+)");
  re.PartialMatch(mUrl, &url_proto_host, &url_file);

  std::cout << "And the lucky shit is: '" << url_proto_host << "' unt '" << url_file << "'\n";

  // Fuck me silly, copied from XrdCommandLine.cc
  // url_proto_host += "//dummy";
  
  XrdCl::FileSystem ca(mUrl);

  unsigned char *csum = 0;
  XrdCl::Buffer arg, *response=NULL;
  if (!ca.Query(XrdCl::QueryCode::Checksum , arg, response).IsOK())
  {
    fprintf(stderr, "Retrival of checksum failed.\n");
    exit(1);
  }

  std::cout << "Checksum is '" << response->ToString() << "'\n";
}

//------------------------------------------------------------------------------

void App::CmsClientSim()
{
  // XrdCl::DefaultEnv::SetLogLevel("Dump"); // Dump gives huge amount of logging
  XrdCl::File xfile;

  if ( ! xfile.Open(mUrl, XrdCl::OpenFlags::Read, XrdCl::Access::None).IsOK() )
  {
    fprintf(stderr, "Error opening file '%s'.\n", mUrl.c_str());
    exit(1);
  }

  XrdCl::StatInfo *statInfo = NULL;
  xfile.Stat(false, statInfo);

  long long request_size = mCcsBytesToRead / mCcsNReqs;
  if (request_size > 128*1024*1024)
  {
    fprintf(stderr, "Error: request size (%lld) larger than 128MB.\n", request_size);
    exit(1);
  }
  if (request_size <= 0)
  {
    fprintf(stderr, "Error: request size (%lld) non-positive.\n", request_size);
    exit(1);
  }
  if (request_size > statInfo->GetSize())
  {
    fprintf(stderr, "Error: request size (%lld) larger than file size (%lld).\n", request_size, statInfo->GetSize());
    exit(1);
  }

  long long usleep_time = 1000000 * ((double)mCcsTotalTime / mCcsNReqs);
  if (usleep_time < 0)
  {
    fprintf(stderr, "Error: sleeptime (%lldmus) negative.\n", usleep_time);
    exit(1);
  }

  std::vector<char> buf;
  buf.reserve(request_size);

  long long offset = 0;
  long long toread = mCcsBytesToRead;
  XrdCl::ChunkList chunks;
  if (mNvread) {
     chunks.reserve(mNvread);
  }

  if (bVerbose)
  {
    printf("Starting CmsClientSim, %f MB to read in about %lld requests spaced by %.1f seconds.\n",
           toread/1024.0/1024.0, mCcsNReqs, usleep_time/1000000.0);
  }

  int count = 0;

  while (toread > 0)
  {
    timeval beg, end;

    long long req = (toread >= request_size) ? request_size : toread;

    if (offset + req > statInfo->GetSize())
    {
      offset = 0;
    }

    ++count;
    if (bVerbose)
    {
      printf("%3d Reading %.3f MB at offset %lld\n", count, req/1024.0/1024.0, offset);
    }


    uint32_t readRet = 0;
    gettimeofday(&beg, 0);
    if (mNvread) {

       int vreq = req/mNvread;
       for (int v=0; v<mNvread; ++v) {
          chunks.push_back(XrdCl::ChunkInfo(offset + vreq*v, vreq));
       }

       XrdCl::VectorReadInfo *vReadInfo;
       xfile.VectorRead(chunks, &buf[0], vReadInfo);
       if (bVerbose)
	       printf(" vector read  from client,  %d x %d, result = %d \n",mNvread,  vreq, readRet);
    }
    else
    {
       xfile.Read(offset, req, &buf[0], readRet);
       printf("plain read  from client req = %d, result = %d \n", req, readRet);
    }

    offset += req;
    toread -= req;

    gettimeofday(&end, 0);
    
    double endfracseconds = end.tv_usec / 1000000.0;

    long long readtime = (1000000ll*(end.tv_sec - beg.tv_sec) + 
    	    (end.tv_usec - beg.tv_usec));
    // printf("    Request %d, time %d\n", req, readtime);
    double readtime_fp = readtime / 1000000.0;
    if (mRTT > 0.0 && readtime_fp > mRTT) // Read time should always be > RTT
    	readtime_fp -= mRTT;
    if (readRet > 0) {
			double rate = (double) req / readtime;
			printf("     Data rate: %g Gbits/sec, %g MB/s\n",
						rate * 8000000.0 / (1024.0 * 1024.0 * 1024.0),
						rate * 1000000.0 / (1024.0 * 1024.0));
			printf("     Clock time: %d %g duration: %g s, size read: %d bytes\n",
				end.tv_sec, endfracseconds, readtime_fp, readRet);
    } else printf("     Failed read. Clock time: %d %g taking %g s, return value: %d\n",
    	end.tv_sec, endfracseconds, readtime_fp, readRet);
    long long sleepy = usleep_time;
    if (bFixedSleepTm == false)
			sleepy -= readtime;
    if (sleepy > 0)
    {
      if (bVerbose)
      {
        printf("    Clock time: %d %g -- Sleeping for %g seconds.\n",
        	end.tv_sec, endfracseconds, sleepy/1000000.0);
      }
      usleep(sleepy);
    }
    else
    {
      if (bVerbose)
      {
        printf("    Not sleeping ... was already %.1f seconds too late.\n", -sleepy/1000000.0);
      }
    }
  }
}

//==============================================================================

int main(int argc, char *argv[])
{
  App app;

  app.ReadArgs(argc, argv);
  app.ParseArgs();

  // Testing of check-sum retrieval ... works not.
  // app.GetChecksum();
  // return 0;

  app.Run();

  return 0;
}
