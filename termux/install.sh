apt update
apt upgrade
echo 'Setting up $HOME/storage'
termux-setup-storage
apt update
apt install -y openssh
