import random

import arrow
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from ..components.pills import Icons, build_pipeline_pill
from ..data import Pipeline


class PipelineAuthor(Widget):
    DEFAULT_CSS = """
        PipelineAuthor {
            width: 100%;
            height: 7;
            padding: 0;
            margin: 0;
        }
    """

    canvas = reactive("", recompose=True, repaint=True)

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        self.canvas = ""
        self.canvas_width = 6
        self.canvas_height = 6

        self.update()

    def _make_pixel(self, top_color: str, bottom_color: str) -> str:
        pixel = "▀"
        return f"[{top_color} on {bottom_color}]{pixel}[/{top_color} on {bottom_color}]"

    def update(self):
        self.canvas = ""
        for _ in range(int(self.canvas_height / 2)):
            for _ in range(self.canvas_width):
                self.canvas += self._make_pixel(
                    random.choice(["red", "blue", "green"]),
                    random.choice(["red", "blue", "green"]),
                )

            self.canvas += "\n"

    def compose(self) -> ComposeResult:
        yield Label(self.canvas)
