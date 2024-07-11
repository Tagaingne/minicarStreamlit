import streamlit as st

# HTML et CSS pour l'interface utilisateur
html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, height=device-height;">
    <title>ControlCar</title>
    <style>
        body {
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(to bottom right, blue, red);
        }
        #joystick-container {
            width: 50vmin;
            height: 50vmin;
            background: rgba(255, 0, 0, 0.3);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            touch-action: none;
        }
        #joystick {
            width: 12.5vmin;
            height: 12.5vmin;
            background: white;
            border-radius: 50%;
            position: relative;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 2px solid #fff;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <img class="shrinkToFit" src='http://192.168.204.90:7000' alt="Image de la Minicar" width="400" height="296">
    <div id="joystick-container">
        <div id="joystick"></div>
    </div>
    <script>
        let joystick = document.getElementById('joystick');
        let container = document.getElementById('joystick-container');
        let lastX = 0;
        let lastY = 0;
        let isStopped = false;
        let sendInterval = 100; // 0,1 seconde
        let ws;

        function setupWebSocket() {
            ws = new WebSocket('ws://192.168.204.90/ws');

            ws.onmessage = (event) => {
                try {
                    let message = JSON.parse(event.data);
                    if (message.cmd === 9 && message.data === 1) {
                        // Gérer l'activation de la caméra ou d'autres actions
                    } else {
                        // Gérer d'autres messages JSON si nécessaire
                    }
                } catch (e) {
                    console.log('Erreur de décodage JSON:', e);
                    console.log('Message reçu:', event.data);
                }
            };

            ws.onerror = (error) => {
                console.log('Erreur WebSocket:', error);
            };

            ws.onclose = () => {
                console.log('WebSocket fermé');
                setTimeout(() => {
                    if (ws.readyState === WebSocket.CLOSED) {
                        setupWebSocket(); // Réessayer la connexion
                    }
                }, 5000);
            };
        }

        function sendCommand() {
            let leftSpeed = getSpeed(lastY + lastX);
            let rightSpeed = getSpeed(lastY - lastX);

            let stopLEDCommand = { cmd: 5, data: [-9, 255, 0, 0] };
            let moveLEDCommand = { cmd: 5, data: [-9, 0, 0, 255] };

            if (leftSpeed === 0 && rightSpeed === 0) {
                if (!isStopped) {
                    let stopCommand = { cmd: 1, data: [0, 0, 0, 0] };
                    ws.send(JSON.stringify(stopCommand));
                    ws.send(JSON.stringify(stopLEDCommand));
                    isStopped = true;
                }
                return;
            } else {
                if (isStopped) {
                    ws.send(JSON.stringify(moveLEDCommand));
                    isStopped = false;
                }
            }

            let command = { cmd: 1, data: [leftSpeed, leftSpeed, rightSpeed, rightSpeed] };
            ws.send(JSON.stringify(command));
        }

        function getSpeed(value) {
            if (value > 0.5) return 1000;
            if (value > 0.2) return 500;
            if (value < -0.5) return -1000;
            if (value < -0.2) return -500;
            return 0;
        }

        function onJoystickMove(event) {
            let rect = container.getBoundingClientRect();
            let centerX = rect.width / 2;
            let centerY = rect.height / 2;
            let x, y;
            if (event.touches) {
                x = event.touches[0].clientX - rect.left - centerX;
                y = event.touches[0].clientY - rect.top - centerY;
            } else {
                x = event.clientX - rect.left - centerX;
                y = event.clientY - rect.top - centerY;
            }
            let radius = Math.min(centerX, centerY);
            let distance = Math.min(Math.sqrt(x * x + y * y), radius);
            let angle = Math.atan2(y, x);
            lastX = (distance / radius) * Math.cos(angle);
            lastY = (distance / radius) * Math.sin(angle);
            joystick.style.transform = `translate(${lastX * radius}px, ${lastY * radius}px)`;
        }

        function resetJoystick() {
            lastX = 0;
            lastY = 0;
            joystick.style.transform = 'translate(0, 0)';
        }

        joystick.addEventListener('mousedown', (event) => {
            document.addEventListener('mousemove', onJoystickMove);
            document.addEventListener('mouseup', () => {
                document.removeEventListener('mousemove', onJoystickMove);
                resetJoystick();
            }, { once: true });
        });

        joystick.addEventListener('touchstart', (event) => {
            document.addEventListener('touchmove', onJoystickMove);
            document.addEventListener('touchend', () => {
                document.removeEventListener('touchmove', onJoystickMove);
                resetJoystick();
            }, { once: true });
        });

        setupWebSocket();
        setInterval(sendCommand, sendInterval);
    </script>
</body>
</html>
"""

# Utilisation de Streamlit pour afficher le HTML
st.components.v1.html(html_code, height=800, scrolling=True)


# import streamlit as st
# import streamlit.components.v1 as components

# def main():
#     st.title("MINICAR")

#     # Charger le contenu HTML depuis le fichier controlcar.html
#     with open('controlCar.html', 'r', encoding='utf-8') as f:
#         controlcar_html = f.read()

#     # Afficher le contenu HTML dans Streamlit
#     components.html(controlcar_html, height=800)

# if __name__ == '__main__':
#     main()
