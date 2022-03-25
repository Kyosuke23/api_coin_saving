from database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, Date, DateTime

class SAVING_LOG(Base):
    __tablename__ = 'coin_saving_log'
    id = Column(Integer, primary_key=True, index=True)
    saving_date = Column(Date)
    amount = Column(Integer)
    total_amount = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
