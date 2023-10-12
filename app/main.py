#import uvicorn
from fastapi import (
    FastAPI
)

from routes import user

tags_metadata = [
    {
        "name": "users",
        "description": "Операции над пользователями",
    },
]
# пробовал по разному, но так и не удалось отсортировать так как хочу.
# хочу чтоб шли методы get, post, put, delete в рамках тега users . а у меня вот так https://prnt.sc/TMmzr8pOuPY_

app = FastAPI(
    docs_url="/swagger",
    title="HW 16",
    summary="ДЗ 16",
    version="0.0.1",
    contact={
        "name": "Oleg Pravlutski",
    },
    openapi_tags=tags_metadata
)

app.include_router(user.router)

# uvicorn main:app --reload
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
