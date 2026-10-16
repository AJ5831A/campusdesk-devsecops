import argparse
import json
import tempfile
import textwrap
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas

from build_presentation_video import duration, run


ROOT = Path(__file__).resolve().parents[1]


def card(work, name, title, lines, narration):
    pdf = work / f"{name}.pdf"
    canvas = Canvas(str(pdf), pagesize=(960, 600))
    canvas.setFillColor(HexColor("#171426"))
    canvas.rect(0, 0, 960, 600, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#C0B4FF"))
    canvas.setFont("Helvetica-Bold", 15)
    canvas.drawString(70, 530, "CAMPUSDESK / MACOS VOICE")
    canvas.setFillColor(HexColor("#FFFFFF"))
    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawString(70, 450, title)
    canvas.setFont("Helvetica", 21)
    y = 370
    for line in lines:
        for wrapped in textwrap.wrap(line, 68):
            canvas.drawString(70, y, wrapped)
            y -= 32
        y -= 20
    canvas.save()
    prefix = work / name
    run(["pdftoppm", "-singlefile", "-scale-to", "1440", "-png", str(pdf), str(prefix)])
    spoken = work / f"{name}.txt"
    spoken.write_text(narration)
    audio = work / f"{name}.aiff"
    run(["say", "-v", "Samantha", "-r", "165", "-f", str(spoken), "-o", str(audio)])
    output = work / f"{name}.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-loop",
            "1",
            "-framerate",
            "25",
            "-i",
            str(prefix.with_suffix(".png")),
            "-i",
            str(audio),
            "-af",
            "apad",
            "-t",
            str(duration(audio) + 1.2),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-tune",
            "stillimage",
            "-crf",
            "25",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-ar",
            "44100",
            "-ac",
            "1",
            str(output),
        ]
    )
    return output


def build():
    parser = argparse.ArgumentParser()
    parser.add_argument("runtime", type=Path)
    parser.add_argument("monitoring", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="campusdesk-walkthrough-") as folder:
        work = Path(folder)
        transition = card(
            work,
            "transition",
            "Recorded cloud evidence",
            [
                "The following footage is the actual earlier CI and AWS session.",
                "AWS has since been destroyed. This is historical proof.",
                "Narration uses the MacBook's Samantha voice, not Aryan's voice.",
            ],
            "The following footage preserves the actual earlier Git push, completed pipeline, application and cloud monitoring session. It is recorded evidence. The temporary AWS environment has since been destroyed, so any references to live systems describe that earlier session. All narration uses the MacBook's synthetic Samantha voice, not Aryan's own voice.",
        )
        closing = card(
            work,
            "closing",
            "Final cleanup completed",
            [
                "Terraform destroy: 59 resources removed.",
                "All 11 scoped cleanup checks passed.",
                "KMS deletion scheduled for 15 November 2026.",
                "Shared foundation and AI assistance are credited in the repository.",
            ],
            "After that recorded session, shared Terraform teardown completed successfully with fifty-nine resources destroyed and eleven scoped cleanup checks passed. The owned KMS key remains scheduled for deletion on the fifteenth of November, twenty twenty-six. The recovery apply was interrupted while waiting for the failed old node group; the successful destroy is documented separately. CampusDesk remains available locally. The shared foundation and AI assistance are credited in the repository. Thank you.",
        )
        segments = [
            ROOT / "demo/presentation.mp4",
            transition,
            args.runtime.resolve(),
            args.monitoring.resolve(),
            closing,
        ]
        timing = []
        elapsed = 0.0
        for label, path in zip(
            [
                "Updated ten-slide presentation",
                "Historical evidence disclosure",
                "Actual recorded CI and cloud walkthrough",
                "Actual corrected monitoring evidence",
                "Final cleanup result",
            ],
            segments,
        ):
            seconds = duration(path)
            timing.append(
                {
                    "section": label,
                    "starts_at_seconds": round(elapsed, 3),
                    "seconds": seconds,
                }
            )
            elapsed += seconds
        manifest = work / "concat.txt"
        manifest.write_text("".join(f"file '{path}'\n" for path in segments))
        output = ROOT / "demo/walkthrough.mp4"
        run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(manifest),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(output),
            ]
        )
    metadata = {
        "voice": "macOS Samantha (synthetic)",
        "cloud_status": "Destroyed; runtime footage is historical",
        "seconds": duration(output),
        "sections": timing,
    }
    (ROOT / "demo/walkthrough-video.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    print(json.dumps(metadata))


if __name__ == "__main__":
    build()
