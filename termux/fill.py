#!python
"""
Script fills filesystem to X percentage
"""
import os
import sys
import math
from shutil import copyfile

def to_mb(number):
    "mb"
    return str(round(number / 1000 / 1000)) + "MB"

def cmd(cmdstr):
    "run command"
    print(cmdstr)
    os.system(cmdstr)

def calc_bytes_to_fill(directory, ratio):
    "dir: directory, ratio: % of space to fill"
    statvfs = os.statvfs(directory)
    # blocks_already_filled:950675 desired_fill_blocks:342344 blocks_to_fill:1293019
    # posix.statvfs_result(f_bsize=4096, f_frsize=4096, f_blocks=1306080, f_bfree=1174591, f_bavail=1163359, f_files=1397757, f_ffree=1392826, f_favail=1392826, f_flag=3078, f_namemax=255)
    blocks_already_filled = statvfs.f_blocks - statvfs.f_bavail # 1306080 - 1163359 = 142721
    desired_fill_blocks = math.floor(statvfs.f_blocks * ratio) # 
    blocks_to_fill = desired_fill_blocks - blocks_already_filled
    print ("blocks_already_filled:%d desired_fill_blocks:%d blocks_to_fill:%d"
           % (blocks_already_filled, blocks_to_fill, desired_fill_blocks))
    bytes_to_fill = blocks_to_fill * statvfs.f_bsize
    return (bytes_to_fill, statvfs.f_blocks * statvfs.f_bsize)

def main(fast_targetdir, media_targetdir, fio):
    """
    f_blocks - total number of blocks
    f_bavail - number of blocks available
    f_bsize - block size
    """
    (bytes_to_fill, total) = calc_bytes_to_fill(fast_targetdir, 1)
    print ("need to fill %s/%s" %
           (to_mb(bytes_to_fill), to_mb(total)))

    short_benchmark_file_size = 100 * 1000 * 1000
    bytes_to_fill -= short_benchmark_file_size + 200 * 1000 * 1000 # also a mb for stats
    if bytes_to_fill <= 0:
        # todo check for files from previous run so we don't have to reallocate
        print "Ended up with -ve bytes_to_fill:%d" % bytes_to_fill
        sys.exit(1)
    bytes_to_fill = int(bytes_to_fill)
    fast_dest_file = fast_targetdir + "/work_file.fio"
    media_dest_file = media_targetdir + "/work_file.fio"

    log_prefix = fast_targetdir + "/benchmark"
    copyfile("/proc/mounts", log_prefix + "_mounts")
    timeout = 60
    fio_str = ("{fio} --name=randwrite --rw=randwrite --timeout={timeout}m     "
               "--eta=always --sync=1 --output-format=json "
               "--write_bw_log={log_prefix} --write_lat_log={log_prefix} --write_iops_log={log_prefix} "
               "--log_store_compressed=1 "
               " --bs={bs} --size={size} --filename={filename} --output {log_prefix}_output.json")
    cmd(fio_str.format(fio=fio,
                       bs="4k",
                       log_prefix=log_prefix + "_before",
                       size=short_benchmark_file_size,
                       filename=fast_dest_file, timeout=timeout))
    num_chunks = 10
    for i in range(0, num_chunks):
        suffix = "" if i == 0 else "_fill_" + str(i)
        cmd(fio_str.format(fio=fio, log_prefix=log_prefix+"_fill" + suffix,
                           bs="4k", size=bytes_to_fill / num_chunks,
                           filename=fast_dest_file + suffix, timeout=timeout/num_chunks))
    cmd(fio_str.format(fio=fio, log_prefix=log_prefix+"_after", bs="4k", size=short_benchmark_file_size, filename=fast_dest_file, timeout=timeout))
    return
    try:
        os.unlink(fast_dest_file)
        os.unlink(media_dest_file)
    except Exception:
        pass


if __name__ == "__main__":
    print("Usage: %s <fast_target_dir> <media_target_dir> <FIO>" % sys.argv[0])
    if len(sys.argv) == 4:
        FAST_TARGET_DIR = sys.argv.pop(1)
        MEDIA_TARGET_DIR = sys.argv.pop(1)
        FIO = sys.argv.pop(1)
    else:
        FAST_TARGET_DIR = '.'
        MEDIA_TARGET_DIR = '/storage/emulated/0'
        FIO = "./fio.arm"
    main(FAST_TARGET_DIR, MEDIA_TARGET_DIR, FIO)
