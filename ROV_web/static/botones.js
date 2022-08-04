/* ----------------------------------------------------------
    SCRIPT PARA RECIBIR COMANDOS DE LOS BOTONES Y ENVIARLOS
Utiliza la Gamepad API de HTML5, con código adapatado de:
https://xtrp.io/blog/2020/12/15/how-to-use-the-html5-gamepad-api/
https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API
------------------------------------------------------------- */

gamepadInfo = document.getElementById("gamepad-info");

// Obtiene el index del gamepad una vez que se conecta
let gamepadIndex;
window.addEventListener('gamepadconnected', (event) => {
    gamepadIndex = event.gamepad.index;
    gamepadInfo.innerHTML = "Gamepad conectado"
});

window.addEventListener('gamepaddisconnected', (event) => {
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
        rpm = 0;
        var request = new XMLHttpRequest();
        request.open("GET", "/prop_reset", true);
        request.send();
    } else if (gp.buttons[0].pressed) {
        rpm -= 10;
        var request = new XMLHttpRequest();
        request.open("GET", "/prop_desacelerar", true);
        request.send();
    } else if (gp.buttons[3].pressed) {
        rpm += 10;
        var request = new XMLHttpRequest();
        request.open("GET", "/prop_acelerar", true);
        request.send();
    } else if (gp.buttons[12].pressed) {
        rpm += 500;
        var request = new XMLHttpRequest();
        request.open("GET", "/prop_subir", true);
        request.send();
    } else if (gp.buttons[13].pressed) {
        rpm -= 500;
        var request = new XMLHttpRequest();
        request.open("GET", "/prop_bajar", true);
        request.send();
    }
    if (rpm > 5000) { rpm = 5000 }
    if (rpm < 5000) { rpm = -5000 }
    document.getElementById("prop").innerHTML = rpm
}



// obtener json de url
async function get() {
    let url = '/datos_sonda'
    let obj = await (await fetch(url)).json();  
    return obj;
    }

// funcion para actualizar tabla
var datos, p, z;
const g = 9.78255, c1 = 9.72659, c2 = -2.2512E-5, c3 = 2.279E-10, c4 = -1.82E-15; 
const actualizar = function () {
(async () => {
    datos = await get()
    p = datos.press
    z = (c1*p + c2*p**2 + c3*p**3 + c4*p**4)/(g + 1.092E-6*p)
    document.getElementById("time").innerHTML = datos.time;
    document.getElementById("depth").innerHTML = z.toFixed(1);
})()
}

// realiza una accion cada 50 ms
var intervalID = window.setInterval(actualizar,50)