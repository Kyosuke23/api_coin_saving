from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースURLの設定
# この例ではカレントディレクトリにsql_app.dbというデータベースを作成する。
SQLALCHEMY_DATABASE_URL = "sqlite:///./private_db.db"

# SQLAlchemyのengineの作成
engine = create_engine(
   SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# セッションクラスの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラスの作成
Base = declarative_base()