import Step from '../step';
import leaflet from 'leaflet';
const TILE_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
const ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';

export default class StepOneB extends Step {
  constructor(name, copy, survey) {
    super(name, copy, survey);
    const query = survey.router.lastRouteResolved().query;
    const [lat, lng] = query.split('&').map(part => part.split('=')[1]);
    this.lat = lat;
    this.lng = lng;
    this.map = null;
    this.marker = null;
    this.selectedLatLng = {
      lat: this.lat,
      lng: this.lng
    };
    this.mapEl = null;
  }

  get childHtml() {
    const head = this.html;
    const body = `
    <div class="row-fluid">
      <div class="col-sm-12">
        <button id="button" class="button">done</button>
        <div id="map"></div>
      </div>
    </div>
    `;
    return `<div class="View" />${head + body}</div>`;
  }

  render() {
    this.mapEl = document.getElementById('map');
    this.mapEl.classList.add('active');
    this.map = this.map || leaflet.map('map').setView([this.lat, this.lng], 16);
    this.initTiles();
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.childHtml;
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
      this.survey.setState({
        latlng: this.selectedLatLng
      })
      this.map.remove();
      this.map = null;
      this.mapEl.classList.remove('active');
      this.router.navigate('/survey/2')
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
