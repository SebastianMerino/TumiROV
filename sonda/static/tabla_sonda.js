// funcion para actualizar tabla
var datos, p, z;
const g = 9.78255, c1 = 9.72659, c2 = -2.2512E-5, c3 = 2.279E-10, c4 = -1.82E-15; 
const actualizar_tabla = function () {
    fetch('/datos_sonda')
    .then(response => response.json())
    .then(datos_sonda => {
        p = datos_sonda.press
        z = (c1*p + c2*p**2 + c3*p**3 + c4*p**4)/(g + 1.092E-6*p)
        document.getElementById("press").innerHTML = datos_sonda.press;
        document.getElementById("temp").innerHTML = datos_sonda.temp;
        document.getElementById("cond").innerHTML = datos_sonda.cond;
        document.getElementById("sal").innerHTML = datos_sonda.sal;
        document.getElementById("O2sat").innerHTML = datos_sonda.O2sat;
        document.getElementById("O2ppm").innerHTML = datos_sonda.O2ppm;
        document.getElementById("pH").innerHTML = datos_sonda.pH;
        document.getElementById("time").innerHTML = datos_sonda.time;
        document.getElementById("depth").innerHTML = z.toFixed(1);
        document.getElementById("prop").innerHTML = infoProp.RPM
    });
}

// realiza una accion cada 50 ms
var actTablaID = window.setInterval(actualizar_tabla,50)