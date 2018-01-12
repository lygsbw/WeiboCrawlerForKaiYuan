import MySQLdb


def getUnfinishedID():
    try:
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='ouyang1000',
            db='weibocrawler',
            port=3306)
        cur = conn.cursor()
        print 'unfinishedID update begin...'
        count = cur.execute('delete from unfinishedid where _id in (select _id from finishedid)')
        print count, ' accounts has been deleted from unfinished'
        print 'unfinishedID update finish...'
        print 'select 10000 accounts from unfinishedID'
        cur.execute(
            'SELECT _id FROM weibocrawler.unfinishedID limit 10000;')
        # print 'unfinished_id: ', count
        result = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return [x[0] for x in result]
    except MySQLdb.Error as e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
