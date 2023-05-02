from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建数据库连接
engine = create_engine('mysql+pymysql://username:password@host:port/database_name')

# 创建Session对象
Session = sessionmaker(bind=engine)
session = Session()

# 进行数据库操作
result = session.query(User).filter(User.username == 'test').first()

# 关闭Session
session.close()