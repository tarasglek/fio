#!env python
"""
Script fills filesystem to X percentage
"""
import os
import sys
import math

def to_mb(number):
    "mb"
    return str(round(number / 1000 / 1000)) + "MB"

def cmd(cmdstr):
    "run command"
    print cmdstr
    os.system(cmdstr)

def main(targetdir, fio):
    """
    f_blocks - total number of blocks
    f_bavail - number of blocks available
    f_bsize - block size
    """
    statvfs = os.statvfs(targetdir)
    blocks_already_filled = statvfs.f_blocks - statvfs.f_bavail
    blocks_desired = math.floor(statvfs.f_blocks * 0.95)
    blocks_to_fill = blocks_desired - blocks_already_filled
    bytes_to_fill = blocks_to_fill * statvfs.f_bsize
    print "need to fill " + (to_mb(bytes_to_fill))
    dest_file = targetdir + "/work_file.fio"
    result_file = targetdir + "/big.json"
    fio_str = ("./fio.arm --name=randwrite --rw=randwrite "
               "--eta=always --sync=1 --output-format=json "
               " --bs=%s --size=%d --filename=%s --output %s")
    fio_cmd = (fio_str % ("4k", 50 * 1000 * 1000, dest_file, result_file + ".before"))
    cmd(fio_cmd)
    fio_str = ("./fio.arm --name=randwrite --rw=randwrite "
               "--eta=always --sync=1 --output-format=json "
               " --bs=%s --size=%d --filename=%s --output %s")
    fio_cmd = (fio_str % ("1M", bytes_to_fill, dest_file, result_file + ".fill"))
    cmd(fio_cmd)
    fio_str = ("./fio.arm --name=randwrite --rw=randwrite "
               "--eta=always --sync=1 --output-format=json "
               " --bs=%s --size=%d --filename=%s --output %s")
    fio_cmd = (fio_str % ("4k", 50 * 1000 * 1000, dest_file, result_file + ".after"))
    cmd(fio_cmd)



if __name__ == "__main__":
    TARGET_DIR = sys.argv.pop(1)
    FIO = sys.argv.pop(1)
    main(TARGET_DIR, FIO)
