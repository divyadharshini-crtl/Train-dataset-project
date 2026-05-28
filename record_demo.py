import sys
import time
import os

def check_dependencies():
    missing = []
    try:
        import cv2
    except ImportError:
        missing.append("opencv-python")
    try:
        import pyautogui
    except ImportError:
        missing.append("pyautogui")
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
        
    return missing

def run_recorder():
    missing = check_dependencies()
    if missing:
        print("=" * 65)
        print("   SYSSLAN PRESENTATION RECORDER - SETUP REQUIREMENT   ")
        print("=" * 65)
        print("To record your screen using this helper, please install these packages first:")
        print(f"  pip install {' '.join(missing)}")
        print("\nAlternatively, you can use Windows built-in Game Bar recorder:")
        print("  1. Press 'Win + G' on your keyboard.")
        print("  2. Click the 'Capture' (circle) button to start recording your screen.")
        print("  3. Press 'Win + Alt + R' to start/stop recording directly!")
        print("=" * 65)
        return
        
    import cv2
    import pyautogui
    import numpy as np

    # Get primary screen size
    screen_width, screen_height = pyautogui.size()
    
    # Configure output file name
    output_filename = "internship_presentation.mp4"
    if os.path.exists(output_filename):
        # Prevent overwriting
        output_filename = f"internship_presentation_{int(time.time())}.mp4"
        
    # Standard modern video codec
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 10.0 # 10 frames per second is perfect for presentation slides and code scrolling
    out = cv2.VideoWriter(output_filename, fourcc, fps, (screen_width, screen_height))
    
    print("=" * 60)
    print("      PULSAR SCREEN RECORDER IS NOW READY      ")
    print("=" * 60)
    print(f"-> Output file will be saved as: '{output_filename}'")
    print("-> Recording starts in 5 seconds...")
    print("-> Press Ctrl + C in this terminal window to STOP recording.")
    print("=" * 60)
    
    # Countdown
    for i in range(5, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
        
    print("\n🔴 RECORDING HAS STARTED! (Minimize this window and start your presentation)")
    
    try:
        frame_count = 0
        start_rec_time = time.time()
        while True:
            # Capture screen frame
            img = pyautogui.screenshot()
            # Convert frame to numpy array for OpenCV
            frame = np.array(img)
            # Convert BGR to RGB color space
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Write frame to video file
            out.write(frame)
            frame_count += 1
            
            # Print status every 30 frames (approx 3 seconds)
            if frame_count % 30 == 0:
                elapsed = time.time() - start_rec_time
                print(f"Recording active: {elapsed:.0f} seconds captured ({frame_count} frames)...", end="\r")
                
            # Sleep slightly to maintain target FPS
            time.sleep(1.0 / fps)
            
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C stopping
        print("\n\n⏹️ Stopping screen recording...")
    finally:
        # Save and release video structures
        out.release()
        cv2.destroyAllWindows()
        print("=" * 60)
        print("🔴 RECORDING COMPLETED SUCCESSFULLY!")
        print(f"-> Video compiled and saved to: '{os.path.abspath(output_filename)}'")
        print("=" * 60)

if __name__ == "__main__":
    run_recorder()
