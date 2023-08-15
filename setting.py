from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# 接続先DBの設定
DATABASE = 'postgresql://root:root@localhost:5432/postgres'

# Engine の作成
Engine = create_engine(
    DATABASE,
)
Base = declarative_base()

# Sessionの作成
session = Session(
    autocommit=False,
    autoflush=True,
    bind=Engine
)

# modelで使用する
Base = declarative_base()
