import os
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class MemeGenerator:
    def create_fresco(self, message: str) -> Image.Image:
        img = Image.open("./assets/images/fresco.jpg")
        font = ImageFont.truetype("./assets/fonts/timesnewromanpsmt.ttf", 20)

        draw = ImageDraw.Draw(img)

        lines = textwrap.wrap(message, width=30)
        text = "\n".join(lines)

        draw.multiline_text(
            (165, 150),
            text,
            fill="black",
            font=font,
            spacing=4,
            anchor="md",
            align="center",
        )

        return img

    def create_demotivator(self, message: str, image_path: str) -> Image.Image:
        font = ImageFont.truetype("./assets/fonts/timesnewromanpsmt.ttf", 120)

        img = Image.open(image_path)
        img = img.resize((1576, 1479))

        template = Image.open("./assets/images/demotivator.jpg")
        template.paste(img, (134, 142))

        draw = ImageDraw.Draw(template)

        lines = textwrap.wrap(message, width=30)
        text = "\n".join(lines)

        draw.multiline_text(
            (925, 1800),
            text,
            fill="white",
            font=font,
            spacing=4,
            anchor="ms",
            align="center",
        )

        return template

    def create_meme(self, message1: str, message2: str, image_path: str) -> Image.Image:
        font = ImageFont.truetype("./assets/fonts/impact.ttf", 36)

        img = Image.open(image_path)
        img = img.resize((640, 480), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img)

        lines1 = textwrap.wrap(message1, width=30)
        lines2 = textwrap.wrap(message2, width=30)

        text1 = "\n".join(lines1)
        text2 = "\n".join(lines2)

        draw.multiline_text(
            (img.width / 2, 50),
            text1,
            fill="white",
            font=font,
            spacing=4,
            anchor="ms",
            align="center",
            stroke_width=5,
            stroke_fill="black",
        )

        draw.multiline_text(
            (img.width / 2, img.height - 20),
            text2,
            fill="white",
            font=font,
            spacing=4,
            anchor="md",
            align="center",
            stroke_width=5,
            stroke_fill="black",
        )

        return img

    def get_random_image_path(self, guild_id: str) -> str:
        images_dir = f"./data/{guild_id}/images"

        image_dir = Path(images_dir)
        image_dir.mkdir(parents=True, exist_ok=True)

        images = os.listdir(images_dir)
        return f"{images_dir}/{random.choice(images)}"

    def get_images_count(self, guild_id: str) -> int:
        images_dir = Path(f"data/{guild_id}/images")
        images_dir.mkdir(parents=True, exist_ok=True)

        return len(os.listdir(images_dir))
