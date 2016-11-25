io_bytes is actually in KB
consider doing some cpu burning on a thread..to ramp up cpu frequnecy
fio --name=randwrite --iodepth=1 --rw=randwrite --bs=4k --direct=0 --size=500M --numjobs=1 --group_reporting --eta=always --sync=1 --output fsync
