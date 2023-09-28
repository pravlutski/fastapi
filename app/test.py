from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from schemas import user
from managers.user import UserManager

obj = UserManager()


# def create_user():
#     try:
#         params = {
#             "first_name": "",
#             "last_name": "user.last_name",
#             "email": "",
#         }
#         return obj.add(params)
#     except Exception as e:
#         print(e)
#         return HTTPException(status_code=404, detail=e)
#
# create_user()



try:
    result = UserManager().get_by_id(pk=1)
    print(result)
except Exception as e:
    print("sdfdsf")

