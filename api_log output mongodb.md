<center>api_log output mongodb<center>
---
```bash
input {
    file {
    path => [ "/home/devinstance/sites/dev_jingsocial/protected/jingsocial_v2/backend/runtime/logs/api.log" ]
    #start_position => "beginning"
    #sincedb_path => "/dev/null"
    type => "api_log"
    }
}
filter {
    if ([message] !~ "[\s\S]+\[api-log\][\s\S]+" ) { drop {} }
    grok {
        match => { "message" => "([1-9][0-9]{3}\-([0][1-9]|[1][1-2])\-(0[1-9]|[12][0-9]|3[01]|[1-9])\s+[0-9]{2}:[0-9]{2}:[0-9]{2}) \[((?<![0-9])(?:(?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])[.](?:[0-1]?[0-9]{1,2}|2[0-4][0-9]|25[0-5]))(?![0-9]))\][\s\S]+\[(api\-log)\] Openid:(?<openid>[\s\S]+)Userid:(?<userid>[\s\S]+)Module_name:(?<module_name>[\s\S]+)Action_type:(?<action_type>[\s\S]+)Wid:(?<wid>[\s\S]+)Appid:(?<appid>[\s\S]+)Data:(?<data1>[\s\S]+)Create_time:(?<create_time>[\s\S]+)"}
         remove_field => ["message"]

    }
    json {
        source => "data1"
        target => "data"
        remove_field => ["data1"]
    }

    mutate { remove_field => ["@version","path","host","type"] }


    date {
        match => [ "datetime","yyyy-MM-dd HH:mm:ss"]
        target => ["@timestamp"]
    }
}

output {
    # stdout{
    #    codec => "rubydebug"
#}
    mongodb {
        collection => "jing_webtrack_data_record"
        database => "dev_jingsocial"
        uri => "mongodb://root:g5drb4pdf2thWs@120.27.160.139:27017"
        codec => "json"
    }
}
```