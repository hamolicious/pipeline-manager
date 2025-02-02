from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget

from pipeline_manager.components.pipeline_list_item import PipelineListItem

from ..data import Pipeline


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
