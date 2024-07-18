import cv2
import os
import numpy as np

def extract_and_stitch_frames(video_path, frames_output_folder, stitched_image_folder, max_frames=25):
    # Ensure output directories exist
    os.makedirs(frames_output_folder, exist_ok=True)
    os.makedirs(stitched_image_folder, exist_ok=True)

    # Initialize video capture
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "Unable to open video file"

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_gap = max(1, total_frames // max_frames)
    frames = []
    saved_frames = 0
    stitched_image_path = os.path.join(stitched_image_folder, 'stitched_image.jpg')

    # Create a stitcher instance
    stitcher = cv2.Stitcher_create()

    try:
        for count in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_gap == 0 and saved_frames < max_frames:
                frame_path = os.path.join(frames_output_folder, f"frame_{saved_frames}.jpg")
                cv2.imwrite(frame_path, frame)
                frames.append(frame)
                saved_frames += 1

            # Stitch when we have collected enough frames or at the end of video
            if saved_frames >= max_frames or count == total_frames - 1:
                if len(frames) > 1:
                    status, stitched = stitcher.stitch(frames)
                    if status == cv2.Stitcher_OK:
                        cv2.imwrite(stitched_image_path, stitched)  # Save or update the stitched image
                        frames = [stitched]  # Start next batch from the stitched result
                        saved_frames = 1  # Reset frame count with the stitched image as the first frame
                    else:
                        # Concatenate the frames horizontally if stitching fails
                        concatenated_image = np.hstack(frames)
                        cv2.imwrite(stitched_image_path, concatenated_image)
                        frames = []  # Clear frames to start fresh
                        saved_frames = 0  # Reset frame count
                else:
                    cv2.imwrite(stitched_image_path, frames[0])  # Save the single frame if that's all we have
                    frames = [frames[0]]  # Continue with the current frame
                    saved_frames = 1

    finally:
        cap.release()

    return stitched_image_path, None
