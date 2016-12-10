io_bytes is actually in KB
consider doing some cpu burning on a thread..to ramp up cpu frequnecy
fio --name=randwrite --iodepth=1 --rw=randwrite --bs=4k --direct=0 --size=500M --numjobs=1 --group_reporting --eta=always --sync=1 --output fsync
android log message: The application may be doing too much work on its main ...
f2fs paper https://www.usenix.org/conference/fast15/technical-sessions/presentation/lee
https://lwn.net/Articles/685499/ multi-stream interface
https://www.usenix.org/system/files/conference/atc16/atc16_paper-min.pdf f2fs ext4 scaling
https://www.usenix.org/legacy/event/fast12/tech/full_papers/Kim.pdf benchmarking phones
/proc/diskstats is a way to count amount of IOs
