from pathlib import Path
import cv2

VIDEO_PATH = Path("videos/match01.mp4")
OUTPUT_DIR = Path("datasets/match01_frames")
INTERVAL_SECONDS = 2
MAX_DURATION_SECONDS = 5 * 60

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise FileNotFoundError(f"Could not open video: {VIDEO_PATH}")

print(f"Opened video: {VIDEO_PATH.resolve()}", flush=True)

fps = cap.get(cv2.CAP_PROP_FPS)

if fps <= 0:
    cap.release()
    raise ValueError("Could not read the video's frame rate.")

print(f"FPS: {fps:.2f}")


interval_frames = round(fps * INTERVAL_SECONDS)
max_frames = int(fps * MAX_DURATION_SECONDS)
start_frame = int(10 * fps)

frame_index = 0
saved_count = 0

"""""
print("Starting frame read...", flush=True)

success, frame = cap.read()

print(f"Read successful: {success}", flush=True)

if success:
    print(f"Frame shape: {frame.shape}", flush=True)
else:
    print("Could not read the first frame.", flush=True)

cap.release()
"""
while frame_index < max_frames:
    success, frame = cap.read()

    if not success:
        break

    print(frame_index)
    if frame_index >= start_frame:
        if frame_index % interval_frames == 0:
            timestamp_ms = round(frame_index / fps * 1000)
            filename = (
                f"frame_{saved_count:05d}_"
                f"{timestamp_ms:010d}ms.jpg"
            )

            cv2.imwrite(
                str(OUTPUT_DIR / filename),
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 95],
            )
            saved_count += 1

    frame_index += 1

cap.release()

print(f"Saved {saved_count} frames to {OUTPUT_DIR}")
