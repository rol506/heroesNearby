// 1. Create the map, centered on some default location (e.g., London)
const map = L.map('map').setView([51.505, -0.09], 13);

// 2. Add the OpenStreetMap tile layer — this is the actual "picture" of the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// We'll keep a reference to markers so we can clear them between searches
let currentMarkers = [];
