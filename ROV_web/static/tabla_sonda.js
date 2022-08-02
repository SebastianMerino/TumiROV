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
          document.getElementById("press").innerHTML = datos.press;
          document.getElementById("temp").innerHTML = datos.temp;
          document.getElementById("cond").innerHTML = datos.cond;
          document.getElementById("sal").innerHTML = datos.sal;
          document.getElementById("O2sat").innerHTML = datos.O2sat;
          document.getElementById("O2ppm").innerHTML = datos.O2ppm;
          document.getElementById("pH").innerHTML = datos.pH;
          document.getElementById("time").innerHTML = datos.time;
          document.getElementById("depth").innerHTML = z.toFixed(1);
        })()
      }
  
      // realiza una accion cada 50 ms
      var intervalID = window.setInterval(actualizar,50)