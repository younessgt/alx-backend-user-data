#!/usr/bin/env python3
""" DB module """


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ adding user to database """

        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """"finding the user based on kwargs"""
        if not kwargs:
            raise (InvalidRequestError)
        arg_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in arg_keys:
                raise (InvalidRequestError)

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise (NoResultFound)

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ updating the user"""

        user = self.find_user_by(id=user_id)
        arg_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in arg_keys:
                raise ValueError

        for key, val in kwargs.items():
            setattr(user, key, val)

        self._session.commit()
