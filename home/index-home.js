import "leaflet";
import "leaflet-control-custom";
import "./src/Leaflet.AccuratePosition";
import * as markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import * as markerShadow from 'leaflet/dist/images/marker-shadow.png';
import cotizar from "./src/cotiza.js";

document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([-17.784071, -63.180522], 11);

    // Inject styles for tooltip horizontal animation
    var style = document.createElement('style');
    style.innerHTML = `
        @keyframes bounce-horizontal {
            0%, 100% { transform: translate(0, -50%); }
            50% { transform: translate(-5px, -50%); }
        }
        .animate-bounce-x {
            animation: bounce-horizontal 1s infinite;
        }
    `;
    document.head.appendChild(style);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
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
        content: '<div id="ubicate-tooltip" class="absolute whitespace-nowrap bg-gray-900 text-white text-xs font-bold py-1.5 px-3 rounded shadow-xl pointer-events-none transition-opacity duration-500 opacity-100 flex items-center animate-bounce-x" style="right: 100%; top: 50%; margin-right: 12px;">' +
            'Ubícate' +
            '<div class="absolute -right-1 top-1/2 -translate-y-1/2 w-2 h-2 bg-gray-900 rotate-45"></div>' +
            '</div>' +
            '<button aria-label="cotizar">' +
            '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">' +
            '<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />' +
            '<path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />' +
            '</svg>' +
            '</button>',
        classes: 'relative overflow-visible bg-white hover:bg-gray-100 text-gray-800 p-2 border border-gray-400 rounded shadow flex items-center justify-center',
        style: {
            cursor: 'pointer',
        },
        events: {
            click: function (data) {
                var tooltip = document.getElementById('ubicate-tooltip');
                if (tooltip) {
                    tooltip.classList.remove('opacity-100');
                    tooltip.classList.add('opacity-0');
                    setTimeout(function () { tooltip.remove(); }, 500);
                }

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
            click: function () {
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
        marker = L.marker(e.latlng, { icon: icono }).addTo(map);

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
        marker = L.marker(e.latlng, { icon: icono }).addTo(map);
        console.log(marker._latlng.lat);
        console.log(marker._latlng.lng);

    }

    map.on('accuratepositionprogress', onAccuratePositionProgress);
    map.on('accuratepositionfound', onAccuratePositionFound);
    map.on('accuratepositionerror', onAccuratePositionError);
    map.on('click', onMapClick);





});
