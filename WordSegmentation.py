import jieba
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def WordSegmentation(inputFileName, outputFileName='output.csv'):

    data = []
    with open(inputFileName, 'r') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for line in reader:
            oneWeibo = line['Content']
            segList = jieba.cut(oneWeibo)
            line['Content'] = "/".join(segList)
            data.append(line)

    with open(outputFileName, "wb") as g:
        writer = csv.DictWriter(
            g,
            delimiter=",",
            fieldnames=header,
            extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)


def WordSegmentation(data):
    print 'word segmentation begin..'
    for i in xrange(len(data)):
        raw_data = data[i]['Content']
        segList = jieba.cut(raw_data)
        data[i]['Content'] = ' '.join(segList)
    print 'word segmentation finish..'

if __name__ == '__main__':
    WordSegmentation('1.csv', '2.csv')
