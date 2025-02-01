from dataclasses import dataclass
from typing import List, TypeAlias

from gitlab.base import RESTObject, RESTObjectList
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from .gitlab_api import get_current_project, get_pipelines


@dataclass
class Pipeline:
    id: str
    status: str


Pipelines: TypeAlias = RESTObjectList | List[RESTObject]


class PipelineListItem(Widget):
    pipeline: reactive[RESTObject | None] = reactive(None, recompose=True)

    def __init__(
        self,
        pipeline: RESTObject,
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

        self.log.info(self.pipeline.asdict())
        yield Label(str(self.pipeline.id))


class PipelineList(Widget):
    pipelines: reactive[Pipelines] = reactive([], recompose=True)

    def __init__(
        self,
        pipelines: RESTObjectList | list[RESTObject],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.pipelines = pipelines

    def update_pipeline_list(self, new_pipelines: Pipelines) -> None:
        self.pipelines = new_pipelines

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for p in self.pipelines:
                yield PipelineListItem(p)


class PipelineManager(App):
    pipelines: reactive[Pipelines] = reactive([])

    def on_mount(self) -> None:
        project = get_current_project()
        self.pipelines = get_pipelines(project)

        self.query_one(PipelineList).update_pipeline_list(self.pipelines)

        self.log.info("Pipelines:", list(map(lambda p: p.asdict(), self.pipelines)))

    def compose(self) -> ComposeResult:
        yield PipelineList(self.pipelines)
