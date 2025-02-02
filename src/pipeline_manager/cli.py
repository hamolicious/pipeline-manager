import time
from typing import List, TypeAlias

from gitlab.base import RESTObject, RESTObjectList
from textual import work
from textual.app import App, ComposeResult
from textual.reactive import reactive

from .components.pipeline_list import PipelineList
from .data import Pipeline
from .gitlab_api import get_current_project, get_pipelines
from .mappers import raw_pipeline_to_pipeline

Pipelines: TypeAlias = RESTObjectList | List[RESTObject]


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
