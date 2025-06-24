let map;
let markers = {};

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: { lat: 24.3636, lng: 88.6241 },
  });

  updateBuses();
  setInterval(updateBuses, 5000);
}

function updateBuses() {
  fetch("/api/bus-locations/")
    .then((response) => response.json())
    .then((data) => {
      data.forEach((bus) => {
        const pos = new google.maps.LatLng(bus.lat, bus.lng);
        const busIcon = {
          url: "/static/images/bus-icon.png",
          scaledSize: new google.maps.Size(40, 40),
          anchor: new google.maps.Point(20, 20),
        };

        if (markers[bus.number]) {
          markers[bus.number].setPosition(pos);
        } else {
          const marker = new google.maps.Marker({
            position: pos,
            map: map,
            icon: busIcon,
            title: `Bus ${bus.number}`,
            label: bus.number,
          });

          const infoWindow = new google.maps.InfoWindow({
            content: `<strong>Bus ${bus.number}</strong><br>Lat: ${bus.lat}<br>Lng: ${bus.lng}`,
          });

          marker.addListener("click", () => {
            infoWindow.open(map, marker);
          });

          markers[bus.number] = marker;
        }
      });
    })
    .catch((error) => console.error("Error fetching bus locations:", error));
}
