import os
import random
import textwrap
from pathlib import Path

import ffmpeg

FONT_IMPACT = "assets/fonts/impact.ttf"


class AnimationGenerator:
    def create_animated_meme(
        self, message1: str, message2: str, animation: str, output_path: str
    ) -> None:
        lines1 = "\n".join(textwrap.wrap(message1, width=30))
        lines2 = "\n".join(textwrap.wrap(message2, width=30))

        probe = ffmpeg.probe(animation)
        has_audio = any(
            stream.get("codec_type") == "audio" for stream in probe.get("streams", [])
        )

        in_stream = ffmpeg.input(animation)
        video = in_stream.video

        # Apply scaling
        video = ffmpeg.filter(video, "scale", 640, 480, flags="lanczos")

        # Apply Top Text
        video = ffmpeg.filter(
            video,
            "drawtext",
            text=lines1,
            fontfile=FONT_IMPACT,
            fontsize=40,
            fontcolor="white",
            bordercolor="black",
            borderw=5,
            x="(w-text_w)/2",
            y="40",
            line_spacing=4,
            text_align="M",
        )

        # Apply Bottom Text
        video = ffmpeg.filter(
            video,
            "drawtext",
            text=lines2,
            fontfile=FONT_IMPACT,
            fontsize=40,
            fontcolor="white",
            bordercolor="black",
            borderw=5,
            x="(w-text_w)/2",
            y="h-text_h-40",
            line_spacing=4,
            text_align="M",
        )

        if has_audio:
            audio = in_stream.audio
            out = ffmpeg.output(
                video, audio, output_path, vcodec="libx264", acodec="aac"
            )
        else:
            out = ffmpeg.output(video, output_path, vcodec="libx264")

        out.run(overwrite_output=True)

    def get_random_animation(self, guild_id: str) -> str:
        gifs_dir = f"./data/{guild_id}/gifs"

        gif_dir = Path(gifs_dir)
        gif_dir.mkdir(parents=True, exist_ok=True)

        images = os.listdir(gifs_dir)
        return f"{gifs_dir}/{random.choice(images)}"

    def get_animations_count(self, guild_id: str) -> int:
        gifs_dir = Path(f"data/{guild_id}/gifs")
        gifs_dir.mkdir(parents=True, exist_ok=True)

        return len(os.listdir(gifs_dir))
