from typing import List, TypeAlias

from gitlab.base import RESTObject, RESTObjectList
from gitlab.v4.objects import ProjectCommit

from .data import Commit, Pipeline

Pipelines: TypeAlias = RESTObjectList | List[RESTObject]


def raw_pipeline_to_pipeline(pipelines: Pipelines) -> list[Pipeline]:
    wrapped_pipelines = []
    is_first = True

    for p in pipelines:
        new_pipeline = Pipeline(
            id=p.id,
            iid=p.iid,
            project_id=p.project_id,
            sha=p.sha,
            ref=p.ref,
            status=p.status,
            source=p.source,
            created_at=p.created_at,
            updated_at=p.updated_at,
            web_url=p.web_url,
            name=p.name,
            is_latest=is_first,
        )

        wrapped_pipelines.append(new_pipeline)
        is_first = False

    return wrapped_pipelines


def raw_commit_to_commit(raw_commit: ProjectCommit) -> Commit:
    return Commit(
        id=raw_commit.id,
        short_id=raw_commit.short_id,
        created_at=raw_commit.created_at,
        parent_ids=raw_commit.parent_ids,
        title=raw_commit.title,
        message=raw_commit.message,
        author_name=raw_commit.author_name,
        author_email=raw_commit.author_email,
        authored_date=raw_commit.authored_date,
        committer_name=raw_commit.committer_name,
        committer_email=raw_commit.committer_email,
        committed_date=raw_commit.committed_date,
        trailers=raw_commit.trailers,
        extended_trailers=raw_commit.extended_trailers,
        web_url=raw_commit.web_url,
        stats=raw_commit.stats,
        status=None,
        project_id=raw_commit.project_id,
        last_pipeline=None,
    )
