from __future__ import annotations
from typing import TypedDict

import io
import base64

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_asset_directory_path(__, filename: str) -> str:
    VALID_PATHS = ["assignment", "avatar"]
    for path in VALID_PATHS:
        if filename.startswith(path):
            return f"{path}/{filename}"
    return f"untitled/{filename}"


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
        raise ValidationError(_("Invalid Image data scheme"))

    media_data: list = raw_data[1].split(",", maxsplit=1)
    if media_data[0] == "base64":
        _media_data: str = media_data[1]
    else:
        raise ValidationError(_("Invalid Image data scheme"))

    _decoded_media_data: bytes = base64.b64decode(_media_data)
    buffer = io.BytesIO(_decoded_media_data)

    _json = {
        "type": _type,
        "format": _format,
        "data": _media_data,
        "file_like": buffer,
    }
    return _json
