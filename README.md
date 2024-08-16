# Camera_system_monitering_using_RTSP

To test and validate the camera system's capabilities in real-time video streaming, with timestamping, and motion detection which are crucial for security and monitoring purposes.

- **Real-Time Video Streaming Setup:**

  - Setting up a mock RTSP (Real Time Streaming Protocol) video link to simulate a live camera feed from the installed system.
  - Develop a Python script using OpenCV to connect to and stream video from this RTSP link.

- **Timestamp Implementation:**

  - For each frame in the video stream, added a timestamp in the bottom right corner. The timestamp have black text on a yellow background, resembling a typical surveillance camera output.
  - Ensure that the timestamp is accurate and updates in real time.

- **Motion Detection:**

  - Implemented a motion detection algorithm within the video stream. The algorithm should identify and flag any significant movement within the camera's field of view.
  - When motion is detected, save the corresponding frame as a JPEG image in a designated folder, named with its timestamp, to simulate incident capture and loggingImage
  
- **Saving and Logging:**

  - Along with motion-triggered saves, regularly save frames (e.g., one frame per minute) as part of routine surveillance logging.
