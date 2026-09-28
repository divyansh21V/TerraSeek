"""Provider adapters for live, standards-based satellite discovery."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from terraseek.models import STACSearchRequest, STACSearchResponse


class ProviderError(RuntimeError):
    """Raised when a remote provider cannot complete a search."""


@dataclass(frozen=True)
class EarthSearchProvider:
    """Public Element84 Earth Search STAC API adapter.

    Earth Search implements the standard STAC Item Search contract. The URL
    remains configurable so deployments can point at a private catalog.
    """

    base_url: str = os.getenv("TERRASEEK_STAC_URL", "https://earth-search.aws.element84.com/v1")
    timeout_seconds: float = 20.0

    def search(self, request: STACSearchRequest) -> STACSearchResponse:
        """Search catalog items by spatial, temporal, and quality constraints."""
        payload: dict[str, object] = {
            "bbox": request.bbox,
            "datetime": (
                f"{request.date_start.isoformat()}T00:00:00Z/"
                f"{request.date_end.isoformat()}T23:59:59Z"
            ),
            "collections": request.collections,
            "limit": request.limit,
        }
        if request.max_cloud_cover is not None:
            payload["query"] = {"eo:cloud_cover": {"lte": request.max_cloud_cover}}

        body = json.dumps(payload).encode("utf-8")
        endpoint = f"{self.base_url.rstrip('/')}/search"
        http_request = Request(
            endpoint,
            data=body,
            headers={"Accept": "application/geo+json", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(http_request, timeout=self.timeout_seconds) as response:
                result = json.load(response)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ProviderError(f"STAC provider request failed: {exc}") from exc

        items = result.get("features", [])
        if not isinstance(items, list):
            raise ProviderError("STAC response did not contain a FeatureCollection")
        return STACSearchResponse(
            provider="earth-search",
            catalog_url=self.base_url,
            matched=len(items),
            items=items,
        )
