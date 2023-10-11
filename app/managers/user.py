from datetime import datetime

from database import session
from managers.base import BaseManager
from models.user import User
from helpers import htmlspecialchars, validate_email
from fastapi import HTTPException, status


class UserManager(BaseManager):
    def __init__(self):
        super().__init__()
        self.entity = User

    def get_list(self, **kwargs) -> object:
        return self._list(**kwargs)

    def detail(self, pk: int) -> object:
        return self.get_by_id(pk)

    def add(self, params: dict) -> bool | object:
        email = htmlspecialchars(params["email"])
        if not validate_email(email):
            raise ValueError("Введенный емейл невалиден")

        # проверяем нет ли уже такого пользователя по еймейл
        res = session.query(self.entity).filter_by(email=email).scalar()
        if res is not None:
            raise ValueError(f"Email уже используется в ID = '{res.id}'")

        first_name = htmlspecialchars(params["first_name"])
        last_name = htmlspecialchars(params["last_name"])
        if len(first_name) < 3 or len(last_name) < 3:
            raise ValueError("Введите имя и фамилию")

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        self._save(user)  # Add the user

        if user.id is not None:
            return self.get_by_id(pk=user.id)
        return False

    def update(self, id: int, params: dict) -> None | object:
        user = self.get_by_id(pk=id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

        email = ""
        if "email" in params:
            email = htmlspecialchars(params["email"])
            if len(email) > 0:
                if not validate_email(email):
                    raise ValueError("Введенный емейл невалиден")

                # проверяем нет ли уже такого еймейла у другого пользователя
                res = session.query(User).filter(User.id != id, User.email == email).scalar()
                if res is not None:
                    raise ValueError(f"Email используется у другого пользователя c ID = '{res.id}'")
                user.email = email

        first_name = htmlspecialchars(params["first_name"])
        last_name = htmlspecialchars(params["last_name"])

        if len(first_name) > 2:
            user.first_name = first_name
        else:
            raise ValueError("Имя > 2 символов")

        if len(last_name) > 2:
            user.last_name = last_name
        else:
            raise ValueError("Фамилия > 2 символов")

        user.updated_at = datetime.now()
        self._save(user)  # Update the user

        return self.get_by_id(pk=user.id)

    def remove(self, pk) -> None:
        self._delete(pk=pk)
