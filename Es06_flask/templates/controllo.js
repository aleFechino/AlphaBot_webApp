
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../static/style.css">
    <title>αBot</title>
</head>
<body>

    <h2>αBot</h2>
    <h3>Controllo movimento</h3>

    <!-- CONTROLLI DIREZIONALI -->
    <div class="controls">
        <div class="grid">
            <div></div>
            <button id="btn-avanti" class="btn arrow">↑</button>
            <div></div>

            <button id="btn-sinistra" class="btn arrow">←</button>
            <div></div>
            <button id="btn-destra" class="btn arrow">→</button>

            <div></div>
            <button id="btn-indietro" class="btn arrow">↓</button>
            <div></div>
        </div>
    </div>

    <!-- MOVIMENTI SPECIALI -->
    <h3>Movimenti speciali</h3>
    <form method="post" action="/" class="specials">
        <button type="submit" name="Quadrato">◻ Quadrato</button>
        <button type="submit" name="L">L</button>
        <button type="submit" name="Triangolo">△ Triangolo</button>
    </form>

    <script>
        // Funzione per inviare comandi al server
        function sendCommand(command) {
            fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: command
            });
        }

        // Funzione per gestire pressione e rilascio
        function setupButton(buttonId, command) {
            const button = document.getElementById(buttonId);
            
            // Mouse events
            button.addEventListener('mousedown', (e) => {
                e.preventDefault();
                sendCommand(command);
            });
            
            button.addEventListener('mouseup', (e) => {
                e.preventDefault();
                sendCommand('Stop=1');
            });
            
            button.addEventListener('mouseleave', (e) => {
                sendCommand('Stop=1');
            });

            // Touch events per dispositivi mobili
            button.addEventListener('touchstart', (e) => {
                e.preventDefault();
                sendCommand(command);
            });
            
            button.addEventListener('touchend', (e) => {
                e.preventDefault();
                sendCommand('Stop=1');
            });
        }

        // Configura tutti i pulsanti direzionali
        setupButton('btn-avanti', 'Avanti=1');
        setupButton('btn-indietro', 'Indietro=1');
        setupButton('btn-sinistra', 'Sinistra=1');
        setupButton('btn-destra', 'Destra=1');
    </script>

</body>
</html>