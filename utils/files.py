from __future__ import annotations
from typing import TypedDict

import base64

from django.core.exceptions import ValidationError


def get_asset_directory_path(_, filename: str) -> str:
    VALID_PATHS = ["assignment", "avatar"]
    for path in VALID_PATHS:
        if filename.startswith(path):
            return path
    return "untitled"


class DATA_SCHEME_JSON(TypedDict):
    media_type: str
    media_format: str
    media_data: str
    decoded_media_data: bytes


def parse_data_scheme(data_scheme: str) -> DATA_SCHEME_JSON:
    # data:image/jpeg;base64,BASE64_ENCODED_JPEG_IMAGE_DATA

    raw_data: list = data_scheme.split(";", maxsplit=1)

    media_type: list = raw_data[0].split(":")
    if media_type[0] == "data":
        _type: str = media_type[1].split("/")[0]
        _format: str = media_type[1].split("/")[1]
    else:
        raise ValidationError("Invalid Image data scheme")

    media_data: list = raw_data[1].split(",", maxsplit=1)
    if media_data[0] == "base64":
        _media_data: str = media_data[1]
    else:
        raise ValidationError("Invalid Image data scheme")

    _decoded_media_data: bytes = base64.b64decode(_media_data)

    _json = {
        "media_type": _type,
        "media_format": _format,
        "media_data": _media_data,
        "decoded_media_data": _decoded_media_data,
    }
    return _json
