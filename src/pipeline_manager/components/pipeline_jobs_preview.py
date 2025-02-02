from textual.app import ComposeResult
from textual.containers import Center, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from ..components.pills import StatusHierarchy, build_pipeline_pill
from ..data import Job


class PipelineJobsPreview(Widget):
    DEFAULT_CSS = """
        PipelineJobsPreview {
            width: 100%;
            height: 7;
        }
    """

    jobs = reactive[list[Job]]([], recompose=True, repaint=True)

    def __init__(
        self,
        jobs: list[Job],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.update_jobs(jobs)

    def update_jobs(self, jobs: list[Job]):
        self.jobs = jobs

    def get_all_stages(self) -> list[str]:
        order = []
        for job in self.jobs:
            if job.stage not in order:
                order.append(job.stage)

        return order[::-1]

    def condense_status_by_stage(self) -> dict[str, str]:
        stage_to_state = {}
        for job in self.jobs:
            curr_stage = job.stage

            if job.stage not in stage_to_state:
                stage_to_state[curr_stage] = job.status.upper()
                continue

            last_status = stage_to_state[job.stage]
            curr_status = job.status.upper()

            if StatusHierarchy[curr_status] > StatusHierarchy[last_status]:
                stage_to_state[curr_stage] = curr_status

        return stage_to_state

    def compose(self) -> ComposeResult:
        order = self.get_all_stages()
        stage_to_state = self.condense_status_by_stage()

        with Center():
            with Horizontal():
                for stage in order:
                    state = stage_to_state[stage]

                    yield Label(build_pipeline_pill(state, no_text=True))

                    if order.index(stage) == len(order) - 1:
                        break

                    yield Label("[bold]-[/bold]")
