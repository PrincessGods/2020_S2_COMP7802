import os
import json

def fileProcess(file):
    f = open(file, )
    dictsp = json.load(f)

    url = list()
    for i in dictsp:
        if i["method"] == 'GET' or\
            i["method"] == 'get' or\
            i["method"] == None:
            data = "/?"
            count = 1
            size = len(i['name'])
            for n in i['name']:
                if count != size:
                    data += n + "=1&"
                else:
                    data += n + "=1"

                count += 1
            url.append(i['form'] + data)

    f.close()

    f = open(file, 'w')
    f.write('')
    f.close()

    print(url)
    return url

if __name__ == '__main__':
    print("[Info] Start crawling")
    os.system("scrapy crawl crawler -t json -O spider.json")
    fileProcess("spider.json")