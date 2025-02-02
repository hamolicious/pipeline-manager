from dataclasses import dataclass


@dataclass
class Pipeline:
    id: int
    iid: int
    project_id: int
    sha: str
    ref: str
    status: str
    source: str
    created_at: str
    updated_at: str
    web_url: str
    name: str
    is_latest: bool
