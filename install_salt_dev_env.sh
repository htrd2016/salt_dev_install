if [ ! -d "./salt" ];
then
#自己folk出来的github路径
git clone https://github.com/htrd2016/salt.git

cd salt

#将原作者项目更新的内容同步到我的本地项目
git remote add upstream https://github.com/htrd2016/salt.git

git fetch upstream

#迁出2016.3版本
git checkout 2016.3
git branch --set-upstream-to upstream/2016.3
git pull --rebase

else
echo "./salt 文件已经存在..."
fi

echo $(pwd)

#安装python-devel
sudo yum install python-devel

#安装沙箱
sudo yum install python-virtualenv.noarch

install_path=/home/$(whoami)/salt_dev_env
mkdir -p $install_path
virtualenv $install_path

source $install_path/bin/activate

codepath=`pwd`

sudo yum install openssl-devel
sudo yum install swig
pip install cherrypy
pip install M2Crypto    # Don't install on Debian/Ubuntu (see below)
pip install pyzmq PyYAML pycrypto msgpack-python jinja2 psutil futures tornado
pip install -e $codepath/salt   # the path to the salt git clone from above

#***************bin/salt-master 注释前3行

mkdir -p $install_path/etc/salt
mkdir -p $install_path/etc/salt/master.d
mkdir -p $install_path/srv
mkdir -p $install_path/srv/reactor

echo -e "external_auth:\n  pam:\n    $(whoami):\n      - .*\n      - '@wheel'\n      - '@runner'" > $install_path/etc/salt/master.d/auth.conf
echo -e "reactor:\n  - 'salt/netapi/hook/mycompany/build/*':\n    - $install_path/srv/reactor/react_ci_builds.sls"  > $install_path/etc/salt/master.d/reactor.conf
echo -e "install nano on my minion:\n  local.pkg.install:\n    - tgt: '*'\n    - arg:\n      - nano"  > $install_path/srv/reactor/react_ci_builds.sls
echo -e "rest_cherrypy:\n  port: 8000\n  disable_ssl: True" > $install_path/etc/salt/master.d/api.conf
cp $codepath/salt/conf/master $codepath/salt/conf/minion $install_path/etc/salt/

#cd $install_path

cp $codepath/salt/conf/master $codepath/salt/conf/minion $install_path/etc/salt/

sed -i "1iuser: $(whoami)" $install_path/etc/salt/master
sed -i "2ipublish_port: 12345" $install_path/etc/salt/master
sed -i "3iret_port: 12346" $install_path/etc/salt/master
sed -i "4iroot_dir: $install_path/srv" $install_path/etc/salt/master
sed -i "5iauto_accept: True" $install_path/etc/salt/master
sed -i "6isock_dir: $install_path/var/run/salt/master" $install_path/etc/salt/master

sed -i "1iuser: $(whoami)" $install_path/etc/salt/minion
sed -i "2imaster: localhost" $install_path/etc/salt/minion
sed -i "3iid: saltdev" $install_path/etc/salt/minion
sed -i "4imaster_port: 12346" $install_path/etc/salt/minion
sed -i "5iroot_dir: $install_path/srv" $install_path/etc/salt/minion

salt-master -c $install_path/etc/salt -d
salt-minion -c $install_path/etc/salt -d
sleep 2
#salt-key -c $install_path/etc/salt -L
#salt-key -c $install_path/etc/salt -A
sleep 2
salt-api -c $install_path/etc/salt -d
sleep 2
salt -c $install_path/etc/salt '*' test.ping

