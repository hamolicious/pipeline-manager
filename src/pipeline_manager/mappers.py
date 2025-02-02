from typing import Any, List, TypeAlias

from gitlab.base import RESTObject, RESTObjectList
from gitlab.v4.objects import ProjectCommit

from .data import Commit, CommitStatus, Job, Pipeline

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


def raw_jobs_to_jobs(jobs: List[RESTObject] | RESTObjectList) -> list[Job]:
    mapped_jobs = []

    for job in jobs:
        mapped_jobs.append(
            Job(
                job.id,
                job.status,
                stage=job.stage,
                name=job.name,
                ref=job.ref,
                tag=job.tag,
                coverage=job.coverage,
                allow_failure=job.allow_failure,
                created_at=job.created_at,
                started_at=job.started_at,
                finished_at=job.finished_at,
                erased_at=job.erased_at,
                duration=job.duration,
                queued_duration=job.queued_duration,
            )
        )

    return mapped_jobs


def raw_status_to_commit_status(status: Any) -> CommitStatus:
    return CommitStatus(
        additions=status.get("additions", 0),
        deletions=status.get("deletions", 0),
        total=status.get("total", 0),
    )


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
        stats=raw_status_to_commit_status(raw_commit.stats),
        status=raw_commit.status,
        project_id=raw_commit.project_id,
        # last_pipeline=raw_pipeline_to_pipeline([raw_commit.last_pipeline])[0],
        last_pipeline=Pipeline(**raw_commit.last_pipeline, name="", is_latest=False),
    )
