import "leaflet";
import "leaflet-control-custom";
import "./src/Leaflet.AccuratePosition";
import * as markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import * as markerShadow from 'leaflet/dist/images/marker-shadow.png';
import cotizar from "./src/cotiza.js";

document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([-17.784071, -63.180522], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.control.scale().addTo(map);

    $('.leaflet-container').css('cursor', 'crosshair'); //Cursor de cruz Mapa
    map.scrollWheelZoom.disable();

    // console.log(markerIcon2x.default);
    // Redirecciona la ruta del icono
    var icono = L.icon({
        iconUrl: markerIcon2x.default,
        iconRetinaUrl: markerIcon2x.default,
        iconSize: [26, 42],
        iconAnchor: [13, 42],
        popupAnchor: [-3, -76],
        shadowUrl: markerShadow.default,
        shadowRetinaUrl: markerShadow.default,
        shadowSize: [68, 50],
        shadowAnchor: [22, 49]
    });

    // Agrega boton de posicion
    L.control.custom({
        position: 'topright',
        content: '<button aria-label="cotizar">' +
            '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">' +
            '<path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />' +
            '</svg>' +
            '</button>',
        classes: 'bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow',
        style: {
            cursor: 'pointer',
        },
        events: {
            click: function (data) {
                $('#map').prepend("<div id='loading' class='absolute flex items-center justify-center bg-opacity-50 bg-black w-full h-full' style='z-index:10000;'>" +
                    "<div class='animate-spin rounded-full h-32 w-32 border-b-2 border-white'>" +
                    "</div>" +
                    "</div>");
                map.findAccuratePosition({
                    maxWait: 7000,
                    desiredAccuracy: 25
                });
            },
        }
    })
        .addTo(map);

    // Agrega boton de cotizar
    L.control.custom({
        position: 'bottomright',
        content: '<div class="text-center px-1">' +
            '<button id="EnviarUbicacion" class="bg-green-600 hover:bg-green-700 text-xl text-white py-1 px-6 border border-green-700 rounded cursor-not-allowed opacity-50" disabled="true" aria-label="Ubicar">' +
            'Cotizar' +
            '</button>' +
            '</div>',
        style: {
            cursor: 'pointer',
        },
        events: {
            click: function() {
                if (marker) {
                    cotizar(marker);
                }
            }
        },
    })
        .addTo(map);

    // funciones de mapa
    function onAccuratePositionError(e) {
        // addStatus(e.message, 'error');
    }

    function onAccuratePositionProgress(e) {
        var message = 'En Progreso … (Presición: ' + e.accuracy + ')';
        console.log(message, 'progressing');
        // addStatus(message, 'progressing');
    }

    function onAccuratePositionFound(e) {
        var message = 'Ubicación encontrada (Presición: ' + e.accuracy + ')';
        // addStatus(message, 'done');
        map.setView(e.latlng, 16);
        $('body #loading').remove(); //Elimina un elemento de DOM
        marker = L.marker(e.latlng, {icon: icono}).addTo(map);

        if ($('#EnviarUbicacion').prop('disabled')) {
            $('#EnviarUbicacion').prop('disabled', false); //Desactiva boton
            $('#EnviarUbicacion').removeClass('cursor-not-allowed opacity-50');
        }

        console.log(marker._latlng.lat);
        console.log(marker._latlng.lng);

    }

    function addStatus(message, className) {
        var ubic = document.getElementById('status');
        ubic.innerHTML = (message);
        ubic.className = className;
    }

    function onMapClick(e) {
        if (marker != null) {
            map.removeLayer(marker);
        }
        if ($('#EnviarUbicacion').prop('disabled')) {
            $('#EnviarUbicacion').prop('disabled', false); //Desactiva boton
            $('#EnviarUbicacion').removeClass('cursor-not-allowed opacity-50');
        }
        marker = L.marker(e.latlng, {icon: icono}).addTo(map);
        console.log(marker._latlng.lat);
        console.log(marker._latlng.lng);

    }

    map.on('accuratepositionprogress', onAccuratePositionProgress);
    map.on('accuratepositionfound', onAccuratePositionFound);
    map.on('accuratepositionerror', onAccuratePositionError);
    map.on('click', onMapClick);



    

});
