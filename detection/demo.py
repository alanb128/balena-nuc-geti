# Copyright (C) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

import cv2
import time
from geti_sdk.deployment import Deployment
from geti_sdk.utils import show_image_with_annotation_scene
import os

use_led = True

# Test to see if FT232H is connected
# Need to import in try because BLINKA_FT232H environment variable is set...
try:
    import board
except Exception as e:
    print("No FT232H GPIO found... supressing LED output.")
    use_led = False
else:
    import digitalio
    led = digitalio.DigitalInOut(board.C0)
    led.direction = digitalio.Direction.OUTPUT

video_input = os.getenv('VIDEO_INPUT', 0)
object_detect = os.getenv('OBJECT_DETECT', 'bird')

try:
    lag_time = int(os.getenv('LED_LAG_TIME', '3'))
except Exception as e:
    print("Invalid value for LED_LAG_TIME. Using default 3.")
    lag_time = 3

if __name__ == "__main__":
    # Step 1: Load the deployment
    deployment = Deployment.from_folder("deployment")

    # video_input can be the id of a webcam or an rtsp url like  "rtsp://192.168.1.168/1"
    capture = cv2.VideoCapture(video_input)

    # Step 3: Send inference model(s) to CPU
    deployment.load_inference_models(device="CPU")
    i = 0

    # Set LED to initial state off
    if use_led:
        led.value = False

    # Step 4: Infer
    while capture.isOpened():
        i = i + 1  # Counting 1/10th seconds
        (status,frame) = capture.read()
        if not status:
            print("Capture error...")
            break
        prediction = deployment.infer(image=frame)
        pred_object = prediction.annotations[0].labels[0].name
        print("Prediction: {} ({}%)".format(pred_object, int(prediction.annotations[0].labels[0].probability * 100)))

        # Turn on LED if selected object detected
        if (pred_object == object_detect) and (use_led):
            led.value = True
            i = 0

        # Turn off LED according to LAG_TIME
        if (use_led):
            if (led.value):
                if (i > (lag_time * 10)) and (lag_time != 0):
                    led.value = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.100)  # Tenth of a second

    capture.release()
