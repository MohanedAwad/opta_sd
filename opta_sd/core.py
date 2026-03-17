from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import Any, Optional

import httpx
from lxml import etree

from .cache import CacheBackend, NoCache
from .config import load_config
from .exceptions import APIError, MissingParameterError, ParseError

logger = logging.getLogger(__name__)

_OPTA_DATE_FMT       = "%Y%m%dT%H%M%S%z"
_OPTA_DATE_FMT_NAIVE = "%Y%m%dT%H%M%S"


def _format_date(dt: datetime) -> str:
    return dt.strftime(_OPTA_DATE_FMT if dt.tzinfo else _OPTA_DATE_FMT_NAIVE)


class Core:
    """
    Asynchronous base class shared by all OPTA SDAPI feed classes.
        result = await AsyncMatch().resource("abc").live().get()
        print(result.data)

    Parameters
    ----------
    config_path : str, optional
    timeout : int
    retries : int
    cache : CacheBackend, optional
    """

    _endpoint:  str = ""
    _base_path: str = "soccerdata"

    def __init__(
        self,
        config_path: Optional[str] = None,
        timeout: int = 30,
        retries: int = 3,
        cache: Optional[CacheBackend] = None,
    ):
        cfg = load_config(config_path)
        self._domain   = cfg["opta_domain"]
        self._token    = cfg["opta_auth_token"]
        self._headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": cfg["referer_domain"],
        }
        self._timeout  = timeout
        self._retries  = retries
        self._cache    = cache or NoCache()

        self._resource_id: Optional[str]  = None
        self._core_params: dict[str, Any] = {}
        self._feed_params: dict[str, Any] = {}

        self._data:             Any                      = None
        self._raw_response:     Optional[httpx.Response] = None
        self._from_cache:       bool                     = False
        self._response_time_ms: Optional[float]          = None

    # ------------------------------------------------------------------
    # Core query-string parameters (mirrors Core exactly)
    # ------------------------------------------------------------------

    def response_type(self, value: str) -> "Core":
        self._core_params["_rt"] = value
        return self

    def format(self, value: str = "json") -> "Core":
        self._core_params["_fmt"] = value
        return self

    def locale(self, value: str) -> "Core":
        self._core_params["_lcl"] = value
        return self

    def callback(self, value: str) -> "Core":
        self._core_params["_clbk"] = value
        return self

    def sort_order(self, value: str) -> "Core":
        self._core_params["_ordSrt"] = value
        return self

    def page_size(self, value: int) -> "Core":
        self._core_params["_pgSz"] = int(value)
        return self

    def page_number(self, value: int) -> "Core":
        self._core_params["_pgNm"] = int(value)
        return self

    # ------------------------------------------------------------------
    # URL helpers
    # ------------------------------------------------------------------

    def __build_url(self) -> str:
        if not self._endpoint:
            raise MissingParameterError("Feed endpoint is not defined.")
        parts = [self._domain, self._base_path, self._endpoint, self._token]
        if self._resource_id:
            parts.append(self._resource_id)
        return "/".join(parts)

    def __build_params(self) -> dict:
        return {**self._core_params, **self._feed_params}

    def _cache_key(self) -> str:
        url    = self.__build_url()
        params = "&".join(f"{k}={v}" for k, v in sorted(self.__build_params().items()))
        return f"{url}?{params}"


    async def get(self) -> "Core":
        
        key = self._cache_key()
        hit = self._cache.get(key)
        if hit is not None:
            self._data, self._from_cache, self._response_time_ms = hit, True, 0.0
            return self

        url, params = self.__build_url(), self.__build_params()
        transport   = httpx.AsyncHTTPTransport(retries=self._retries)

        t0 = time.monotonic()
        print(f"GET {url} with params {params}...")
        async with httpx.AsyncClient(transport=transport,
                                      timeout=self._timeout,
                                      headers=self._headers,
                                      ) as client:
            self._raw_response = await client.get(url, params=params)
        self._response_time_ms = (time.monotonic() - t0) * 1000
        logger.debug("ASYNC GET %s → %d (%.0f ms)",
                     self._raw_response.url,
                     self._raw_response.status_code,
                     self._response_time_ms)

        if not self._raw_response.is_success:
            raise APIError(self._raw_response.status_code, self._raw_response.text[:500])

        fmt = self._core_params.get("_fmt", "json")
        self._data = (self.__parse_xml(self._raw_response.text)
                      if fmt == "xml"
                      else self.__parse_json(self._raw_response.text))
        self._from_cache = False
        self._cache.set(key, self._data)
        return self

    def __parse_json(self, text: str) -> Any:
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ParseError(f"Failed to parse JSON: {exc}") from exc

    def __parse_xml(self, text: str) -> etree._Element:
        try:
            return etree.fromstring(text.encode())
        except etree.XMLSyntaxError as exc:
            raise ParseError(f"Failed to parse XML: {exc}") from exc

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def data(self) -> Any:
        if self._data is None:
            raise RuntimeError("No data — call `await .get()` first.")
        return self._data

    @property
    def raw_response(self) -> Optional[httpx.Response]:
        return self._raw_response

    @property
    def from_cache(self) -> bool:
        return self._from_cache

    @property
    def response_time_ms(self) -> Optional[float]:
        return self._response_time_ms

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} endpoint={self._endpoint!r} "
                f"resource={self._resource_id!r} params={self.__build_params()}>")