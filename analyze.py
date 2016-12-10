import json
import os
import sys
import re
def main(directory):
    for entry in sorted(os.listdir(directory)):
        match = re.search(r'fill_fill.*json$', entry)
        if not match:
            continue
        filename = "%s/%s" % (directory, entry)
        stats = json.loads(open(filename).read())
        clat = stats["jobs"][0]["write"]["clat"]["percentile"] 
        print "%s,%s" % (clat["50.000000"],clat["99.000000"])

main(sys.argv[-1])