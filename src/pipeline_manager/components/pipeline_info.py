from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from ..components.pills import Colors, Icons, build_pill
from ..data import Commit, Pipeline


class PipelineInfo(Widget):
    DEFAULT_CSS = """
        PipelineInfo {
            width: 100%;
            height: 7;
        }
    """

    title = reactive("", recompose=True, repaint=True)
    pipeline_id = reactive(0, recompose=True, repaint=True)
    branch = reactive("", recompose=True, repaint=True)
    short_sha = reactive("", recompose=True, repaint=True)
    author = reactive("", recompose=True, repaint=True)
    is_latest = reactive(False, recompose=True, repaint=True)

    def __init__(
        self,
        pipeline: Pipeline,
        commit: Commit,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.update_pipeline(pipeline, commit)

    def update_pipeline(self, pipeline: Pipeline, commit: Commit):
        self.title = commit.title
        self.pipeline_id = pipeline.id
        self.branch = pipeline.ref
        self.short_sha = pipeline.sha[:8:]
        self.author = commit.author_name
        self.is_latest = pipeline.is_latest

    def compose(self) -> ComposeResult:
        yield Label(self.title)

        sections = [
            f"[blue]#{self.pipeline_id}[/blue]",
            build_pill(
                self.branch,
                icon=Icons.BRANCH.value,
                text_color=Colors.TEXT.value,
                pill_color=Colors.GENERIC.value,
            ),
            build_pill(
                self.short_sha,
                icon=Icons.COMMIT.value,
                text_color=Colors.TEXT.value,
                pill_color=Colors.GENERIC.value,
            ),
            build_pill(
                self.author,
                icon=Icons.USER.value,
                text_color=Colors.TEXT.value,
                pill_color=Colors.GENERIC.value,
            ),
        ]
        yield Label("  ".join(sections))

        if self.is_latest:
            yield Label(
                build_pill(
                    "latest",
                    icon=None,
                    text_color="white",
                    pill_color=Colors.SUCCESS.value,
                )
            )
