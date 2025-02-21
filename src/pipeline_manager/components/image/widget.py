import os
import random
import time
from typing import Any

import numpy as np
import requests
from PIL import Image as PillowImage
from textual import work
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label


class Image(Widget):
    DEFAULT_CSS = """
        Image {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }

        Container {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }
    """

    @staticmethod
    def rgba_to_hex(rgba: tuple[int, int, int, int]) -> str:
        return "#{:02X}{:02X}{:02X}".format(*rgba[:3:])

    canvas = reactive("", recompose=True, repaint=True)

    def __init__(
        self,
        src: str,
        init_width: int,
        init_height: int,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        self.src = src
        self.raw_data: np.ndarray[Any, np.dtype[Any]] = np.ndarray(1)

        self.init_width = init_width
        self.init_height = init_height
        self.canvas = self.random_canvas()

        self.render_image()

    def is_remote(self) -> bool:
        return any(
            [
                self.src.startswith("http"),
            ]
        )

    def _make_pixel(self, top_color: str, bottom_color: str) -> str:
        pixel = "▀"
        return f"[{top_color} on {bottom_color}]{pixel}[/{top_color} on {bottom_color}]"

    async def load_image(self) -> bytes:
        with requests.get(self.src) as r:
            return r.content

    def random_canvas(self) -> str:
        return "\n".join(
            [
                "".join(
                    [
                        self._make_pixel(
                            random.choice(["red", "green", "blue"]),
                            random.choice(["red", "green", "blue"]),
                        )
                        for _ in range(self.init_width)
                    ]
                )
                for _ in range(self.init_height)
            ]
        )

    async def build_canvas(self) -> str:
        canvas = ""

        self.log.debug(self.raw_data)
        for i in range(len(self.raw_data) - 1):
            for j in range(len(self.raw_data[0])):
                top_col = self.rgba_to_hex(self.raw_data[i][j])
                bot_col = self.rgba_to_hex(self.raw_data[i + 1][j])

                pix = self._make_pixel(top_col, bot_col)
                canvas += pix
            canvas += "\n"

        return canvas

    @work(thread=True)
    async def render_image(self) -> None:
        path = "temp-adf8ad7fya807fta08dfga0dgfa"
        temp_file: Any = open(path, "wb")

        try:
            data = await self.load_image()
            temp_file.write(data)

            temp_file.close()
            temp_file = open(path, "rb")

            image = PillowImage.open(temp_file)
            self.raw_data = np.asarray(
                image.resize((self.init_width, self.init_height))
            )

            self.canvas = await self.build_canvas()

            os.remove(path)

        except Exception as e:
            self.log.error(e)

        finally:
            temp_file.close()

    def compose(self) -> ComposeResult:
        with Container():
            yield Label(self.canvas)
