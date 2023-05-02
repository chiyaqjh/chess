import sqlite3

# 连接到数据库，如果不存在则自动创建
conn = sqlite3.connect('test.db')

# 创建一个游标对象
cursor = conn.cursor()

# 执行一条SQL语句，创建名为users的表
cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')

# 执行一条SQL语句，插入一些用户记录
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('alice', '123456'))
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('bob', 'qwerty'))

# 提交事务
conn.commit()

# 关闭游标和数据库连接
cursor.close()
conn.close()