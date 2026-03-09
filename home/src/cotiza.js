import { postData } from "./postCliente.js";

const closebutton = document.getElementById("closebutton");
const contratar = document.getElementById("contratar");
closebutton.addEventListener("click", () => {
  modal.classList.remove("scale-100");
  modal.classList.add("scale-0");
});

function generarCodigo(precio) {
  const now = new Date();
  
  // Año: últimos dos dígitos
  const anio = now.getFullYear() % 100;

  // Mes y día con 2 dígitos
  const mes = String(now.getMonth() + 1).padStart(2, '0'); // meses van de 0 a 11
  const dia = String(now.getDate()).padStart(2, '0');

  // Convertir precio a string para acceder a dígitos
  const precioStr = precio.toString();

  let d1 = precioStr[0] || '0';
  let d2 = precioStr[1] || '0';
  let d3 = precioStr[2] || '0';
  let d4 = precioStr[3] || '';

  // Si el precio es de 3 dígitos, usar d3 como último
  // Si el precio es de 4 dígitos, usar d3 + d4 como último
  const final = precioStr.length === 4 ? d3 + d4 : d3;

  // Concatenar todos los componentes
  const codigo = `${anio}${d1}${mes}${d2}${dia}${final}`;
  return codigo;
}

export default async function cotizar(marker) {
  document.getElementById("loading").classList.remove("invisible");
  document.body.style.overflow = "hidden";
  const modal = document.getElementById("modal");
  const h2Tag = modal.getElementsByTagName("h2")[0];
  const pTag = modal.getElementsByTagName("p")[0];
  let disponibilidad;

  const response = await fetch(`https://pozosscz.com/api/v1/contratar/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      lat: marker.getLatLng().lat.toFixed(6),
      lon: marker.getLatLng().lng.toFixed(6),
    }),
  });
  if (!response.ok) {
    throw new Error("Failed to fetch routes");
  }
  const data = await response.json();
  document.getElementById("loading").classList.add("invisible");
  document.body.style.overflow = "auto";
  modal.classList.remove("scale-0");
  modal.classList.add("scale-100");

  console.log(data);
  console.log(data.factor_zona);
  if (data.factor_zona == 0) {
    h2Tag.innerText = "Fuera de Rango"; //cambia el codigo de precio
    pTag.innerText = mjeFueraDeRango; //cambia el texto de precio
    confirmar.innerText = "Contactarse"; //cambia el texto de precio
    disponibilidad = false;
  } else {
    var precioTotal = data.precio;
    var precioRound = Math.floor(precioTotal / 10) * 10;
    if (precioRound % 100 === 0) { //si el precio es multiplo de 100, se resta 5
      precioRound -= 5;
    }
    console.log(precioRound);
    h2Tag.innerText = "Bs. " + precioRound; //cambia el codigo de precio
    pTag.innerText = mjeCotiza; //cambia el texto de precio
    confirmar.innerText = "Coordinar Servicio"; //cambia el texto de precio
    disponibilidad = true;
  }

  contratar.addEventListener("click", async function () {
    if (disponibilidad) {
      var codigo = generarCodigo(precioRound);
      await postData("multisane", "", precioRound, marker, "COT", "CLC", codigo);
      var url = `https://wa.me/591${celular}?text=Código+de+cotización:+${codigo}%0D%0a${mjeWAContratando}%0D%0ahttps://maps.google.com/maps?q=${marker._latlng.lat}%2C${marker._latlng.lng}&z=17&hl=es`;
    } else {
      var url = `https://wa.me/591${celular}?text=${mjeWAFueraDeRango}`;
    }
    modal.classList.remove("scale-100");
    modal.classList.add("scale-0");
    window.open(url);
  });
}

