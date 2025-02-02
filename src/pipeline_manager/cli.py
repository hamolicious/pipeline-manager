import time
from typing import List, TypeAlias

from gitlab.base import RESTObject, RESTObjectList
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Rule

from .components.pills import build_pipeline_pill
from .components.pipeline_info import PipelineInfo
from .components.pipeline_timings import PipelineTimings
from .data import Pipeline
from .gitlab_api import get_current_project, get_pipelines
from .mappers import raw_commit_to_commit, raw_pipeline_to_pipeline

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
    pipeline: reactive[Pipeline | None] = reactive(None, recompose=True)

    def __init__(
        self,
        pipeline: Pipeline,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        project = get_current_project()
        self.pipeline = pipeline
        self.commit = raw_commit_to_commit(project.commits.get(self.pipeline.sha))
        self.jobs = project.jobs.list(get_all=False)

    def compose(self) -> ComposeResult:
        if self.pipeline is None:
            return

        with Vertical():
            with Horizontal():
                with Container(classes="pipeline-line"):
                    yield PipelineTimings(self.pipeline)

                with Container(classes="pipeline-line"):
                    yield PipelineInfo(self.pipeline, self.commit)

                with Container(classes="pipeline-line"):
                    ...

                with Container(classes="pipeline-line"):
                    with Center():
                        with Horizontal():
                            yield Label(
                                build_pipeline_pill(self.pipeline.status, no_text=True)
                            )
                            yield Label("[bold]-[/bold]")
                            yield Label(
                                build_pipeline_pill(self.pipeline.status, no_text=True)
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
    worker_last_update = 0.0
    REQUEST_INTERVAL_SEC = 3

    @work(exclusive=True, thread=True, name="Pipeline Updatetor")
    def start_pipeline_updator(self) -> None:
        self.log.info(f"Pipeline updator thread started")
        project = get_current_project()

        while True:
            elapsed = time.time() - self.worker_last_update
            self.log.info(f"Elapsed: {elapsed}")

            if elapsed < self.REQUEST_INTERVAL_SEC:
                time.sleep(0.5)
                continue

            self.log.info("Updating!")
            self.pipelines = raw_pipeline_to_pipeline(get_pipelines(project))

            self.query_one(PipelineList).update_pipeline_list(self.pipelines)
            self.worker_last_update = time.time()

    def on_mount(self) -> None:
        self.start_pipeline_updator()

    def compose(self) -> ComposeResult:
        yield PipelineList(self.pipelines)
