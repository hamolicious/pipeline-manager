from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, TypeAlias

import textual
from gitlab.base import RESTObject, RESTObjectList
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Rule

from .gitlab_api import get_current_project, get_pipelines


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


Pipelines: TypeAlias = RESTObjectList | List[RESTObject]


class PipelineListItem(Widget):
    DEFAULT_CSS = """
        PipelineListItem {
            width: 100%;
            height: 7;
        }

        Label {
            width: 100%;
            height: auto;
        }

        .pipeline-line {
            height: auto;
            margin-top: 1;
            padding-right: 2;
            padding-left: 2;
        }
    """

    class Text(Enum):
        SUCCESS = "Passed"
        WARNING = "Warning"
        FAILED = "Failed"
        SKIPPED = "Skipped"
        MANUAL = "Manual"

    class Colors(Enum):
        SUCCESS = "#0C522C"
        WARNING = "#6F3A0C"
        FAILED = "#8C1E0D"
        SKIPPED = "#333238"
        MANUAL = "#333238"
        GENERIC = "#323232"
        TEXT = "#AAAAAA"

    class Icons(Enum):
        SUCCESS = ""
        WARNING = ""
        FAILED = ""
        SKIPPED = ""
        MANUAL = ""
        CALENDAR = ""
        ELAPSED = ""
        BRANCH = ""
        COMMIT = ""

    pipeline: reactive[Pipeline | None] = reactive(None, recompose=True)

    @classmethod
    def pill(
        cls,
        text: str | None,
        icon: str | None,
        fg_color: str = "black",
        bg_color: str = "green",
    ) -> str:
        color = f"{fg_color} on {bg_color}"
        left_side = f"[{bg_color}][/{bg_color}]"
        right_side = f"[{bg_color}][/{bg_color}]"
        icon = f"{icon} " if icon is not None else ""

        if text is None:
            text = ""
            icon = icon[:-1:]

        return f"{left_side}[{color}]{icon}{text}[/{color}]{right_side}"

    def pipeline_pill(self, state: str, no_text: bool = False) -> str:
        state = state.upper()

        return self.pill(
            (self.Text[state].value if no_text is False else None),
            self.Icons[state].value,
            "white",
            self.Colors[state].value,
        )

    def __init__(
        self,
        pipeline: Pipeline,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.pipeline = pipeline

    def compose(self) -> ComposeResult:
        if self.pipeline is None:
            return

        with Vertical():
            with Horizontal():
                with Container(classes="pipeline-line"):
                    yield Label(self.pipeline_pill(self.pipeline.status.upper()))
                    yield Label(
                        f"{self.Icons.ELAPSED.value} {self.pipeline.created_at}"
                    )
                    yield Label(
                        f"{self.Icons.CALENDAR.value} {self.pipeline.updated_at}"
                    )

                with Container(classes="pipeline-line"):
                    yield Label("Update .gitlab-ci.yml file")

                    sections = [
                        f"[blue]#{self.pipeline.id}[/blue]",
                        self.pill(
                            self.pipeline.ref,
                            self.Icons.BRANCH.value,
                            self.Colors.TEXT.value,
                            self.Colors.GENERIC.value,
                        ),
                        self.pill(
                            self.pipeline.sha[:8:],
                            self.Icons.COMMIT.value,
                            self.Colors.TEXT.value,
                            self.Colors.GENERIC.value,
                        ),
                    ]
                    yield Label("  ".join(sections))

                    if self.pipeline.is_latest:
                        yield Label(
                            self.pill(
                                "latest", None, "white", self.Colors.SUCCESS.value
                            )
                        )

                with Container(classes="pipeline-line"):
                    ...

                with Container(classes="pipeline-line"):
                    with Center():
                        with Horizontal():
                            yield Label(
                                self.pipeline_pill(self.pipeline.status, no_text=True)
                            )
                            yield Label("[bold]-[/bold]")
                            yield Label(
                                self.pipeline_pill(self.pipeline.status, no_text=True)
                            )

            yield Rule()


class PipelineList(Widget):
    pipelines: reactive[list[Pipeline]] = reactive([], recompose=True)

    def __init__(
        self,
        pipelines: list[Pipeline],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.pipelines = pipelines

    def update_pipeline_list(self, new_pipelines: list[Pipeline]) -> None:
        self.pipelines = new_pipelines

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for p in self.pipelines:
                yield PipelineListItem(p)


class PipelineManager(App):
    pipelines: reactive[list[Pipeline]] = reactive([])

    def _wrap_pipelines(self, pipelines: Pipelines) -> list[Pipeline]:
        self.log.info("Wrapping pipelines")
        wrapped_pipelines = []
        is_first = True

        for p in pipelines:
            self.log.info(f"Transforming raw pipeline to internal pipeline")
            self.log.info(p.asdict())

            self.log.info("->")

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
            self.log.info(new_pipeline)

            wrapped_pipelines.append(new_pipeline)

            is_first = False

        return wrapped_pipelines

    def on_mount(self) -> None:
        project = get_current_project()
        self.pipelines = self._wrap_pipelines(get_pipelines(project))

        self.query_one(PipelineList).update_pipeline_list(self.pipelines)

    def compose(self) -> ComposeResult:
        yield PipelineList(self.pipelines)
