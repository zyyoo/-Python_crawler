#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import re

def get_domain_conf_info(web_path):

    """
    获取服务器网站目录下配置文件,然后根据配置文件获取域名的网站目录
    :return:
    """
    name_pattern = re.compile('server_name(.*?);')
    path_pattern = re.compile('root(.*?_html);')
    time_pattern = re.compile('auto.py(.*?:\d\d)')
    index_pattern = re.compile('(index.*?);')

    ssl_patter = re.compile('ssl_certificate')
    ssl_patter_2 =re.compile('#\s+ssl_certificate')


    re_patter= re.compile("rewrite.*?(http.*?)permanent;")
    re_patter2 = re.compile("rewrite.*?(http.*?)$.*?request_uri;")

    acc_patter = re.compile('access_log\s.*?log')
    err_patter = re.compile('error_log\s.*?log')
    acc_patter_2 = re.compile('#\s*access_log\s.*?log')
    err_patter_2 = re.compile('#\s*error_log\s.*?log')

    file_list = os.listdir(web_path)
    print(len(file_list))
    with open(write_path, 'w') as f:
        for file in file_list:
            port = 80
            gzip = 1
            full_path = web_path+file
            #Ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(full_path)))
            #Etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(full_path)))

            Etime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(full_path)))
            try:
                with open(full_path,'r') as f1:
                    content = f1.read()
                    domain_name = name_pattern.search(content)
                    if domain_name:
                        domain_name=domain_name.group(1)
                    else:
                        domain_name=''

                    domain_url = path_pattern.search(content)
                    if domain_url:
                        domain_url=domain_url.group(1)
                    else:
                        domain_url=""

                    time1 = time_pattern.search(content)
                    if time1:
                        Etime=time1.group(1)

                    index_page = index_pattern.search(content)
                    if index_page:
                        index_page=index_page.group(1)
                    else:
                        index_page=''
                    ssl_status = ssl_patter.search(content)
                    ssl_status2 = ssl_patter_2.search(content)
                    if ssl_status and not ssl_status2:
                        ssl_status=1
                        port=443
                    else:
                        ssl_status=0

                    acc_log = acc_patter.search(content)
                    acc_log_2 = acc_patter_2.search(content)

                    if acc_log and not acc_log_2:
                        acc_log = 1
                    else:
                        acc_log=0

                    err_log = err_patter.search(content)
                    err_log_2 = err_patter_2.search(content)
                    if err_log and not err_log_2:
                        err_log = 1
                    else:
                        err_log=0
                    re_url = re_patter.search(content)
                    re_url2 = re_patter2.search(content)
                    #print(re_url)
                    if re_url and not re_url2:
                        re_301=1
                        re_url=re_url.group(1)
                        re_url =re_url.replace('','').strip()
                        print(re_url)
                    elif not re_url and re_url2:
                        re_301 = 1
                        re_url = re_url2.group(1)
                    else:
                        re_301=0
                        re_url=''

                    info = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}\n'.format                        (full_path.strip(),domain_name.strip(),domain_url,Etime,index_page.strip(),ssl_status,acc_log,err_log,port,ip,re_301,re_url,gzip,web_status,server,web_type)

                    f.write(info)

            except IOError as e :
                #print(e)
                f.write(full_path.strip()+',error,error,error,error,error,error,error,error,error,error,error,error\n')

if __name__ == '__main__':
    ip='211.149.172.175'
    write_path ='domain.csv'
    web_status='1'
    server='209'
    web_type='1'
    #web_path = ['/www/server/panel/vhost/nginx/']
    #web_path = ['/usr/local/nginx/conf/vhost/']
    web_path = ['/www/wdlinux/nginx/conf/vhost/']
    for web_path in web_path:
         get_domain_conf_info(web_path)
