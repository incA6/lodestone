import time
import struct
import numpy as np
import pyaudio

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # Size of audio buffer chunks (approx 23ms)

# Clap detection tuning parameters
VOLUME_THRESHOLD = 8000     # Minimum absolute volume to consider a clap
SUDDENNESS_THRESHOLD = 7.0  # How many times louder a chunk must be than the previous one
COOLDOWN_PERIOD = 0.2       # Seconds to wait before allowing another detection

def detect_claps():
    p = pyaudio.PyAudio()
    
    # Open the microphone stream
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("🎙️  Listening for claps... Press Ctrl+C to stop.")
    
    prev_rms = 1.0  # Avoid division by zero
    last_clap_time = 0

    try:
        while True:
            # Read a chunk of raw data from the microphone
            data = stream.read(CHUNK, exception_on_overflow=False)
            
            # Convert raw bytes into numbers (16-bit integers)
            count = len(data) / 2
            format_str = f"{int(count)}h"
            shorts = struct.unpack(format_str, data)
            audio_array = np.array(shorts, dtype=np.int64)

            # Calculate Root Mean Square (RMS) which equates to volume
            rms = np.sqrt(np.mean(audio_array ** 2))

            # Check if volume spiked dramatically compared to the last chunk
            current_time = time.time()
            if rms > VOLUME_THRESHOLD and (rms / prev_rms) > SUDDENNESS_THRESHOLD:
                if current_time - last_clap_time > COOLDOWN_PERIOD:
                    print("👏 Clap Detected!")
                    # PLACE YOUR AUTOMATION OR TRIGGER CODE HERE!
                    last_clap_time = current_time

            # Update the baseline volume for the next loop execution
            # Avoid letting prev_rms fall all the way to 0
            prev_rms = max(rms, 1.0)

    except KeyboardInterrupt:
        print("\nStopping listener...")
    finally:
        # Clean up streaming assets
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    detect_claps()
