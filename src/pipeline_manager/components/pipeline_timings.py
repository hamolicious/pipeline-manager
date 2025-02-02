import arrow
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from ..components.pills import Icons, build_pipeline_pill
from ..data import Pipeline


class PipelineTimings(Widget):
    DEFAULT_CSS = """
        PipelineTimings {
            width: 100%;
            height: 7;
        }
    """

    status = reactive("Created", recompose=True, repaint=True)
    updated_at = reactive("2025-01-01T00:00:00.000+00:00", recompose=True, repaint=True)
    created_at = reactive("2025-01-01T00:00:00.000+00:00", recompose=True, repaint=True)

    def __init__(
        self,
        pipeline: Pipeline,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        self.status = pipeline.status
        self.updated_at = pipeline.updated_at
        self.created_at = pipeline.created_at

    def update_pipeline(self, pipeline: Pipeline):
        self.status = pipeline.status
        self.updated_at = pipeline.updated_at
        self.created_at = pipeline.created_at

    def compose(self) -> ComposeResult:
        elapsed = str(arrow.get(self.updated_at) - arrow.get(self.created_at)).split(
            "."
        )[0]

        yield Label(build_pipeline_pill(self.status.upper()))
        yield Label(f"{Icons.ELAPSED.value} {elapsed}")

        date = arrow.get(self.updated_at)
        display_date = arrow.Arrow.humanize(date)
        yield Label(f"{Icons.CALENDAR.value} {display_date}")
