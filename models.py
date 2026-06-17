from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    query_type = Column(String)
    query_value = Column(String)
    result_name = Column(String)
    spotify_id = Column(String)
    searched_at = Column(DateTime, default=datetime.utcnow)