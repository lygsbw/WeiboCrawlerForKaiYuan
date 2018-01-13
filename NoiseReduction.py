# coding:utf-8
import re
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def NoiseReduction(inputFileName, outputFileName='output.csv'):
    data = []

    with open(inputFileName, 'r') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for line in reader:
            # print line['Content']
            raw_data = line['Content']
            raw_data = raw_data.strip().replace(' ', '').replace(u'全文', '')  # 去空格,全文两字
            # raw_data = re.sub(r'@(.*?) ', '', raw_data)     # 去除@:  @papi酱
            raw_data = re.sub(r'\[.*?\]', '', raw_data)  # 去除表情: [赞],[鼓掌]...
            raw_data = re.sub(r'(http://(\w+|\.|/)+)', '', raw_data)  # 去除链接: http://..
            raw_data = re.sub(r'\d{6,}', '', raw_data)  # 去除6位以上的数字
            line['Content'] = raw_data
            data.append(line)

    with open(outputFileName, "wb") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames=header, extrasaction='ignore')
        writer.writeheader()  # 写入表头
        writer.writerows(data)  # row为字典类型


def NoiseReduction(data):
    print 'noise reduction begin...'
    for i in xrange(len(data)):
        raw_data = data[i]['Content']
        raw_data = raw_data.strip().replace(' ', '').replace(u'全文', '')  # 去空格,全文两字
        # raw_data = re.sub(r'@(.*?) ', '', raw_data)     # 去除@:  @papi酱
        raw_data = re.sub(r'\[.*?\]', '', raw_data)  # 去除表情: [赞],[鼓掌]...
        raw_data = re.sub(r'(http://(\w+|\.|/)+)', '', raw_data)  # 去除链接: http://..
        raw_data = re.sub(r'\d{6,}', '', raw_data)  # 去除6位以上的数字
        data[i]['Content'] = raw_data
    print 'noise reduction finish..'

if __name__ == '__main__':
    NoiseReduction('weibo_content.csv', '1.csv')


