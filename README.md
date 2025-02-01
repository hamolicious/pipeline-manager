# launch_project

Launch tmux sessions and automatically rename the session and start vim.

## Installation

````bash
pipx install tmux-launch-project --index-url https://__token__:$GITLAB_TOKEN@gitlab.slayhouse.net/api/v4/projects/75/packages/pypi/simple```
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
