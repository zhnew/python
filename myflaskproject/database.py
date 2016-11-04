import sqlite3,hashlib,time

def isSQLite3(filename):
    from os.path import isfile, getsize

    if not isfile(filename):
        return False
    if getsize(filename) < 100: # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)

    return header[:16] == b'SQLite format 3\x00'

def initDb():
    dbname='info.db'
    if isSQLite3(dbname):
        return
    conn=sqlite3.connect(dbname)
    c=conn.cursor()
    c.execute('''create table usr (name text primary key,pwd text)''')
    c.execute('''create table book (name text primary key,content blob,uptime text)''')
    c.execute('''
        create table visitlog (bname text,tag text, vtime text,
            FOREIGN KEY(bname) references book(name))
            ''')
    conn.commit()
    conn.close()


class Db:
    
    def __init__(self,dbname):
        self.conn=sqlite3.connect(dbname)

    def addUser(self,name,pwd):
        c=self.conn.cursor()
        pwd=hashlib.md5(pwd.encode('utf-8')).hexdigest()
        c.execute("insert into usr(name,pwd) values (?,?)",(name,pwd))
        self.conn.commit()

    def __del__(self):
        #close(self)
        pass
        
    def close(self):
        self.conn.close()

    def checkUsr(self,name,pwd):
        pwd=hashlib.md5(pwd.encode('utf-8')).hexdigest()
        c=self.conn.cursor()
        c.execute("select pwd from usr where name=:who",{"who":name})
        row=c.fetchone()
        if row is None:
            rs="user %s not exists"%name
            return rs
        if row[0]!=pwd:
            rs="password for %s is wrong"%name
            return rs
        return ''

    def addBook(self,name,content):
        uptime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        c=self.conn.cursor()
        c.execute("insert into book(name,content,uptime) values(?,?,?)",(name,content,uptime))
        self.conn.commit()
    
    def _clear_(self):
        c=self.conn.cursor()
        c.execute("delete from usr")
        c.execute("delete from book")
        self.conn.commit()

if __name__ == "__main__":
    initDb()
    db=Db(name=None)
    db._clear_()
    db.addUser("zaq12wsx","zaq12wsx")
    db.checkUsr("zaq12wsx","zaq12wsx")
    '''content=None
    with open('pdf.pdf', 'rb') as f: 
        content=sqlite3.Binary(f.read())
    db.addBook('css book',content)'''

