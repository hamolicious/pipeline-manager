# pipeline-manager

View and cotroll pipelines within the CLI! For fun: made to look the same as Gitlab's web-ui!

![pipeline list screenshot](./screenshots/pipeline-list.png)

## Installation

````bash
pipx install pipeline-manager --index-url https://__token__:$GITLAB_TOKEN@gitlab.slayhouse.net/api/v4/projects/76/packages/pypi/simple```
````

## Usage

```bash
launch-project folder1/ folder2/
```

This creates 3 sessions in running in the background!

```bash
> launch-project common-lib event-generator event-consumer
Launching prject common-lib
Launching prject event-generator
Launching prject event-consumer

>
```
