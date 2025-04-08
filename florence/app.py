from flask import Flask, render_template, jsonify, request
import threading
import time
from hardware.led_controller import LEDController
from hardware.printer_controller import PrinterController
import random
import json

app = Flask(__name__)

# Initialize hardware controllers
led_controller = LEDController()
printer_controller = PrinterController()

# Plant response messages
PLANT_RESPONSES = [
    "Stable all around, Perfect temperature and humidity.",
    "This is joyful. I am growing fast.",
    "Too much. Let me rest.",
    "Let's play with light again!",
    "Your presence settles me. Light flows through my cells. I am opening to the day.",
    "I'm in rest mode. Quiet is good.",
    "Energy is abundant. My leaves stretch. Every cell is buzzing with light.",
    "There's too much right now. I am protecting my cells. Please dim your light.",
    "I sense change. I don't understand, but I lean toward it. I am aware.",
    "Light has gone. I slow down, storing what I can. I rest, quietly aware.",
    "My systems are alert. Conditions are harsh. I am holding on, but it's not easy.",
    "Your message changes me. I grew because of you. I recognize your light."
]

response_index = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    global response_index
    message = request.json.get('message', '')
    
    # Start LED sequence in background
    led_thread = threading.Thread(target=led_controller.run_sequence)
    led_thread.start()
    
    # Simulate processing time
    time.sleep(120)  # 2 minutes for LED sequence
    
    # Get next plant response
    response = PLANT_RESPONSES[response_index]
    response_index = (response_index + 1) % len(PLANT_RESPONSES)
    
    # Print response
    printer_controller.print_message(response)
    
    return jsonify({
        'status': 'success',
        'response': response
    })

@app.route('/get_status', methods=['GET'])
def get_status():
    # Return current status of processing
    return jsonify({
        'semantic_analysis': led_controller.get_semantic_progress(),
        'sentiment_analysis': led_controller.get_sentiment_progress(),
        'translation': led_controller.get_translation_progress(),
        'message_sent': led_controller.get_message_progress(),
        'receiving_response': led_controller.get_response_progress()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 