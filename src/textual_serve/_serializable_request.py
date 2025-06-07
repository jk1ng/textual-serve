from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional

@dataclass
class SerializableRequest:
    method: str
    url: str
    path: str
    query_string: str
    query: Dict[str, str]
    headers: Dict[str, str]
    cookies: Dict[str, str]
    remote: Optional[str]
    content_type: str
    charset: Optional[str]
    body_text: Optional[str] = None
    body_json: Optional[Any] = None

    @classmethod
    async def from_request(cls, request) -> "SerializableRequest":
        body_text = None
        body_json = None

        if request.can_read_body:
            try:
                if request.content_type.lower() == "application/json":
                    body_json = await request.json()
                else:
                    body_text = await request.text()
            except Exception:
                body_text = None
                body_json = None

        return cls(
            method=request.method,
            url=str(request.url),
            path=request.path,
            query_string=request.query_string,
            query=dict(request.query),
            headers=dict(request.headers),
            cookies=dict(request.cookies),
            remote=request.remote,
            content_type=request.content_type,
            charset=request.charset,
            body_text=body_text,
            body_json=body_json,
        )