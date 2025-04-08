from escpos.printer import Usb
import usb.core
import usb.util

class PrinterController:
    def __init__(self):
        # USB printer settings (you may need to adjust these values)
        self.vendor_id = 0x0416  # Default vendor ID for thermal printers
        self.product_id = 0x5011  # Default product ID for thermal printers
        
        try:
            self.printer = Usb(self.vendor_id, self.product_id)
        except Exception as e:
            print(f"Warning: Could not initialize printer: {e}")
            self.printer = None

    def print_message(self, message):
        """Print a message to the thermal printer."""
        if self.printer is None:
            print(f"Would print: {message}")
            return
            
        try:
            # Add some styling to the message
            self.printer.set(align='center', font='a', width=2, height=2)
            self.printer.text("\n")
            self.printer.text("Florence Says:\n")
            self.printer.text("-" * 32 + "\n")
            
            # Print the main message
            self.printer.set(align='left', font='a', width=1, height=1)
            self.printer.text(message + "\n")
            
            # Add a footer
            self.printer.text("\n")
            self.printer.set(align='center', font='a', width=1, height=1)
            self.printer.text("-" * 32 + "\n")
            self.printer.text("Plant-Human Interface\n")
            
            # Cut the paper
            self.printer.cut()
            
        except Exception as e:
            print(f"Error printing message: {e}")
            print(f"Message that would have been printed: {message}")

    def __del__(self):
        """Cleanup when the object is destroyed."""
        if self.printer:
            try:
                self.printer.close()
            except:
                pass 