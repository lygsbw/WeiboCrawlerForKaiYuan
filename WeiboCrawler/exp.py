import datetime
"""
import MySQLdb
from WeiboCrawler.weiboID import weiboID1

try:
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='ouyang1000', db='weibocrawler', port=3306)
    cur = conn.cursor()
    #count = cur.execute('(SELECT distinct fanID FROM weibocrawler.usersrelation) union (SELECT distinct followID FROM weibocrawler.usersrelation)')
    # print 'there has %s rows record' % count
    count = cur.execute('SELECT distinct UserID FROM weibocrawler.weibo')
    result = cur.fetchmany(count)
    #print result
    y = [x[0] for x in result]
    l = [x for x in weiboID1 if x not in y]
    print len(l)
    print l
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

str = '20170423'
now = datetime.datetime.strptime(str, '%Y%m%d')
# now = datetime.datetime.now()
oneDay = datetime.timedelta(days=60)
print (now-oneDay).strftime('%Y%m%d')
"""
endtime = '20170423'
endtime = datetime.datetime.strptime(endtime, '%Y%m%d')
oneDay = datetime.timedelta(days=1)
for i in range(29):
    starttime = endtime - oneDay
    print starttime.strftime('%Y%m%d') + '  ' + endtime.strftime('%Y%m%d')
    endtime = starttime - oneDay
