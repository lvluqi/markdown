>Centos 7 系统优化脚本

```bash
#!/bin/bash
# time:


# get kernel version
RELEASEVER=$(rpm -q --qf "%{VERSION}" $(rpm -q --whatprovides redhat-release))

# configure yum source
cd /etc/yum.repos.d/
mkdir /etc/yum.repos.d/backup
mv /etc/yum.repos/d/*.repo /etc/yum.repos.d/bak
if [ ${RELEASEVER}x != x ];then
    wget http://mirrors.163.com/.help/CentOS${RELEASEVER}-Base-163.repo -O init.repo
fi

#if [ $RELEASEVER == 7 ];then
#    wget http://mirrors.163.com/.help/CentOS7-Base-163.repo -O init.repo
#fi

yum -y clean all
yum check-updata

# install base rpm package
yum -y install epel-release
yum -y install nc vim iftop iotop dstat tcpdump net-tools
yum -y install ipmitool bind-libs bind-utils
yum -y install libselinux-python ntpdate

# updata rpm package include kernel
yum -y updata
rm -rf /etc/yum.repos.d/CentOS*

# update ulimit configure
if [ $RELEASEVER == 6 ];then
    test -f /etcsecurity/limits.d/90-nproc.conf && rm -rf /etc/security/limits.d/90-nproc.conf && touch /etc/security/limits.d/90=cproc.conf
fi
if [ $RELEASEVER == 7 ];then
    test -f /etcsecurity/limits.d/20-nproc.conf && rm -rf /etc/security/limits.d/20-nproc.conf && touch /etc/security/limits.d/20=cproc.conf
fi

>/etc/security/limits.conf
cat >> /etc/security/limits.conf <<EOF
* soft nproc 65535
* hard nproc 65535
* soft nofile 65535
* hard nofile 65535
EOF

# set timezone
test -f /etc/localtime && rm -rf /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# set LANG
sed -i 's@LANG=.*$LANG="en_US.UTF-8"$g' /etc/sysconfig/i18n

# update time
if [ $RELEASEVER == 6 ];then
    /usr/sbin/ntpdate pool.ntp.org
    grep -q ntpdate /var/spool/cron/root
    if [ $? -ne 0 ];then
        echo '* * * * * /usr/sbin/ntpdate ntp.aliyun.com > /dev/null/ 2>&1' >> /var/spool/cron/root
    fi
    /etc/init.d/crond restart
fi
if [ $RELEASEVER == 7 ];then
    yum -y install chrony
    > /etc/chrony.conf
cat >> /etc/security/limits.conf <<EOF
server pool.ntp.org lburst
stratumweight 0
driftfile /var/lib/chrony/drift
rtcsync
makestep 10 3
bindcmdaddress 127.0.0.1
bindcmdaddress ::1
commandkey 1
keyfile /etc/chrony.keys
generatecommandkey
noclientlog
logchange 0.5
logdir /var/log/chrony
EOF
fi

# clean iptables default rules
if [ $RELEASEVER == 6 ];then
    /sbin/iptables -F
    /etc/init.d/iptables save
    chkconfig ip6tables off
fi
if [ $RELEASEVER == 7 ];then
    systemctl disable firewalld
fi


# disable unuserd service
chkconfig auditd off

# disable ipv6
cd /etc/modprobe.d/ && touch ipv6.conf
> /etc/modprobe.d/ipv6.conf
cat >> /etc/modprobe.d/ipv6.conf << EOF
alias net-pf-10 off
alias ipv6 off
EOF


# disable iptable nat moudule
cd /etc/modprobe.d/ && touch connectiontracking.conf
> /etc/modprobe.d/connectiontracking.conf
cat >>/etc/modprobe.d/connectiontracking.conf <<EOF
install nf_nat /bin/true
install xt_state /bin/true
install iptable_nat /bin/true
install nf_conntrack /bin/true
install nf_defrag_ipv4 /bin/true
install nf_conntrack_ipv4 /bin/true
install nf_conntrack_ipv6 /bin/true
EOF

# disable SELINUX
setenforce 0
sed -i 's/^SELINUX=.*$/SELINUX=disabled/' /etc/selinux/config

# update record command
sed -i 's/^HISTSIZE=.*$/HISTSIZE=100000/' /etc/profile
grep -q 'HISTTIMEFORMAT' /etc/profile
if [[ $? -eq 0 ]];then
    sed -i 's/^HISTTIMEFROMAT=.*$/HISTTIMEFORMAT="%F %T "/' /etc/profile
else
    echo 'HISTTIMEFORMAT="%F %T "/' >>  /etc/profile
fi

# install dnsmasq and update configure
yum -y install dnsmasq
> /etc/dnsmasq.conf
cat >> /etc/dnsmasq.conf << EOF
listen-address 127.0.0.1
no-dhcp-interface lo
log-queries
log-facility=/var/log/dnsmasq.log
all-servers
no-negcache
cache-size=1024
dns-firward-max=512
EOF

if [ $RELEASEVER == 6 ];then
    /etc/init.d/dnsmasq restart
fi
if [ $RELEASEVER == 7 ];then
    systemctl restart dnsmasq
fi

# update /etc/resolv.conf
> /etc/resolv.conf
cat >> /etc/resolv.conf << EOF
search xxx.com
options timeout:1
nameserver 114.114.114.114
EOF

# update /etc/sysctl.conf
sed -i 's/net.ipv4.tcp_syncookies.*/net.ipv4.tcp_syncookies = 1/g' /etcsysctl.con
cat >> /etc/sysctl.conf << EOF
kernel.core_users_pid=1
kernel.core_pattern=/tmp/core-%e-%p
fs.suid_dumpable=2
net.ipv4.tcp_tw_reuse=1
net.ipv4.tcp_tw_recycle=0
net.ipv4.tcp_timestamps=1
EOF

sysctl -p
```





