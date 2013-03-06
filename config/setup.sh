# install node
sudo apt-get update
sudo apt-get install git-core curl build-essential openssl libssl-dev -y
git clone https://github.com/joyent/node.git
cd node
./configure
make
sudo make install
node -v

#install less.js
curl https://npmjs.org/install.sh | sudo sh
npm -v
sudo npm install less

#less doesn't automatically add itself to the path :(
#sudo updatedb
#sudo ln -s `locate lessc|tail -n1` /usr/bin