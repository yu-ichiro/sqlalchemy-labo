from typing import Union, Type, TypeVar


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Bundle
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.base import Executable
# noinspection PyProtectedMember
from sqlalchemy.sql.elements import Label
from sqlalchemy.sql.operators import Operators


T = TypeVar('T')
engine = create_engine('sqlite:///sqlite.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class UserSetting(Base):
    __tablename__ = 'user_settings'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    setting_key = Column(String(128))
    setting_value = Column(String(128))
    
    __table_args__ = UniqueConstraint('user_id', 'setting_key'),


class SingleBundle(Bundle):
    single_entity = True


class Alias(Label):
    def __init__(self, element, name=None, type_=None):
        super().__init__(name, element, type_)

    # @property
    # def ref(self):
    #    val = _textual_label_reference(self.name)
    #    return val

    def value_at(self, row):
        return getattr(row, self.name)


class CustomModelMeta(type):
    def __new__(typ, name, bases, namespace):
        _aliases = []
        for attr, clause in namespace.items():
            if isinstance(clause, Operators):
                _aliases.append(Alias(clause, attr))
                
        bundle = SingleBundle(name, *_aliases)
        for alias in _aliases:
            setattr(bundle, alias.name, alias)
        print(bundle)
        return bundle


class CustomModel(metaclass=CustomModelMeta):
    test = User.id
    

# Pycharm がGeneric Aliasに対応する日までおあずけ
Col = Union[T, Alias]


def col(_type: Type[T], column: Operators) -> Union[T, Alias]:
    return column  # type: Any
