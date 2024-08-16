import cv2
import time
import os


def detect_motion_and_save(rtsp_url, output_dir):
    """Detects motion and saves frames with timestamps, also saves one frame per minute."""

    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print(f"Error: Unable to open RTSP stream '{rtsp_url}'")
        return

    fgbg = cv2.createBackgroundSubtractorMOG2()
    motion_detected = False
    last_minute_saved = -1  # Track the last minute a frame was saved

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to read frame. Stream might have ended.")
            break

        fgmask = fgbg.apply(frame)
        thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                motion_detected = True
                break

        # Motion-triggered saving
        if motion_detected:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            # Add timestamp (with background and custom positioning)
            (text_width, text_height), _ = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            text_x = frame.shape[1] - text_width - 10  # Adjust for padding
            text_y = frame.shape[0] - 10

            # Draw yellow background rectangle
            cv2.rectangle(frame, (text_x - 5, text_y - text_height - 5), (frame.shape[1] - 5, frame.shape[0] - 5), (0, 255, 255), -1)  # Filled

            # Add timestamp text
            cv2.putText(frame, timestamp, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
            filename = f"{output_dir}/motion_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Motion detected! Saved frame as '{filename}'")
            motion_detected = False

        # Per-minute saving
        current_minute = int(time.time() / 60)  # Get current minute since epoch
        if current_minute != last_minute_saved:
            timestamp = time.strftime("%Y-%m-%d_%H-%M-00")  # Force seconds to 00
            filename = f"{output_dir}/minute_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved minute frame as '{filename}'")
            last_minute_saved = current_minute

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()

if __name__ == "__main__":
    rtsp_url = "rtsp://localhost:8554/qn4"
    output_dir = "captured_frames"
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if not exists
    detect_motion_and_save(rtsp_url, output_dir)