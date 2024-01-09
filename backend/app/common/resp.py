from fastapi import status
from fastapi.responses import JSONResponse  # , ORJSONResponse
from pydantic import BaseModel
from typing import Union, Optional
import datetime
import decimal
import json
import typing

from common.error_code import ErrorBase


class DateEncoder(json.JSONEncoder):
    """
    解决dict 转json 时 datetime 转换失败
    使用方法：json.dumps(data, cls=DateEncoder)
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def _render(self, content: typing.Any) -> bytes:
    return json.dumps(
        content,
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(",", ":"),
        cls=DateEncoder,
    ).encode("utf-8")


# 覆写JSONResponse类的render方法让其支持格式化datatime类型数据
# setattr(JSONResponse,'render',_render)

class MyJSONResponse(JSONResponse):
    pass
    # def render(self, content: typing.Any) -> bytes:
    #     return json.dumps(
    #         content,
    #         ensure_ascii=False,
    #         allow_nan=False,
    #         indent=None,
    #         separators=(",", ":"),
    #         cls=DateEncoder,
    #     ).encode("utf-8")


setattr(MyJSONResponse, 'render', _render)


class respJsonBase(BaseModel):
    code: int
    msg: str
    data: Union[dict, list]


def respSuccessJson(data: Union[list, dict, str] = None, msg: str = "Success"):
    """ 接口成功返回 """
    if not data and not isinstance(data, list) and not isinstance(data, dict):
        data = {}
    return MyJSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 0,
            'msg': msg,
            'data': data
            # 'data': json.dumps(data or {}, cls=DateEncoder)
        }
    )


def respVodJson(data: Union[list, dict, str] = None):
    """ 接口成功返回 """
    if not data and not isinstance(data, list) and not isinstance(data, dict):
        data = {}
    return MyJSONResponse(
        status_code=status.HTTP_200_OK,
        content=data
    )


def respErrorJson(error: ErrorBase, *, msg: Optional[str] = None, msg_append: str = "",
                  data: Union[list, dict, str] = None, status_code: int = status.HTTP_200_OK):
    """ 错误接口返回 """
    return MyJSONResponse(
        status_code=status_code,
        content={
            'code': error.code,
            'msg': (msg or error.msg) + msg_append,
            'data': data or {}
        }
    )
