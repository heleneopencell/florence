document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const submitBtn = document.getElementById('submit-btn');
    const responseText = document.getElementById('response-text');
    const canvas = document.getElementById('signal-canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size
    function resizeCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Progress bars
    const progressBars = {
        semantic: document.getElementById('semantic-progress'),
        sentiment: document.getElementById('sentiment-progress'),
        translation: document.getElementById('translation-progress'),
        message: document.getElementById('message-progress'),
        response: document.getElementById('response-progress')
    };

    // Auto-type initial message
    setTimeout(() => {
        const initialMessage = "Hello Florence, it is nice to see you. How are you today?";
        let index = 0;
        
        function typeMessage() {
            if (index < initialMessage.length) {
                messageInput.value += initialMessage[index];
                index++;
                setTimeout(typeMessage, Math.random() * 100 + 50);
            } else {
                submitBtn.click();
            }
        }
        
        typeMessage();
    }, 5000);

    // Plant signal visualization
    function drawSignals() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        const time = Date.now() / 1000;
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 2;
        
        // Draw multiple sine waves
        for (let i = 0; i < 3; i++) {
            ctx.beginPath();
            for (let x = 0; x < canvas.width; x++) {
                const frequency = 0.01 + (i * 0.005);
                const amplitude = 20 + (i * 10);
                const y = canvas.height/2 + 
                         Math.sin(x * frequency + time) * amplitude +
                         Math.sin(x * frequency * 2 + time * 1.5) * (amplitude/2);
                
                if (x === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }
            ctx.stroke();
        }
        
        requestAnimationFrame(drawSignals);
    }
    drawSignals();

    // Update progress bars
    function updateProgress() {
        fetch('/get_status')
            .then(response => response.json())
            .then(data => {
                progressBars.semantic.style.width = `${data.semantic_analysis}%`;
                progressBars.sentiment.style.width = `${data.sentiment_analysis}%`;
                progressBars.translation.style.width = `${data.translation}%`;
                progressBars.message.style.width = `${data.message_sent}%`;
                progressBars.response.style.width = `${data.receiving_response}%`;
            });
    }

    // Handle form submission
    submitBtn.addEventListener('click', () => {
        const message = messageInput.value;
        if (!message) return;

        // Disable input during processing
        messageInput.disabled = true;
        submitBtn.disabled = true;
        submitBtn.textContent = 'In Progress...';

        // Start progress updates
        const progressInterval = setInterval(updateProgress, 100);

        // Send message to server
        fetch('/submit_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Display response with typing effect
            let index = 0;
            responseText.textContent = '';
            
            function typeResponse() {
                if (index < data.response.length) {
                    responseText.textContent += data.response[index];
                    index++;
                    setTimeout(typeResponse, Math.random() * 50 + 25);
                }
            }
            
            typeResponse();

            // Reset UI
            messageInput.value = '';
            messageInput.disabled = false;
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit';
            
            // Stop progress updates
            clearInterval(progressInterval);
            
            // Reset progress bars after delay
            setTimeout(() => {
                Object.values(progressBars).forEach(bar => {
                    bar.style.width = '0%';
                });
            }, 2000);
        })
        .catch(error => {
            console.error('Error:', error);
            messageInput.disabled = false;
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit';
            clearInterval(progressInterval);
        });
    });
}); 