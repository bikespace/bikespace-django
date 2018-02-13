import Content from './content';
import leaflet from 'leaflet';
import MapboxClient from 'mapbox/lib/services/geocoding';
import 'leaflet-search';

const ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';
const TILE_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';

export default class Map extends Content {
  constructor() {
    super(...arguments);
    this.values = [];
    this.getDeviceLocation();
  }


  getDeviceLocation() {
    if ('geolocation' in navigator) {
      navigator.geolocation.watchPosition(this.locationAcquired.bind(this), this.locationFailed);
    }
  }

  locationAcquired(position) {
    this.location = {};
    this.location.lat = position.coords.latitude;
    this.location.lng = position.coords.longitude;
  }


  get value() {
    return this.location;
  }

  bind() {
    var self = this;
    this.map = leaflet.map('mapid').setView([this.location.lat, this.location.lng], 25);
    this.renderMap();
  }

  renderMap() {
    this.initTiles();
    this.setPin();
  }


  initTiles() {
    leaflet.tileLayer(TILE_URL, {
      attribution: ATTRIBUTION,
      id: 'mapbox.streets',
      maxZoom: 18,
      accessToken: TOKEN
    }).addTo(this.map);
  }

  setPin() {
    if (this.marker) {
      this.marker.remove();
    }
    this.marker = L.marker(this.location, {
      draggable: true
    });
    this.marker.addTo(this.map);
  }

  get template() {
    return (`
      <div class="screen1">
        <div class="progress prog3"></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.text}</h2>
        <div id="mapid"></div>
      </div>
      `
    )
  }
}