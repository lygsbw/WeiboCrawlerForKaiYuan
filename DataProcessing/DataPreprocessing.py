# coding:utf-8
import re
import csv
import jieba
from RemovePunctuation import loadPunctuation


def noiseReduction(raw_data):
    # 降噪
    raw_data = raw_data.strip().replace(' ', '').replace(u'全文', '')  # 去空格,全文两字
    # raw_data = re.sub(r'@(.*?) ', '', raw_data)     # 去除@:  @papi酱
    raw_data = re.sub(r'\[.*?\]', '', raw_data)  # 去除表情: [赞],[鼓掌]...
    raw_data = re.sub(r'(http://(\w+|\.|/)+)', '', raw_data)  # 去除链接: http://..
    raw_data = re.sub(r'\d{6,}', '', raw_data)  # 去除6位以上的数字
    return raw_data


def removePunctuation(segList):
    # 去停用词
    punctuation = loadPunctuation()
    dataRP = [word for word in segList if punctuation.get(str(word), 0) != 1]
    dataRP = ' '.join(dataRP)
    return dataRP


def DataPreprocessing(inputFileName, outputFileName):
    data = []
    outToCSV = True
    if 'txt' in outputFileName:
        outToCSV = False
    with open(inputFileName, 'r') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        print "read file.."
        print "data preprocessing.."
        for line in reader:
            raw_data = line['Content']

            # 降噪
            dataNR = noiseReduction(raw_data)

            # 分词
            segList = jieba.cut(dataNR)

            # 去停用词
            dataRP = removePunctuation(segList)

            line['Content'] = dataRP
            if outToCSV:
                data.append(line)
            else:
                data.append(line['Content'])
    print "preprocessing finish.."
    print "save file.."
    if outToCSV:
        with open(outputFileName, "w") as g:
            writer = csv.DictWriter(g, delimiter=",", fieldnames=header, extrasaction='ignore')
            writer.writeheader()  # 写入表头
            writer.writerows(data)  # row为字典类型
    else:
        with open(outputFileName, 'w') as g:
            for c in data:
                if len(c) > 5:
                    g.write(c + '\n')
    # print "写入文件完成.."

if __name__ == '__main__':
    DataPreprocessing('unfinished.csv', 'finished.csv')
