import uuid
from datetime import datetime
from sqlalchemy import TIMESTAMP, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.base import Base


class ProductEvent(Base):
    __tablename__ = "product_events"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, index=True, default=uuid.uuid4)
    event_type: Mapped[str]
    client_id: Mapped[str]
    event_data: Mapped[JSON] = mapped_column(tuple=JSON)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
