import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#model_path = '/absolute/path/to/pose_landmarker.task'
model_path='/home/charles/Desktop/HW/mediapipe/mediapipe/tasks/python/vision/'


import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a pose landmarker instance with the live stream mode:
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('pose landmarker result: {}'.format(result))

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with PoseLandmarker.create_from_options(options) as landmarker:
  # The landmarker is initialized. Use it here.
  # ...
    
    
#import mediapipe as mp

# Use OpenCV’s VideoCapture to start capturing from the webcam.
webcam=Picamera2()
dispW=640
dispH=320
webcam_config = webcam.create_video_configuration({"format": "RGB888", "size" : (dispW,dispH)})
webcam.configure(webcam_config)
webcam.start()
fps=0

# Create a loop to read the latest frame from the camera using VideoCapture#read()

# Convert the frame received from OpenCV to a MediaPipe’s Image object.
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_frame_from_opencv)
    
    
# Send live image data to perform pose landmarking.
# The results are accessible via the `result_callback` provided in
# the `PoseLandmarkerOptions` object.
# The pose landmarker must be created with the live stream mode.
landmarker.detect_async(mp_image, frame_timestamp_ms)
    