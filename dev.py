from src.pipeline_manager.cli import PipelineManager


def main() -> None:
    app = PipelineManager()
    app.run()


if __name__ == "__main__":
    main()
