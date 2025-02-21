import time
from typing import List, TypeAlias

from gitlab.base import RESTObject, RESTObjectList
from gitlab.v4.objects import pipelines
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Rule

from ..components.pipeline_author import PipelineAuthor
from ..components.pipeline_info import PipelineInfo
from ..components.pipeline_jobs_preview import PipelineJobsPreview
from ..components.pipeline_timings import PipelineTimings
from ..data import Commit, Job, Pipeline
from ..gitlab_api import get_current_project, get_pipelines
from ..mappers import raw_commit_to_commit, raw_jobs_to_jobs, raw_pipeline_to_pipeline


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
    commit: reactive[Commit | None] = reactive(None, recompose=True)
    jobs: reactive[list[Job] | None] = reactive(None, recompose=True)

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
        self.commit = None
        self.jobs = None

        self.fetch_data()

    @work(exclusive=False, thread=True)
    def fetch_data(self) -> None:
        if self.pipeline is None:
            return

        project = get_current_project()
        self.commit = raw_commit_to_commit(project.commits.get(self.pipeline.sha))
        self.jobs = raw_jobs_to_jobs(
            project.pipelines.get(self.pipeline.id).jobs.list(get_all=False)
        )

    def compose(self) -> ComposeResult:
        if self.pipeline is None or self.commit is None or self.jobs is None:
            yield SkeletonPipelineListItem()
            return

        with Vertical():
            with Horizontal():
                with Container(classes="pipeline-line"):
                    yield PipelineTimings(self.pipeline)

                with Container(classes="pipeline-line"):
                    yield PipelineInfo(self.pipeline, self.commit)

                with Container(classes="pipeline-line"):
                    self.log.debug(self.pipeline, self.commit)
                    yield PipelineAuthor(self.commit)

                with Container(classes="pipeline-line"):
                    yield PipelineJobsPreview(self.jobs)

            yield Rule()


class SkeletonPipelineListItem(Widget):
    def generate_label(self, length: int = 15) -> Label:
        return Label("[white on #323232]" + (" " * length) + "[/white on #323232]")

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                with Container(classes="pipeline-line"):
                    yield self.generate_label()

                with Container(classes="pipeline-line"):
                    yield self.generate_label()

                with Container(classes="pipeline-line"):
                    yield self.generate_label()

                with Container(classes="pipeline-line"):
                    yield self.generate_label()

            yield Rule()
