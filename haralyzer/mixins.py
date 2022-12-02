"""Mixin Objects that allow for shared methods"""
from collections.abc import MutableMapping
from typing import Any, Dict, Optional, Union
from functools import cached_property


def _list_to_dict(list_: list[dict[str, str]]) -> dict[str, str]:
    return {
        dict_["name"].strip(): dict_["value"].strip()
        for dict_ in list_
        if not dict_["name"].startswith(":")
    }


class GetHeaders:
    # pylint: disable=R0903
    """Mixin to get a header"""

    def get_header_value(self, name: str) -> Optional[str]:
        """
        Returns the header value of the header defined in ``name``

        :param name: Name of the header to get the value of
        :type name: str
        :return: Value of the header
        :rtype: Optional[str]
        """
        for header in self.raw_entry["headers"]:
            if header["name"].lower() == name.lower():
                return header["value"]
        return None

    def get_headers(self) -> dict[str, str]:
        """Returns headers as a dictionary"""
        return _list_to_dict(self.headers)


class GetCookies:
    """Mixin to get cookies"""

    def get_cookies(self) -> dict[str, str]:
        return _list_to_dict(self.cookies)


class GetPostData:
    """Mixin to get post data for a Request"""

    def get_post_data(self) -> Union[dict[str, str], Any]:
        return _list_to_dict(self.post_data["params"])


class MimicDict(MutableMapping):
    """Mixin for functions to mimic a dictionary for backward compatibility"""

    def __getitem__(self, item: str) -> Any:
        return self.raw_entry[item]

    def __len__(self) -> int:
        return len(self.raw_entry)

    def __delitem__(self, key):
        del self.raw_entry[key]

    def __iter__(self):
        return iter(self.raw_entry)

    def __setitem__(self, key, value):
        self.raw_entry[key] = value


class HttpTransaction(GetHeaders, GetCookies, MimicDict):
    """Class the represents a request or response"""

    def __init__(self, entry: dict):
        self.raw_entry = entry
        super().__init__()

    # Base class gets properties that belong to both request/response
    @cached_property
    def headers(self) -> list:
        """
        Headers from the entry

        :return: Headers from both request and response
        :rtype: list
        """
        return self.raw_entry["headers"]
