// funcion para actualizar tabla
const actualizar = function () {
    fetch('/datos_PX4')
    .then(response => response.json())
    .then(datos_PX4 => {
        var orient = datos_PX4.attitude.yaw*180/3.141592;
        var vel = datos_PX4.motors;
        document.getElementById("yaw").innerHTML = orient.toFixed(1);
        document.getElementById("speed").innerHTML = datos_PX4.vel_mod.toFixed(2);
        document.getElementById("time").innerHTML = datos_PX4.time_boot;
        document.getElementById("prop1").innerHTML = vel[0].toFixed(2);
        document.getElementById("prop2").innerHTML = vel[1].toFixed(2);
        document.getElementById("prop3").innerHTML = vel[2].toFixed(2);
        document.getElementById("prop4").innerHTML = vel[3].toFixed(2);
    });

    fetch('/prop_verticales')
    .then(response => response.json())
    .then(infoProp => {
        document.getElementById("prop5").innerHTML = infoProp.vel_der.toFixed(2)
        document.getElementById("prop6").innerHTML = infoProp.vel_izq.toFixed(2)
    });

    fetch('/datos_sonda')
    .then(response => response.json())
    .then(sonda => {
        document.getElementById("depth").innerHTML = sonda.depth.toFixed(1);
  });
}

// Actualizar tabla cada X milisegundos
var navID = window.setInterval(actualizar,100)