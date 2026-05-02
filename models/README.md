## 🚀 Model Deployment

If you are setting up Nicla Vision with OpenMV IDE for the first time, please follow this guide first:  
[Getting Started with Nicla Vision and OpenMV IDE (Arduino Docs)](https://docs.arduino.cc/tutorials/nicla-vision/getting-started/)  

You may also find this step-by-step lab very helpful (covers Arduino IDE, OpenMV firmware, and Edge Impulse integration):  
[MLSysBook Lab – Nicla Vision Setup with OpenMV & Edge Impulse](https://www.mlsysbook.ai/contents/labs/arduino/nicla_vision/setup/setup.html)

### Steps to Run

1. **Update Wi-Fi credentials**  
   Open `main.py` and set your Wi-Fi details:
   - `SSID` = your Wi-Fi network name  
   - `KEY` = your Wi-Fi password  

2. **Copy model file and MicroPython script to Nicla Vision**  
   Connect the Arduino Nicla Vision over USB and copy the following files to its storage:
   - `main.py`  
   - `trained.tflite`  
   - `labels.txt`  


 View real-time detections on terminal  
