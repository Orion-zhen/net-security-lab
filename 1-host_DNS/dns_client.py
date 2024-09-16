#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
循环解析
"""

import re
import os
import sys


def getDigResult(dnsserver, url, mytype):
    for line in range(1):
        result = os.popen(
            "dig @" + dnsserver + " " + url + " " + mytype
        ).readlines()  # 在控制台输入解析的域名,获取解析结果
        # print(result)

        for i in range(len(result)):
            if "ANSWER SECTION" in result[i]:
                a = result[i + 1]
                a = a.replace(". ", ".	")
                c = a.split(".	")[0]
                b = c.replace("_", " ")

                if b != "null":
                    print(b)
                ip = re.findall(
                    r"(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])", str(a), 0
                )  # 提取出解析出来的ip
                # if ip == ['12.12.12.27'] or ['12.12.12.26']:    # 判断解析出来的ip是否正确-----no use
                # print (ip)        # 在控制台打印出每次解析出来的ip
                # else:
                # print ('error')


if __name__ == "__main__":
    list_of_args = sys.argv
    try:
        while True:
            getDigResult(list_of_args[1], list_of_args[2], list_of_args[3])
    except KeyboardInterrupt:
        sys.exit(0)
