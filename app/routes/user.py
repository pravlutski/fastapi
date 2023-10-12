from fastapi import APIRouter, HTTPException, status
from schemas.user import (
    UserListSchema,
    UserDetailResponse,
    UserCreateRequest,
    UserCreateResponse,
    UserUpdateRequest,
    UserUpdateResponse
)
from managers.user import UserManager


router = APIRouter()


@router.get(
    '/users',
    tags=['users'],
    name="Список всех",
    response_model=list[UserListSchema]
)
def get_all_users(page: int = 1, limit: int = 5):
    try:
        if page <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="param page > 0")
        if limit <= 0 or limit > 100:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="param limit between (>= 0 <= 100)")

        result = UserManager().get_list(page=page, limit=limit)
        if result is not None:
            return result

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid response")
    except HTTPException as e:
        # с try тут и далее напутал наверно. но если return HTTPException... то код возвращает 200.
        # https://prnt.sc/74fDFZrJep8q
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get(
    '/user/{user_id}',
    tags=['users'],
    name="Детальная информация"
)
def get_detail_user(user_id: int) -> UserDetailResponse:
    try:
        result = UserManager().get_by_id(pk=user_id)
        if result is not None:
            return UserDetailResponse(**result.__dict__)

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.post(
    '/user',
    status_code=status.HTTP_201_CREATED,
    tags=['users'], name="Создать",
    response_description="Пользователь успешно создан"
)
def create_user(user: UserCreateRequest):
    try:
        params = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        result = UserManager().add(params)
        if result is not None:
            return UserCreateResponse(**result.__dict__)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid response")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.put(
    '/user/{user_id}',
    response_model=UserUpdateRequest,
    tags=['users'],
    name="Обновить",
    response_description="Пользователь успешно обновлен"
)
def update_user(user_id: int, user: UserUpdateRequest) -> UserUpdateResponse:
    try:
        params = {
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        result = UserManager().update(id=user_id, params=params)
        if result is not None:
            return UserUpdateResponse(**result.__dict__)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid update")
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.delete(
    '/user/{user_id}',
    tags=['users'],
    name="Удалить",
    response_description="Пользователь успешно удален"
)
def delete_user(user_id: int):
    try:
        result = UserManager().get_by_id(pk=user_id)
        if result is not None:
            UserManager().remove(pk=user_id)
            result = UserManager().get_by_id(pk=user_id)
            if result is None:
                return {"success": True}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not deleted. Try again")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
