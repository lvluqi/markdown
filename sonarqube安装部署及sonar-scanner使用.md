<center>sonarqube安装部署及sonar-scanner使用<center>
---


-------------------
[TOC]

###一、sonarqube简介
>SonarQube能够提供对代码的检查扫描和分析功能，然后通过客户端或者软件插件的形式完成对各种环境和软件的支持[官网](https://www.sonarqube.org/)

环境说明参考[官网要求](https://docs.sonarqube.org/display/SONAR/Requirements)

|    软件   |    版本 |
| :-------- | --------:|
| 系统  | Centos 7.4 |
| jdk	| 1.8 |
| mysql | 5.7.21 |
|sonarqube|7.3|

###二、Sonarqube安装及部署
1.jdk
2.下载[SonarQube](https://www.sonarqube.org/downloads/)

####2.1 创建数据库
```bash
create database sonar character set urf8 collate utf8_general_ci;
grant all privileges on sonar.* to sonar@"%" identified by 'xxxx';
```
####2.2 解压Sonarqube安装包
```bash
#上传sonarqube安装包到相应目录
wget https://sonarsource.bintray.com/Distribution/sonarqube/sonarqube-7.3.zip
cd sonarqube-7.3 && ls

bin  conf  COPYING  data  elasticsearch  extensions  lib  logs  temp  web

#修改conf/sonar.properties配置文件
sonar.jdbc.username=sonar
sonar.jdbc.password=redhat
sonar.jdbc.url=jdbc:mysql://192.168.0.216:3306/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance&useSSL=false
sonar.jdbc.maxActive=60
sonar.jdbc.maxIdle=5
sonar.jdbc.minIdle=2
sonar.jdbc.maxWait=5000
sonar.jdbc.minEvictableIdleTimeMillis=600000
sonar.jdbc.timeBetweenEvictionRunsMillis=30000
sonar.web.host=0.0.0.0
sonar.web.port=9090
```

#### 2.3 创建用户
>由于elasticsearch的原因，因此sonar不允许root用户运行
```bash
#创建sonar用户
useradd sonar
passwd sonar

#赋予权限
chmod -R 777 /opt/sonar
```

#### 3 启动
```bash
#切换到sonar用户
/root/sonarqube-7.3/bin/linux-x86-64/sonar.sh start
```

#### 4 访问及欢呼


[参考](https://blog.csdn.net/beauxie/article/details/81157330)