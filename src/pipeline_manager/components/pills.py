from enum import Enum


class Text(Enum):
    CREATED = "Created"
    PENDING = "Pending"
    RUNNING = "Running"
    SUCCESS = "Passed"
    WARNING = "Warning"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    MANUAL = "Manual"


class Colors(Enum):
    CREATED = "#333238"
    PENDING = "#6F3A0C"
    RUNNING = "#154584"
    SUCCESS = "#0C522C"
    WARNING = "#6F3A0C"
    FAILED = "#8C1E0D"
    SKIPPED = "#333238"
    MANUAL = "#333238"
    GENERIC = "#323232"
    TEXT = "#AAAAAA"


class Icons(Enum):
    CREATED = ""
    PENDING = ""
    RUNNING = ""
    SUCCESS = ""
    WARNING = ""
    FAILED = ""
    SKIPPED = ""
    MANUAL = ""
    CALENDAR = ""
    ELAPSED = ""
    BRANCH = ""
    COMMIT = ""
    USER = ""


def build_pill(
    text: str | None,
    *,
    icon: str | None,
    text_color: str = Colors.GENERIC.value,
    pill_color: str = Colors.TEXT.value,
) -> str:
    color = f"{text_color} on {pill_color}"
    left_side = f"[{pill_color}][/{pill_color}]"
    right_side = f"[{pill_color}][/{pill_color}]"
    icon = f"{icon} " if icon is not None else ""

    if text is None:
        text = ""
        icon = icon[:-1:]

    return f"{left_side}[{color}]{icon}{text}[/{color}]{right_side}"


def build_pipeline_pill(state: str, no_text: bool = False) -> str:
    state = state.upper()

    return build_pill(
        (Text[state].value if no_text is False else None),
        icon=Icons[state].value,
        text_color="white",
        pill_color=Colors[state].value,
    )
