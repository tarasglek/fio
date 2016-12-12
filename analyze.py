#!/usr/bin/env python
import json
import os
import sys
import re

def dump_stats(directory, entry):
    filename = "%s/%s" % (directory, entry)
    stats = json.loads(open(filename).read())
    clat = stats["jobs"][0]["write"]["clat"]["percentile"]
    print "%s,%s,%s,%s" % (entry, clat["50.000000"], clat["90.000000"], clat["99.000000"])

def main(directory):
    print "filename,p50,p90,p99"
    dump_stats(directory, "benchmark_before_output.json")
    dump_stats(directory, "benchmark_fill_output.json")
    for entry in sorted(os.listdir(directory)):
        match = re.search(r'fill_fill.*json$', entry)
        if not match:
            continue
        dump_stats(directory, entry)
    dump_stats(directory, "benchmark_after_output.json")
    
        
main(sys.argv[-1])