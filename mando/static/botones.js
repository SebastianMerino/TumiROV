/* ----------------------------------------------------------
    SCRIPT PARA RECIBIR COMANDOS DE LOS BOTONES Y ENVIARLOS
Utiliza la Gamepad API de HTML5, con código adapatado de:
https://xtrp.io/blog/2020/12/15/how-to-use-the-html5-gamepad-api/
https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API
------------------------------------------------------------- */

gamepadInfo = document.getElementById("gamepad-info");

// Obtiene el index del gamepad una vez que se conecta
let gamepadIndex;
window.addEventListener('gamepadconnected', event => {
    gamepadIndex = event.gamepad.index;
    gamepadInfo.innerHTML = "Gamepad conectado"
});

window.addEventListener('gamepaddisconnected', event => {
    gamepadInfo.innerHTML = "Esperando al Gamepad. Presione cualquier botón para comenzar."
});

// Escaneo de los botones cada 100 ms
setInterval(() => {
    if(gamepadIndex !== undefined) {
        // a gamepad is connected and has an index
        const myGamepad = navigator.getGamepads()[gamepadIndex];
        gameLoop(myGamepad)
    }
}, 100)

// Actualiza la velocidad segun el boton presionado
var rpm = 0
function gameLoop(gp) {
    if (gp.buttons[1].pressed) {
        url = "/prop_reset";
    } else if (gp.buttons[0].pressed) {
        url = "/prop_desacelerar"
    } else if (gp.buttons[3].pressed) {
        url = "/prop_acelerar";
    } else if (gp.buttons[12].pressed) {
        url = "/prop_subir";
    } else if (gp.buttons[13].pressed) {
        url = "/prop_bajar";
    }
    else { return; } // No se presionó ningún botón
    
    fetch(url)
        .then(response => response.json())
        .then(infoProp => {
            document.getElementById("prop").innerHTML = infoProp.RPM
        });
}