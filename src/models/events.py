from datetime import datetime
from sqlalchemy import TIMESTAMP, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductEvent(Base):
    __tablename__ = "product_events"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True)
    event_type: Mapped[str]
    client_id: Mapped[str]
    event_data: Mapped[JSON] = mapped_column(JSON)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
