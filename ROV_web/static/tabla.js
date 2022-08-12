// funcion para actualizar tabla
const actualizar = function () {
    // fetch('/datos_PX4')
    // .then(response => response.json())
    // .then(datos_PX4 => {
    //     orient = datos_PX4.attitude.yaw*180/3.141592
    //     document.getElementById("yaw").innerHTML = orient.toFixed(1);
    //     document.getElementById("speed").innerHTML = datos_PX4.velocity.vz;
    //     document.getElementById("time").innerHTML = datos_PX4.time_boot;
    // });

    fetch('/prop_verticales')
    .then(response => response.json())
    .then(infoProp => {
        document.getElementById("prop5").innerHTML = infoProp.vel_der.toFixed(2)
        document.getElementById("prop6").innerHTML = infoProp.vel_izq.toFixed(2)
    });
}

// realiza una accion cada 50 ms
var intervalID = window.setInterval(actualizar,50)