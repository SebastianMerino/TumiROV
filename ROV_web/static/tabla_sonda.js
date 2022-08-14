// funcion para actualizar tabla
const actualizar_tabla = function () {
	fetch('/datos_sonda')
	.then(response => response.json())
	.then(sonda => {
			document.getElementById("press").innerHTML = sonda.press;
			document.getElementById("temp").innerHTML = sonda.temp;
			document.getElementById("cond").innerHTML = sonda.cond;
			document.getElementById("sal").innerHTML = sonda.sal;
			document.getElementById("O2sat").innerHTML = sonda.O2sat;
			document.getElementById("O2ppm").innerHTML = sonda.O2ppm;
			document.getElementById("pH").innerHTML = sonda.pH;
			document.getElementById("time").innerHTML = sonda.time;
			document.getElementById("depth").innerHTML = sonda.depth.toFixed(1);
	});
}

// realiza una accion cada 50 ms
var actTablaID = window.setInterval(actualizar_tabla,50)