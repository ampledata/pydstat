MODULE NAME
    pydstat

DESCRIPTION
    Collect and return process stats in Cloudkick and syslog formats.

    A Pythonic wrapper for pidstat: 
    http://manpages.ubuntu.com/manpages/lucid/en/man1/pidstat.1.html

    License
    =======
      Copyright 2011 Splunk, Inc.

      Licensed under the Apache License, Version 2.0 (the "License"); you 
      may not use this file except in compliance with the License. You may 
      obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software 
      distributed under the License is distributed on an "AS IS" BASIS, 
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or 
      implied. See the License for the specific language governing 
      permissions and limitations under the License.


CLASSES
    
    class PydstatError(exceptions.StandardError)
     |  Placeholder Exception for pydstat.
     |  
     |  Inherited methods
     |      exceptions.BaseException.__delattr__(...)
     |      object.__format__(...)
     |      exceptions.BaseException.__getattribute__(...)
     |      exceptions.BaseException.__getitem__(x, y)
     |      exceptions.BaseException.__getslice__(x, i, j)
     |      object.__hash__(x)
     |      exceptions.StandardError.__init__(...)
     |      exceptions.StandardError.__new__(T, S, *...)
     |      exceptions.BaseException.__reduce__(...)
     |      object.__reduce_ex__(...)
     |      exceptions.BaseException.__repr__(x)
     |      exceptions.BaseException.__setattr__(...)
     |      exceptions.BaseException.__setstate__(...)
     |      object.__sizeof__()
     |      exceptions.BaseException.__str__(x)
     |      object.__subclasshook__(...)
     |      exceptions.BaseException.__unicode__(...)

FUNCTIONS
    
    setup_logging()
        Sets up logging for pydstat.
    
    get_stats(pid=None)
        Call pidstat for the specified pid and return its output.
        
        Most of this is inherited from _pidstatMetrics.
        Returns:
            Output from subprocess.Popen() as a string split into a list.
        Return type:
            list
    
    parse_stats(stats)
        Groks the output from pidstat.
        Returns:
            List of stats for each PID specified (or all pids).
        Return type:
            list
    
    ck_print_stats(stats)
        Detects a metric's type (int or float) and print it in Cloudkick 
        format.
    
    log_stats(stats)
        Logs stats to syslog.
        
        Replace PyDict/JSON style string with k=v string. Also replace 
        weird field names, e.g. '%CPU', 'kb/s'.
    
    main()
        Main program loop, parses args, calls stuff.

VARIABLES
    
    __help__ = 'https://ampledata.github.com/pydstat'
    
    LOGGER = setup_logging()
    
    IGNORED_FIELDS = ('Time', 'PID', '%guest', 'CPU', 'Command')
    
    TEST_SINGLE = 'Linux 2.6.32-312-ec2 (orchestration-i-78061518.prod) ...
    
    TEST_ALL = 'Linux 2.6.32-312-ec2 (orchestration-i-78061518.prod)    ...
    
    __package__ = None

