from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum, ForeignKey, MetaData
from core.db.engine import Base
import enum
from core.db.models.user import User


class ResultEnum(enum.Enum):
    healthy = "healthy"
    unhealthy = "unhealthy"
    artifact = "artifact"


class Result(Base):
    result: Mapped[ResultEnum] = mapped_column(Enum(ResultEnum), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="results")
