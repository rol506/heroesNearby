
// defaul for kaliningrad
var lat = 54.71096765269365;
var lon = 20.508728027343754;

// 1. Create the map, centered on some default location
const map = L.map('map', {zoomControl: false}).setView([lat, lon], 13);

// 2. Add the OpenStreetMap tile layer — this is the actual "picture" of the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors',
  unloadInvisibleTiles: true,
  reuseTiles: true,
}).addTo(map);


function geoSuccess(pos) {
  //sendInfo(`${pos.coords.latitude} ${pos.coords.longitude}`);
  lat = pos.coords.latitude;
  lon = pos.coords.longitude;
  console.log(pos);
  map.setView([lat, lon], 13);
}

function geoDenied(err) {
  switch (err.code) {
    case 1:
      sendError("PERMISSION DENIED"); // юзер отказался
      break;
    case 2:
      sendError("POSITION UNAVAILABLE"); // ошибка получения
      break;
    case 3:
      sendError("TIMEOUT"); // таймаут
      break;
  }
  console.log(err);
}

// получить геолокацию
if ("geolocation" in navigator) {
  navigator.geolocation.getCurrentPosition(geoSuccess, geoDenied); // все получилось
} else {
  //sendError("GEOLOCATION UNSUPPORTED"); // браузер не поддерживает
}

// We'll keep a reference to markers so we can clear them between searches
let currentMarkers = [];

const input = document.getElementById('street-input');
const button = document.getElementById('search-btn');
const resultsList = document.getElementById('search-results');
const aside = document.getElementById("aside");
const continueBtn = document.getElementById("continue");
const closeBtn = document.getElementById("close");
const description = document.getElementById("description");
const descriptionData = document.getElementById("descriptionSpan");
const fact = document.getElementById("fact");

//aside.classList.remove("active");
continueBtn.classList.add("active");
continueBtn.addEventListener("click", (_) => {
  continueBtn.classList.remove("active");
  closeBtn.classList.add("active");
  description.classList.add("active");
})
closeBtn.classList.remove("active");
closeBtn.addEventListener("click", (_) => {
  continueBtn.classList.add("active");
  closeBtn.classList.remove("active");
  description.classList.remove("active");
})

async function search(e) {
  if (e.type == "keydown" && e.key != "Enter") return;
  const street = input.value.trim();
  const region = "Калининград";
  if (!street) return;

  const response = await fetch(`/search?street=${encodeURIComponent(street)}&region=${encodeURIComponent(region)}`);
  console.log(response);
  if (response.status != 200) {
    sendError("Не удалось выполнить поиск!");
    return;
  }
  const res = await response.json();
  if (res.code != 0) {
    sendError("Не удалось выполнить поиск!");
    return;
  }

  displayResults(res.data);
}

button.addEventListener('click', search);
input.addEventListener('keydown', search);

map.on('click', function(e) {        
  var popLocation= e.latlng;
  L.popup()
    .setLatLng(popLocation)
    .setContent('<p>Hello world!<br>This is a nice popup.</p>')
    .openOn(map);        

    });


function clearResults() {
  resultsList.classList.remove("active");
}

function displayResults(results) {
  aside.classList.remove("active");
  resultsList.innerHTML = '';
  resultsList.classList.add("active")
  clearMarkers();

  if (results.length === 0) {
    resultsList.innerHTML = '<li>No matches found.</li>';
    return;
  }

  results.forEach(place => {
    const li = document.createElement('li');
    descriptionData.innerHTML = place.description;
    fact.innerHTML = place.fact;
    li.textContent = place.display_name;
    li.addEventListener('click', () => {focusOnPlace(place); clearResults(); aside.classList.add("active");});
    resultsList.appendChild(li);

    addMarker(place);
  });

  // Automatically zoom to the first result
  focusOnPlace(results[0]);
}

function addMarker(place) {
  const marker = L.marker([place.lat, place.lon]).addTo(map);
  marker.bindPopup(place.display_name);
  currentMarkers.push(marker);
}

function clearMarkers() {
  currentMarkers.forEach(m => map.removeLayer(m));
  currentMarkers = [];
}

function focusOnPlace(place) {
  map.setView([place.lat, place.lon], 16);
}
