<center>ES</center>
----
查看所有索引

```
curl -XGET http://$URL:$PORT/_cat/indices?v

集群有认证：
curl -XGET http://$USER:$PASSWD@$URL:$PORT/_cat/indices?v
```

###ES快照备份

@(Md)


1.注册仓库
```
快照仓库命令的几个参数
location:   指定快照的存储位置。必须要有
compress: 指定是否对快照文件进行压缩. 默认是 true.
chunk_size: 如果需要在做快照的时候大文件可以被分解成几块。这个参数指明了每块的字节数。也可用不同的单位标识，比如：1g，10m，5k等，默认是 null (表示不限制块大小)。
    
max_restore_bytes_per_sec: 每个节点恢复数据的最高速度限制. 默认是 20mb/s
max_snapshot_bytes_per_sec: 每个节点做快照的最高速度限制。默认是 20mb/s
```
创建命令
```
curl -XPUT 'http://127.0.0.1:9200/_snapshot/backup' -d '{"type": "fs","settings": {"location":"/data/es_bak","max_snapshot_bytes_per_sec" : "50mb", "max_restore_bytes_per_sec" :"50mb"}}'
```
><font color="red">注意</font> location 目录 集群所有机器都要能访问到         -------------->nfs
```bash
curl -XPUT http://$URL:$PORT/_cat/indices?v
```