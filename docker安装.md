#docker安装

| docker版本     |  系统版本 |      
| :-------- | --------:|
| 17.05-ce    |   Centos 7.4 |

>开始部署

```bash
wget url
yum localinstall *.rpm
```
>docker配置镜像仓库加速器


```json
vim /etc/docker/daemon.json
{
  "registry-mirrors": ["https://kpdd3a5q.mirror.aliyuncs.com"]
}
```
>重新加载docker systemctl
```bash
systemctl daemon-reload
docker info 查看修改的镜像仓库
```

```xml
<pom>version 3.2.1</pom>
```