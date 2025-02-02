from textual.app import ComposeResult
from textual.containers import Center, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from ..components.pills import build_pipeline_pill
from ..data import Job


class PipelineJobsPreview(Widget):
    DEFAULT_CSS = """
        PipelineTimings {
            width: 100%;
            height: 7;
        }
    """

    jobs = reactive[list[Job]]([], recompose=True, repaint=True)

    def __init__(
        self,
        jobs: list[Job],
        pipeline_id: int,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.update_jobs(jobs, pipeline_id)

    def update_jobs(self, jobs: list[Job], pipeline_id: int):
        self.log.info(jobs)
        self.jobs = list(filter(lambda j: j, jobs))
        self.pipeline_id = pipeline_id

    def compose(self) -> ComposeResult:
        # TODO: convert to stages
        with Center():
            with Horizontal():
                for job in self.jobs:
                    yield Label(build_pipeline_pill(job.status, no_text=True))

                    if self.jobs.index(job) == len(self.jobs) - 1:
                        break

                    yield Label("[bold]-[/bold]")
