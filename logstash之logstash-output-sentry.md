<center>logstash之logstash-output-sentry<center>
---
>插件开发源地址  http://clarkdave.net/2014/01/tracking-errors-with-logstash-and-sentry/

####安装[插件](https://github.com/javiermatos/logstash-output-sentry)
```bash
./bin/logstash-plugin install logstash-out-sentry
```

####收集php-fpm相关日志

```
input {
   file {
    path => "/var/log/php-fpm/error.log"
    type => "php-fpm-error"
  }
   file {
    path => "/var/log/php-fpm/www-slow.log"
    type => "php-fpm-slow"
  }
}

filter {
  if [type] == "php-error" {
    grok {
	  match => ["message","\[%{%{MONTHDAY}[./-]%{MONTH}[./-]%{YEAR} %{TIME}:datetime}\]\s+%{DATA:zone}\]\s+PHP\s+%{LOGLEVEL:severity}:\s+%{GREEDYDATA:errormessage}"]
	}
  
  }
  if [type] == "php-fpm-error" {
    grok {
	  match => ["message","\[%{%{MONTHDAY}[./-]%{MONTH}[./-]%{YEAR} %{TIME}:datetime}\]\s+%{LOGLEVEL:severity}:\s+%{GREEDYDATA:errormessage}"]
          remove_field => ["message"]
	}
    mutate { 
        add_field => {
          "host_ip" => "120.27.160.139"
          "[@metadata][sentry][server_name]" => "dev.jingsocial.com"
        }
        add_tag => ["dev"]
        #gsub => ["host","iZbp13lsytivlvvks4ulatZiZbp","dev-php-fpm-slow"]
        remove_field => ["@version","path","host"] 
    }
    date {
      match => ["@timestamp","YYYY-MM:dd HH:mm:ss"]
      target => "@timestamp"
      timezone =>  "Asia/Shanghai"
    }
    ruby {
      code => "event.timestamp.time.localtime+8*60*60"
    }
  }
  if [type] == "php-fpm-slow" {
    multiline {
	  pattern => '^(\[0x0|script_filename|$)'
	  what => 'previous'
	  negate => false
	}
	
    mutate {
      add_field => {
        "message" => "hahah"
        "host_ip" => "120.27.160.139"
      }
      add_tag => ["dev"]
      remove_field => ["@version","path","host","@timestamp"]
    }
#	grok {
#      patterns_dir => '/usr/local/logstash/patterns'
#      match => [
#        "message","%{PHP_FPM_SLOW_LOG}"
#      ]
#    }
  }
}

output{
  stdout {
    codec => rubydebug {"metadata" => true} 
  }

  sentry {
    "message" => "message"
    "server_name" => "[@metadata][sentry][server_name]"
    "environment" => "[tags][1]"
    "exception" => "[@metadata][sentry][exception]"
    #"user_value" => "nobody"


    "url" => "https://sentry.jingsocial.com/api"
    "key" => "9a55b6e183c744e28a813fb8c8a19bcf"
    "secret" => "faa95e5d681b47659002eaa5fa7b45fe"
    "project_id" => "9"
  }
}
```
>logstash-output-sentry [插件下载](https://github.com/javiermatos/logstash-output-sentry) 
>更多接口开发详情请祥阅https://sentry.io

###elasticsearch
```
input {
  file {
    path => "/var/log/elasticsearch/private_test.log"
    type => "es-error"
    
    #logstash高版本用codec multiline进行多行匹配
    codec => multiline {
      pattern => "^\["
      negate => true
      what => "previous"
    }
  }
  file {
    path => "/var/log/elasticsearch/private_test_index_search_slowlog.log"
    type => "es-slow"
  }

}

filter {
  if [type] == "es-error"{
    if "INFO" in [message] { drop { } }   #删除INFO
    mutate {
      add_tag => ["dev"]
      add_field => {
        "[@metadata][sentry][server_name]" => "dev.jingsocial.com" #添加server_name
        "host_ip" => "120.27.160.139"
      }
      remove_field => ["@timestamp","host","@version"]    #删除字段
    }
  }


  if [type] == "es-slow"{
    if ([message] =~ "^[\s\S]+\[[0-9]\.]{1,5}m") { drop{} }
    grok {
        match =>  { "message" => "^\[(?<timestamp>(\d\d){1,2}-(?:0[1-9]|1[0-2])-(?:(?:0[1-9])|(?:[12][0-9])|(?:3[01])|[1-9])\s+(?:2[0123]|[01]?[0-9]):(?:[0-5][0-9]):(?:(?:[0-5]?[0-9]|60)(?:[:.,][0-9]+)))\]\[(TRACE|DEBUG|WARN\s|INFO\s)\]\[(?<io_type>[a-z\.]+)\]\s\[(?<node>[a-z0-9\-\.]+)\]\s\[(?<index>[A-Za-z0-9\.\_\-]+)\]\[\d+\]\s+took\[(?<took_time>[\.\d]+)(?<took_time_type>(s|m))\]\,\s+took_millis\[(\d)+\]\,\s+types\[(?<types>([A-Za-z\_]+|[A-Za-z\_]*))\]\,\s+stats\[\]\,\s+search_type\[(?<search_type>[A-Z\_]+)\]\,\s+total_shards\[\d+\]\,\s+source\[(?<source>[\s\S]+)\]\,\s+extra_source\[[\s\S]*\]\,\s*$" }

        remove_field => ["message"]
    }
    mutate {
      add_tag => ["dev"]     #添加标签
      add_field => {
        "[@metadata][sentry][server_name]" => "dev.jingsocial.com"
        "host_ip" => "120.27.160.139"
      }
      remove_field => ["@timestamp","@version","host"]
    }
  }
}
output {
  if [type] == "es-error"{
  stdout {
    codec => "rubydebug"
  }
  sentry {
    "message" => "message"
    "server_name" => "[@metadata][sentry][server_name]"
    "environment" => "[tags][1]"
    #"exception" => "[@metadata][sentry][exception]"   #异常需要sentry exception接口


    "url" => "https://sentry.jingsocial.com/api"
    "key" => "9a55b6e183c744e28a813fb8c8a19bcf"
    "secret" => "faa95e5d681b47659002eaa5fa7b45fe"
    "project_id" => "9"
  }
 }
}
```
注意事项
```
logstash-output-sentry是ruby开发，可以看上述原作者开发指南可另行开发
output {
  sentry {
    'url' => "http://local.sentry:9000/api"
    'key' => "yourkey"
    'secret' => "yoursecret"
    'project_id' => "yourprojectid"
  }
}
默认值 logger > logstash 
      platform > other
      level > error
      server_name > host
      可以添加相应的字段进行赋值
eg:
  
filter{
  mutate{
    add_field => {
    "[@metadata][sentry][server_name]" => "dev.jingsocial.com"
    }
  }
}

output{
   sentry {
    'url' => "http://local.sentry:9000/api"
    'key' => "yourkey"
    'secret' => "yoursecret"
    'project_id' => "yourprojectid"
    "server_name" => [@metadata][sentry][server_name]  
    }
}

如此之后sentry server_name就会显示相对应的名字
```