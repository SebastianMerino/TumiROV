// obtener json de url
async function get() {
    let url = '/datos_PX4'
    let obj = await (await fetch(url)).json();  
    return obj;
}

// funcion para actualizar tabla
var datos_PX4,orient;
const actualizar = function () {
(async () => {
    datos_PX4 = await get()
    orient = datos_PX4.attitude.yaw*180/3.141592
    document.getElementById("yaw").innerHTML = orient.toFixed(1);
    document.getElementById("speed").innerHTML = datos_PX4.velocity.vz;
    document.getElementById("time").innerHTML = datos_PX4.time_boot;
})()
}

// realiza una accion cada 50 ms
var intervalID = window.setInterval(actualizar,50)