import leaflet from 'leaflet';
const TILE_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
const ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';

const icon = window.ASSETS_PATH + 'marker-icon.png';
const iconShadow = window.ASSETS_PATH + 'marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow
});

L.Marker.prototype.options.icon = DefaultIcon;

export default class Map {
  constructor(latlng, onSelect) {
    const [lat, lng] = latlng;
    this.lat = lat;
    this.lng = lng;
    this.map = null;
    this.marker = null;
    this.selectedLatLng = {
      lat: this.lat,
      lng: this.lng
    };
    this.onSelect = onSelect;
    this.mapEl = null;
  }

  get template() {
    return (`
      <div class="View">
          <button id="button" class="button">done</button>
          <div id="map"></div>
      </div>
    `);
  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.template;
    this.mapEl = document.getElementById('map');
    this.mapEl.classList.add('active');
    this.map = this.map || leaflet.map('map').setView([this.lat, this.lng], 16);
    this.initTiles();
    this.bind();
    this.setPin();
  }

  onMarkerMove(event) {
    this.selectedLatLng = event.latlng;
  }

  setPin() {
    if (this.marker) {
      this.marker.remove();
    }
    this.marker = L.marker(this.selectedLatLng, {
      draggable: true
    });
    this.marker.on('dragend', this.onMarkerMove.bind(this));
    this.marker.addTo(this.map);

  }

  onMapClick(event) {
    this.selectedLatLng = Object.assign({}, event.latlng);
    this.setPin();
  }

  selectLocation() {
    if (this.selectedLatLng) {
      this.map.remove();
      this.map = null;
      this.mapEl.classList.remove('active');
      this.onSelect(this.selectedLatLng)
    }
  }

  bind() {
    this.map.on('click', this.onMapClick.bind(this));
    document.getElementById('button').addEventListener('click', (evt) => {
      this.selectLocation();
    });
  }

  initTiles() {
    leaflet.tileLayer(TILE_URL, {
      attribution: ATTRIBUTION,
      maxZoom: 18,
      id: 'mapbox.streets',
      accessToken: TOKEN
    }).addTo(this.map);
  }
}
