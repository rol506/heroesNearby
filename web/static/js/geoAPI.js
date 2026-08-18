function geoSuccess(pos) {
  sendInfo(`${pos.coords.latitude} ${pos.coords.longitude}`);
  console.log(pos);
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
  sendError("GEOLOCATION UNSUPPORTED"); // браузер не поддерживает
}
