IP=`ifconfig | awk '/inet addr/{print substr($2,6)}'|tail -n 1`
TARBALL=termux.tgz
tar -czvf $TARBALL -C termux .
echo wget http://$IP:8000/$TARBALL '&&' tar zxvf $TARBALL
python -m SimpleHTTPServer
