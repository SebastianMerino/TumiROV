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
    fetch('/gamepad', {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify({
            axes: {
                LH: gp.axes[0],
                LV: -gp.axes[1],
                RH: gp.axes[2],
                RV: -gp.axes[3],
            },
            buttons: {
                A: gp.buttons[0].pressed,
                B: gp.buttons[1].pressed,
                X: gp.buttons[2].pressed,
                Y: gp.buttons[3].pressed,
                U: gp.buttons[12].pressed,
                D: gp.buttons[13].pressed,
                L: gp.buttons[14].pressed,
                R: gp.buttons[15].pressed,
            }
        }),
    });

    fetch('/prop_verticales')
        .then(response => response.json())
        .then(infoProp => {
            document.getElementById("prop").innerHTML = infoProp.rpm
        });

    // if (gp.buttons[1].pressed) {
    //     url = "/gamepad_B";
    // } else if (gp.buttons[0].pressed) {
    //     url = "/gamepad_A"
    // } else if (gp.buttons[3].pressed) {
    //     url = "/gamepad_Y";
    // } else if (gp.buttons[12].pressed) {
    //     url = "/gamepad_U";
    // } else if (gp.buttons[13].pressed) {
    //     url = "/gamepad_D";
    // }
    // else { return; } // No se presionó ningún botón
    // fetch(url)
    // .then(response => response.json())
    // .then(infoProp => {
    //     document.getElementById("prop").innerHTML = infoProp.rpm
    // });
}