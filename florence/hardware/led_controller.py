import board
import neopixel
import time
import threading

class LEDController:
    def __init__(self):
        # Initialize the NeoPixel strip
        self.pixel_pin = board.D10  # GPIO10 (MOSI)
        self.num_pixels = 24
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.5, auto_write=False
        )
        
        self._semantic_progress = 0
        self._sentiment_progress = 0
        self._translation_progress = 0
        self._message_progress = 0
        self._response_progress = 0
        
        self._progress_lock = threading.Lock()

    def clear(self):
        """Clear all pixels."""
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def blink(self, color, times, duration=0.5):
        """Blink LED pattern."""
        for _ in range(times):
            self.pixels.fill(color)
            self.pixels.show()
            time.sleep(duration)
            self.clear()
            time.sleep(duration)

    def pulse(self, color, times, duration=1.0):
        """Slow pulse LED pattern."""
        for _ in range(times):
            # Fade in
            for i in range(100):
                brightness = i / 100.0
                r = int(color[0] * brightness)
                g = int(color[1] * brightness)
                b = int(color[2] * brightness)
                self.pixels.fill((r, g, b))
                self.pixels.show()
                time.sleep(duration/200)
            
            # Fade out
            for i in range(100, -1, -1):
                brightness = i / 100.0
                r = int(color[0] * brightness)
                g = int(color[1] * brightness)
                b = int(color[2] * brightness)
                self.pixels.fill((r, g, b))
                self.pixels.show()
                time.sleep(duration/200)

    def fade_inout(self, color, times, duration=1.0):
        """Fade in/out LED pattern."""
        for _ in range(times):
            # Fade in (slower)
            for i in range(100):
                brightness = i / 100.0
                r = int(color[0] * brightness)
                g = int(color[1] * brightness)
                b = int(color[2] * brightness)
                self.pixels.fill((r, g, b))
                self.pixels.show()
                time.sleep(duration/100)  # Slower fade
            
            # Hold at full brightness
            time.sleep(duration/2)
            
            # Fade out (slower)
            for i in range(100, -1, -1):
                brightness = i / 100.0
                r = int(color[0] * brightness)
                g = int(color[1] * brightness)
                b = int(color[2] * brightness)
                self.pixels.fill((r, g, b))
                self.pixels.show()
                time.sleep(duration/100)  # Slower fade

    def blink_pulse(self, color, times, duration=0.5):
        """Blink-pulse LED pattern."""
        for _ in range(times):
            # Quick blink
            self.pixels.fill(color)
            self.pixels.show()
            time.sleep(duration/4)
            self.clear()
            time.sleep(duration/4)
            
            # Quick pulse
            for i in range(50):  # Faster pulse
                brightness = i / 50.0
                r = int(color[0] * brightness)
                g = int(color[1] * brightness)
                b = int(color[2] * brightness)
                self.pixels.fill((r, g, b))
                self.pixels.show()
                time.sleep(duration/100)
            
            for i in range(50, -1, -1):
                brightness = i / 50.0
                r = int(color[0] * brightness)
                g = int(color[1] * brightness)
                b = int(color[2] * brightness)
                self.pixels.fill((r, g, b))
                self.pixels.show()
                time.sleep(duration/100)

    def flash(self, color, times, duration=0.2):
        """Quick flash LED pattern."""
        for _ in range(times):
            self.pixels.fill(color)
            self.pixels.show()
            time.sleep(duration)
            self.clear()
            time.sleep(duration/2)

    def run_sequence(self):
        """Run the full LED sequence."""
        # Reset progress
        self._reset_progress()
        
        # Define colors
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        
        # Sequence mapping based on the message pattern
        sequence = [
            (self.blink, RED, 3),         # "Hello Florence" (Greeting)
            (self.pulse, BLUE, 5),        # "it is nice" (Appreciation)
            (self.fade_inout, RED, 5),    # "to see you" (Connection)
            (self.blink_pulse, BLUE, 5),  # "How are you" (Question)
            (self.blink_pulse, RED, 5),   # "How are you" (Question)
            (self.flash, GREEN, 1),       # "today" (Time)
        ]
        
        # Run sequence 3 times (as specified)
        start_time = time.time()
        target_duration = 120  # 2 minutes
        
        while time.time() - start_time < target_duration:
            for func, color, times in sequence:
                func(color, times)
                self._update_progress()
                
                # Check if we've exceeded the target duration
                if time.time() - start_time >= target_duration:
                    break
        
        self.clear()

    def _reset_progress(self):
        """Reset all progress values."""
        with self._progress_lock:
            self._semantic_progress = 0
            self._sentiment_progress = 0
            self._translation_progress = 0
            self._message_progress = 0
            self._response_progress = 0

    def _update_progress(self):
        """Update progress values during sequence."""
        with self._progress_lock:
            if self._semantic_progress < 100:
                self._semantic_progress += 16.67
            elif self._sentiment_progress < 100:
                self._sentiment_progress += 16.67
            elif self._translation_progress < 100:
                self._translation_progress += 16.67
            elif self._message_progress < 100:
                self._message_progress += 5.56
            elif self._response_progress < 100:
                self._response_progress += 5.56

    # Getter methods for progress values
    def get_semantic_progress(self):
        with self._progress_lock:
            return min(100, self._semantic_progress)

    def get_sentiment_progress(self):
        with self._progress_lock:
            return min(100, self._sentiment_progress)

    def get_translation_progress(self):
        with self._progress_lock:
            return min(100, self._translation_progress)

    def get_message_progress(self):
        with self._progress_lock:
            return min(100, self._message_progress)

    def get_response_progress(self):
        with self._progress_lock:
            return min(100, self._response_progress) 