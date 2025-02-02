import time
from typing import List, TypeAlias

from gitlab.base import RESTObject, RESTObjectList
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Rule

from .components.pills import Colors, Icons, build_pill, build_pipeline_pill
from .components.pipeline_timings import PipelineTimings
from .data import Pipeline
from .gitlab_api import get_current_project, get_pipelines

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
        self.commit = project.commits.get(self.pipeline.sha)
        self.jobs = project.jobs.list(get_all=False)

    def compose(self) -> ComposeResult:
        if self.pipeline is None:
            return

        with Vertical():
            with Horizontal():
                with Container(classes="pipeline-line"):
                    yield PipelineTimings(self.pipeline)

                with Container(classes="pipeline-line"):
                    yield Label(self.commit.title)

                    sections = [
                        f"[blue]#{self.pipeline.id}[/blue]",
                        build_pill(
                            self.pipeline.ref,
                            icon=Icons.BRANCH.value,
                            text_color=Colors.TEXT.value,
                            pill_color=Colors.GENERIC.value,
                        ),
                        build_pill(
                            self.pipeline.sha[:8:],
                            icon=Icons.COMMIT.value,
                            text_color=Colors.TEXT.value,
                            pill_color=Colors.GENERIC.value,
                        ),
                        build_pill(
                            self.commit.author_name,
                            icon=Icons.USER.value,
                            text_color=Colors.TEXT.value,
                            pill_color=Colors.GENERIC.value,
                        ),
                    ]
                    yield Label("  ".join(sections))

                    if self.pipeline.is_latest:
                        yield Label(
                            build_pill(
                                "latest",
                                icon=None,
                                text_color="white",
                                pill_color=Colors.SUCCESS.value,
                            )
                        )

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

    def _wrap_pipelines(self, pipelines: Pipelines) -> list[Pipeline]:
        self.log.info("Wrapping pipelines")
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

    @work(exclusive=True, thread=True, name="Pipeline Updatetor")
    def start_pipeline_updator(self) -> None:
        self.log.info(f"Pipeline updator thread started")

        project = get_current_project()
        self.pipelines = self._wrap_pipelines(get_pipelines(project))

        self.query_one(PipelineList).update_pipeline_list(self.pipelines)
        self.worker_last_update = time.time()

        while True:
            elapsed = time.time() - self.worker_last_update
            self.log.info(f"Elapsed: {elapsed}")

            if elapsed < self.REQUEST_INTERVAL_SEC:
                time.sleep(0.5)
                continue

            self.log.info("Updating!")
            self.pipelines = self._wrap_pipelines(get_pipelines(project))

            self.query_one(PipelineList).update_pipeline_list(self.pipelines)
            self.worker_last_update = time.time()

    def on_mount(self) -> None:
        self.start_pipeline_updator()

    def compose(self) -> ComposeResult:
        yield PipelineList(self.pipelines)
