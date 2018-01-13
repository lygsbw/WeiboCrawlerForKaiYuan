import ConfigParser


class DBConfig:
        def __init__(self):
            pass
        cf = ConfigParser.ConfigParser()
        cf.readfp(open('DBConfig/DBConfig.ini'))
        host = cf.get('db', 'host')
        port = int(cf.get('db', 'port'))
        user = cf.get('db', 'user')
        passwd = cf.get('db', 'passwd')
        db = cf.get('db', 'db')
        charset = cf.get('db', 'charset')
        use_unicode = cf.get('db', 'use_unicode')
