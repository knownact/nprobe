# Nprobe

​	**nprobe** 是一款用于解析网络流量、提取关键信息的探针软件，能够将流量或pcap文件解析后，提取并匹配指定数据内容后，以netflow格式传输至采集器。

​	除提取网络层相关信息，亦可解析HTTP、DNS、ICMP等应用层协议。

​	通过配置指纹规则库，支持提取应用层协议相关应用、设备、操作系统等绑定到IP详细扩展信息，也支持识别应用层的威胁行为，或其他匹配目标特征的网络行为。

​	规则命中的数据包可以根据需求以文件方式同步留存，供后续调查验证使用。

## 项目介绍

### 组织结构

```
nprobe
├─── .dep/         --pl0文件
├─── m4/           --m4宏文件
├─── plugins/      --插件
├─── fp-pattern/   --综合测绘识别指纹规则
├─── l7-pattern/   --应用层协议识别指纹规则
|─ ......
└─ nprobe.c        --主体代码
```



### 环境依赖

编译环境

```
GCC
automake
autoconf
libtool
libpcap
PF_RING (可选)
```

运行环境

```
libpcap
PF_RING (可选)
```



### 编译安装

```
sh ./configure
make
sudo make install
```



## 运行示例

通过参数指定数据源、运行模式、解析格式、采集器位置等。

### 基本参数

```
# nprobe -h 
nprobe -n <host:port|none> [-i <interface|dump file>] [-f <filter>]
              [-G] [-O <# threads>] [-w <hash size>] [-e <flow delay>]
              [-T <flow template>] [-U <flow template id>]
              ......
[--collector|-n] <host:port|none>   | Address of the NetFlow collector(s).
                                    | Multiple collectors can be defined using
                                    | multiple -n flags. In this case flows
                                    | will be sent in round robin mode to
                                    | all defined collectors if the -a flag
                                    | is used. Note that you can specify
                                    | both IPv4 and IPv6 addresses.
                                    | If you specify none as value,
                                    | no flow will be export; in this case
                                    | the -P parameter is mandatory.
[--interface|-i] <iface|pcap>       | Interface name from which packets are
                                    | captured, or .pcap file (debug only)
[--bpf-filter|-f] <BPF filter>      | BPF filter for captured packets
                                    | [default=no filter]
[--daemon-mode|-G]                  | Start as daemon.
[--num-threads|-O] <# threads>      | Number of packet fetcher threads
                                    | [default=2]. Use 1 unless you know
                                    | what you're doing.
[--hash-size|-w] <hash size>        | Flows hash size [default=32768]
[--flow-delay|-e] <flow delay>      | Delay (in ms) between two flow
                                    | exports [default=1]
[--flow-templ|-T] <flow template>   | Specify the NFv9 template (see below).
--pcap-file-list <filename>         | Specify a filename containing a list
                                    | of pcap files.
                                    | If you use this flag the -i option will be
                                    | ignored.
......

```



### 基础示例

以守护进程形式在后台运行，监听eth0网卡的数据流量，解析MAC、IP、L4协议、端口、数据量等基础信息，以netflow形式发送至127.0.0.1:9995。

```
# nprobe -T "%IN_SRC_MAC %OUT_DST_MAC %IPV4_SRC_ADDR %IPV4_DST_ADDR %PROTOCOL %L4_SRC_PORT %L4_DST_PORT %TCP_FLAGS %SRC_TOS %IN_PKTS %IN_BYTES" -n 127.0.0.1:9995 -e 0 -w 32768 -G -i eth0
```



## 插件使用

### 服务识别插件 - ServicePlugin

​		通过数据包传输层载荷进行正则模式匹配，结合资产指纹规则，识别数据流应用层协议，目标IP的中间件服务、设备种类、操作系统等资产信息；结合威胁指纹规则，识别指定类型的威胁流量。

​		指纹规则存放于 **fp-pattern/** 目录中，包含以JSON格式书写的五类规则：

```
service.json	-- 应用层协议与服务识别规则
​device.json	-- 硬件设备识别规则
​os.json		-- 操作系统识别规则
​midware.json	-- 软件平台与中间件规则
​threat.json	-- 威胁流量识别规则
```



​		指纹规则通过数个字段指定匹配条件与标记结果，例如：

```
{
    "midware":{
        "rules":{
            "40001":{
                "type":"Web Service",	-- 命中后类型标识，输出至XXX_TYPE字段
                "name":"Nginx",			-- 命中后名称标识，输出至XXX_NAME字段
                "protocol":"tcp",		-- 指定传输层协议
                "port":"80",			-- 指定端口
                "is_http":1,			-- 指定是否为HTTP流量
                "regex":"Server: nginx(?:\\/(\\d*\\.?\\d*\\.?\\d*))?",	-- 正则语句
                // "version":""			-- 使用指定字符串声明版本信息；未设置字段时,
                //						-- 提取第一个正则子表达式命中内容作为版本信息
            },
            "49999":{
            }
        }
    }
}
            
```



​		指定字段，在采集数据过程中进行规则匹配，获取到服务、设备、操作系统、中间件的类型、名称、版本等信息以及威胁流量的描述信息。插件留存规则命中的数据包，并通过微秒级的时间戳，对指定数据包进行定位查找。

```
# nprobe -T "%IN_SRC_MAC %OUT_DST_MAC %IPV4_SRC_ADDR %IPV4_DST_ADDR %PROTOCOL %L4_SRC_PORT %L4_DST_PORT %TCP_FLAGS %SRC_TOS %IN_PKTS %IN_BYTES %SRV_TYPE %SRV_NAME %SRV_VERS %DEV_TYPE %DEV_NAME %DEV_VEND %DEV_VERS %OS_TYPE %OS_NAME %OS_VERS %MID_TYPE %MID_NAME %MID_VERS %THREAT_TYPE %THREAT_NAME %THREAT_VERS %ICMP_DATA %ICMP_SEQ_NUM %ICMP_PAYLOAD_LEN %SRV_TIME %DEV_TIME %OS_TIME %MID_TIME %THREAT_TIME" -n 127.0.0.1:9995 -e 0 -w 32768 -i eth0
```



### DNS协议解析插件 - DNSPlugin

​		解析PCAP文件的数据流量，实现对DNS协议内容的解析，获取DNS查询域名，查询类型，查询结果关联IP。

```
# nprobe -T "%IN_SRC_MAC %OUT_DST_MAC %IPV4_SRC_ADDR %IPV4_DST_ADDR %PROTOCOL %L4_SRC_PORT %L4_DST_PORT %TCP_FLAGS %SRC_TOS %IN_PKTS %IN_BYTES %DNS_REQ_DOMAIN %DNS_REQ_TYPE %DNS_RES_IP" -n 127.0.0.1:9995 -e 0 -w 32768 -i eth0
```



### HTTP协议解析插件 - HTTPPlugin

​		解析PCAP文件的数据流量，实现对HTTP协议内容的解析，获取HTTP协议头部字段信息。

```
# nprobe -T "%IN_SRC_MAC %OUT_DST_MAC %IPV4_SRC_ADDR %IPV4_DST_ADDR %PROTOCOL %L4_SRC_PORT %L4_DST_PORT %TCP_FLAGS %SRC_TOS %IN_PKTS %IN_BYTES %HTTP_URL %HTTP_REQ_METHOD %HTTP_HOST %HTTP_MIME %HTTP_RET_CODE %HTTP_USER_AGENT" -n 127.0.0.1:9995 -e 0 -w 32768 -i eth0
```



## 许可证

* GNU GENERAL PUBLIC LICENSE  Version 3