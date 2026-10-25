import asyncio
import base64
import logging
from pathlib import Path

from _chrome import get_ws_url

from cdpify import Client
from cdpify.domains.page.events import ScreencastFrameEvent

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def save_frame(frame_data: str, frame_number: int, output_dir: Path) -> None:
    image_bytes = base64.b64decode(frame_data)
    output_path = output_dir / f"frame_{frame_number:04d}.jpg"
    output_path.write_bytes(image_bytes)
    print(f"✓ Saved frame {frame_number}")


async def main():
    output_dir = Path("screencast_frames")
    output_dir.mkdir(exist_ok=True)

    ws_url = get_ws_url(start_url="https://example.com")
    print(f"Connecting to: {ws_url}\n")

    async with Client(ws_url) as client:
        await client.page.enable()

        print("🎬 Starting screencast...")
        await client.page.start_screencast(
            format="jpeg",
            quality=80,
            max_width=1280,
            max_height=720,
            every_nth_frame=1,
        )

        print("🎥 Recording screencast... Press Ctrl+C to stop\n")

        frame_count = 0
        try:
            async for event in client.listen(ScreencastFrameEvent):
                frame_count += 1
                print(f"🎬 Frame {frame_count} received!")

                await client.page.screencast_frame_ack(session_id=event.session_id)

                await save_frame(event.data, frame_count, output_dir)
        except asyncio.CancelledError:
            # Ctrl+C cancels the main task; KeyboardInterrupt only reaches
            # the caller of asyncio.run().
            print("\n⏹️  Stopping...")
            raise
        finally:
            print("🛑 Stopping screencast...")
            await client.page.stop_screencast()
            print(f"📹 Recorded {frame_count} frames to {output_dir.absolute()}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Done!")
