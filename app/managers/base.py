from sqlalchemy.exc import IntegrityError
from database import session, engine
from sqlalchemy import select
from sqlalchemy.orm import load_only
from models.user import User


class BaseManager:
    LIMIT_ITEM_PAGE = 5

    def __init__(self) -> None:
        self.entity = None

    def _list(
            self, filter: list | None = None,
            options: tuple | None = None,
            limit: int | None = None,
            page: int | None = 0
    ) -> list:
        query = session.query(self.entity)
        if limit is not None and limit > 0:
            query = query.limit(limit)
            self.LIMIT_ITEM_PAGE = limit
        if page is not None and page > 1:
            query = query.offset((page - 1) * self.LIMIT_ITEM_PAGE)
        if filter is not None:
            query = query.filter(filter)
        if options is not None:
            query = query.options(options)

        return query.all()

    def _save(self, obj: object) -> None:
        try:
            session.add(obj)
            session.flush()
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise Exception(e)

    def _delete(self, pk: int) -> None:
        try:
            obj = self.get_by_id(pk=pk)
            if obj is not None:
                session.delete(obj)
                session.commit()
        except IntegrityError as e:
            session.rollback()
            raise Exception(e)

    def get_by_id(self, pk: int):
        return session.query(self.entity).filter_by(id=pk).scalar()
