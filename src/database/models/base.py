import re
from typing import Any, Final, Optional, Pattern, Type, cast

from sqlalchemy import Column, func, inspect
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeMeta, declared_attr, has_inherited_table, registry
from sqlalchemy.util import ImmutableProperties

mapper_registry = registry()

TABLE_NAME_REGEX: Pattern[str] = re.compile(r'(?<=[A-Z])(?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z])')
PLURAL: Final[str] = 's'


class BaseModel(metaclass=DeclarativeMeta):
    abstract = True
    mapper_args = {'eager_defaults': True}

    def init(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    registry = mapper_registry
    metadata = mapper_registry.metadata

    @declared_attr
    def tablename(self) -> Optional[str]:
        if has_inherited_table(cast(Type[BaseModel], self)):
            return None
        cls_name = cast(Type[BaseModel], self).__qualname__
        table_name_parts = re.split(TABLE_NAME_REGEX, cls_name)
        formatted_table_name = ''.join(
            table_name_part.lower() + '_' for i, table_name_part in enumerate(table_name_parts)
        )
        last_underscore = formatted_table_name.rfind('_')
        return formatted_table_name[:last_underscore] + PLURAL

    def _get_attributes(self) -> dict[Any, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def str(self) -> str:
        attrs = '|'.join(str(v) for k, v in self._get_attributes().items())
        return f'{self.__class__.__qualname__} {attrs}'

    def repr(self) -> str:
        table_attrs = cast(ImmutableProperties, inspect(self).attrs)
        primary_keys = ' '.join(
            f'{key.name}={table_attrs[key.name].value}'
            for key in inspect(self.__class__).primary_key
        )
        return f'{self.__class__.__qualname__}->{primary_keys}'

    def as_dict(self) -> dict[Any, Any]:
        return self._get_attributes()


class TimedBaseModel(BaseModel):
    abstract = True

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now(), server_default=func.now())