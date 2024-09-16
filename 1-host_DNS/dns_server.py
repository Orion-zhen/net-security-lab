from dnslib import *
from dnslib.server import *
import os
import sys
import time
import threading


class suppress_stdout_stderr(object):
    """
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    """

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])


class TestResolver:
    namemap = {}

    def addname(self, name, ip):
        TestResolver.namemap[name] = ip
        # print(TestResolver.namemap)

    def getname(self, name):
        return TestResolver.namemap[name]

    def delname(self, name):
        if (name) in TestResolver.namemap:
            TestResolver.namemap.remove[name]
        # print(TestResolver.namemap)

    def resolve(self, request, handler):
        reply = request.reply()
        qname = request.q.qname
        qtype = request.q.qtype
        TestResolver.namemap["get"] = "true"
        TestResolver.namemap["getstr"] = str(qname)
        if str(qname) in TestResolver.namemap:
            replyip = TestResolver.namemap[str(qname)]
            rqname = TestResolver.namemap["reply"]
            TestResolver.namemap["reply"] = "null"

            answer = RR(rname=rqname, ttl=10, rdata=A(replyip))
            reply.add_answer(answer)
            return reply
        ## 调价其他的域名对应的IP，在这里加if语句增加

        ## 未匹配到时的返回值
        reply.header.rcode = getattr(RCODE, "NXDOMAIN")
        return reply


resolver = TestResolver()


def pt():
    while True:
        if resolver.getname("get") == "true":
            print("this msg:")
            print(resolver.getname("getstr"))
            resolver.addname("get", "false")


def main():
    resolver.addname("get", "false")  # add a A record
    resolver.addname("falsestr", "")  # add a A record
    resolver.addname("reply", "null")  # add a A record
    resolver.addname("www.aa.com.", "192.168.0.1")  # add a A record
    resolver.addname("www.bb.com.", "192.168.0.2")  # add a A record
    resolver.addname("www.test123.com.", "12.168.0.102")  # add a A record

    # logger = DNSLogger(prefix=False)
    with suppress_stdout_stderr():
        dns_server = DNSServer(resolver, port=53, address="0.0.0.0")

        dns_server.start_thread()


if __name__ == "__main__":
    t = threading.Thread(target=main)
    with suppress_stdout_stderr():
        t.start()
    msg = threading.Thread(target=pt)
    msg.start()
    while True:
        replyip = input("")
        replyip = replyip.replace(" ", "_")
        # resolver.delname(replyip)	# add a A record
        resolver.addname("reply", replyip)  # add a A record
        print(replyip)
