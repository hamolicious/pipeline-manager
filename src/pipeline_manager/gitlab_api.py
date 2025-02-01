import os
import subprocess

import gitlab
from gitlab.v4.objects import Project


class Config:
    GITLAB_URL = os.environ.get("GITLAB_HOST", "")
    GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "")

    @classmethod
    def valid(cls) -> bool:
        checks = [
            cls.GITLAB_URL != "",
            cls.GITLAB_TOKEN != "",
        ]

        return all(checks)


def get_git_remote_url() -> str | None:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() if result.stdout else None
    except subprocess.CalledProcessError:
        return None


def login() -> gitlab.Gitlab:
    assert Config.valid()

    gl = gitlab.Gitlab(url=Config.GITLAB_URL, private_token=Config.GITLAB_TOKEN)
    gl.auth()

    return gl


def get_current_project() -> Project:
    url = get_git_remote_url() or ""
    project = "/".join(url.replace(".git", "").split("/")[3::])

    gl = login()

    return gl.projects.get(project)


def get_pipelines(project: Project):
    return project.pipelines.list()
