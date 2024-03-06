import cv2 as cv
import numpy as np
from datetime import datetime

class VideoRecorder:
    def __init__(self, camera_source):
        self.camera_source = camera_source
        self.capture = cv.VideoCapture(camera_source)
        self.recording = False
        self.recorded_video = None
        self.frame_width = int(self.capture.get(cv.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.brightness = 0  # 명도
        self.contrast = 1.0  # 대비

    def start_recording(self, filename, fps=30):
        self.recorded_video = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*'XVID'), fps, (self.frame_width, self.frame_height))

    def stop_recording(self):
        if self.recorded_video is not None:
            self.recorded_video.release()
            self.recorded_video = None

    def mode(self):
        if self.recording:
            self.stop_recording()
            self.recording = False
        else:
            now = datetime.now()
            self.start_recording(f"REC_{now.strftime('%y%m%d_%H%M%S')}.avi")
            self.recording = True

    def brightness_change(self, value):
        self.brightness += value
    
    def contras_change(self, value):
        self.contrast += value

    def run(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                print("Error reading frame")
                break
            
            img_tran = self.contrast * frame + self.brightness
            img_tran = np.clip(img_tran, 0, 255).astype(np.uint8)

            if self.recording:
                self.recorded_video.write(img_tran)
                cv.circle(img_tran, (50, 40), 15, (0, 0, 255), -1)
                cv.putText(img_tran, "REC", (70, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)

            cv.putText(img_tran, "Space: REC Start/Stop", (30, self.frame_height-150), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, "q: Reset", (30, self.frame_height-130), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, "w: Brightness -", (30, self.frame_height-110), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, "e: Brightness +", (30, self.frame_height-90), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, "r: Contras -", (30, self.frame_height-70), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, "t: Contras +", (30, self.frame_height-50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, "ESC: Exit", (30, self.frame_height-30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, f"Brightness: {self.brightness}", (self.frame_width-180, self.frame_height-55), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv.LINE_AA)
            cv.putText(img_tran, f"Contrast: {self.contrast:.1f}", (self.frame_width-180, self.frame_height-30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv.LINE_AA)
            
            cv.imshow('Video Recorder', img_tran)

            key = cv.waitKey(1)
            if key == ord(' '):  # Space key
                self.mode()
            elif key == ord('q'):  # q key 초기화
                self.brightness = 0
                self.contrast = 1.0
            elif key == ord('w'):  # w key 명도 감소
                self.brightness_change(-1)
            elif key == ord('e'):  # e key 명도 증가
                self.brightness_change(1)
            elif key == ord('r'):  # a key 대비 감소
                self.contras_change(-0.1)
            elif key == ord('t'):  # s key 대비 증가
                self.contras_change(0.1)
            elif key == 27 or cv.getWindowProperty('Video Recorder', cv.WND_PROP_VISIBLE) < 1:  # ESC key or window closed
                break

        self.capture.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    camera_source = "rtsp://210.99.70.120:1935/live/cctv001.stream"
    video_recorder = VideoRecorder(camera_source)
    video_recorder.run()
