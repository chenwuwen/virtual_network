# -*-coding:utf-8-*-

'''
DNS 解析
DNS处理模块dnspython
dnspython提供一个DNS解析器类——resolver，使用它的query方法来实现域名的查询功能。
query（self,qname,rdtype=1,rdclass=1,tcp=False,source=None,raise_on_no_answer=True,source_prot=0)
其中，qname参数为查询的域名，rdtype参数用来指定RR资源的类型，常用的类型如下：
A记录：将主机名转换成IP地址
MX记录：邮件交换记录，定义邮件服务器的域名
CNAME记录：指别名记录，实现域名间的映射。
NS记录：标记区域的域名服务器及授权子域
PTR记录：反向解析，与A记录相反，将地址换成主机名
SOA记录：SOA标记，一个起始授权区的定义。

rdclass参数用于指定网络类型，可选的值为IN,CH,HS，IN为默认，使用最广泛。
tcp参数用于指定查询是否启用TCP协议，默认不启用。
source和source_prot指定查询源地址和端口，默认值为查询设备IP地址和0。
raise_on_no_answer指定当查询无应答时是否触发异常，默认为TRUE。

'''

import dns.resolver
import http.client
import logger, datetime

ip_list = []  # 定义域名IP列表变量
app_domain = "www.baidu.com"  # 定义业务域名


# 域名解析函数，解析成功IP将追加到ip_list
def get_ip_list(domain=""):
    try:
        A = dns.resolver.query(domain, 'A')  # 解析A记录类型
        # SRV = dns.resolver.query(domain, 'SRV')  # 解析SRV记录类型
    except Exception as e:
        print("dns resolver error:" + str(e))
        return
    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == 1:
                ip_list.append(j.address)  # 追加到ip_list

    return True


'''
检查IP通断状态
'''


def checkIp(current_ip):
    check_url = current_ip + ":80"
    get_content = ""
    http.client.socket.setdefaulttimeout(5)  # 定义http连接超时时间(5秒)
    conn = http.client.HTTPConnection(check_url)  # 创建http连接对象

    try:
        conn.request("GET", "/", headers={"Host": app_domain})  # 发起URL请求，添加host主机头
        r = conn.getresponse()
        get_content = r.read(15)  # 获取URL页面前15个字符，以便做可用性校验,返回的是字节类型bytes
    finally:
        if get_content.lower().decode('utf-8') == "<!doctype html>":  # 监控URL页的内容一般是事先定义好，比如“HTTP200”等
            print(ip + " [OK]")
        else:
            print(ip + " [Error]")  # 此处可放告警程序，可以是邮件、短信通知


if __name__ == "__main__":
    if get_ip_list(app_domain) and len(ip_list) > 0:  # 条件：域名解析正确且至少要返回一个IP
        for ip in ip_list:
            checkIp(ip)
    else:
        print("DNS 解析错误")
