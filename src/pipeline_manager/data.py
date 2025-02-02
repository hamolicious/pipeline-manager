from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    id: int
    username: str
    name: str
    state: str
    locked: bool
    avatar_url: str
    web_url: str
    created_at: str
    bio: str
    location: str
    public_email: str
    skype: str
    linkedin: str
    twitter: str
    discord: str
    website_url: str
    organization: str
    job_title: str
    pronouns: str
    bot: bool
    work_information: str
    followers: int
    following: int
    local_time: str


@dataclass
class CommitStatus:
    additions: int
    deletions: int
    total: int


@dataclass
class Commit:
    id: str
    short_id: str
    created_at: str
    parent_ids: list[str]
    title: str
    message: str
    author_name: str
    author_email: str
    authored_date: str
    committer_name: str
    committer_email: str
    committed_date: str
    trailers: Any
    extended_trailers: Any
    web_url: str
    stats: CommitStatus
    status: str
    project_id: int
    last_pipeline: "Pipeline"


@dataclass
class Job:
    id: int
    status: str
    stage: str
    name: str
    ref: str
    tag: bool
    coverage: str
    allow_failure: bool
    created_at: str
    started_at: str
    finished_at: str
    erased_at: str
    duration: float
    queued_duration: float


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
