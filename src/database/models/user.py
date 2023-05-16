import sqlalchemy as sa
from sqlalchemy.dialects.mysql import ENUM

from src.database.models.base import TimedBaseModel
from src.database.services.enums import UserStatusEnum


class User(TimedBaseModel):
    user_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=False, index=True)
    full_name = sa.Column(sa.VARCHAR(255), nullable=False)
    mention = sa.Column(sa.VARCHAR(300), nullable=False)
    status = sa.Column(ENUM(UserStatusEnum), nullable=False, default=UserStatusEnum.ACTIVE)


