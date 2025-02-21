import random

import arrow
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from ..components.image import Image
from ..components.pills import Icons, build_pipeline_pill
from ..data import Commit, Pipeline
from ..gitlab_api import login


class PipelineAuthor(Widget):
    DEFAULT_CSS = """
        PipelineAuthor {
            width: 7;
            height: 7;
            padding: 0;
            margin: 0;
        }
    """

    def __init__(
        self,
        commit: Commit,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        self.commit = commit
        gl = login()

        self.user = list(gl.users.list(username=self.commit.author_name))[0]
        self.log.debug(self.user.avatar_url)

    def compose(self) -> ComposeResult:
        yield Image(self.user.avatar_url, 6, 6)
