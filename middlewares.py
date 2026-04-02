from fastapi import Request, Depends
from db import get_session
from pprint import pprint
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.datastructures import URL, Headers


async def inject_db_connection(
        request: Request, call_next
):
    print(f'{call_next=}')
    response = await call_next(
        request,
        # get_session
    )
    print(f'{call_next=}')
    return response
