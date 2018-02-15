import Input from './input';
import leaflet from 'leaflet';
import 'leaflet-search';
import GoogleMapsClient from '@google/maps';

const TILE_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
const ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';
const GOOGLE_AUTH = 'AIzaSyD3HcEXo5I-XxTyZPf34c6gTw20zBWFiNg';

const icon = window.ASSETS_PATH + 'marker-icon.png';
const iconShadow = window.ASSETS_PATH + 'marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow
});
L.Marker.prototype.options.icon = DefaultIcon;

var googleMapsClient = GoogleMapsClient.createClient({
  key: GOOGLE_AUTH
});

export default class MapInput extends Input {
  constructor() {
    super(...arguments);
    this.values = [];
    this.marker = null;
    this.location = {
      lat: null,
      lng: null
    }
  }

  get value() {
    return this.location;
  }

  onSelect(event) {
    console.log(event);
  }

  formatJSON(rawjson) {
    var json = {},
      key;

    var results = rawjson.json.results;
    for (var i in results) {
      key = results[i].formatted_address;
      json[key] = L.latLng(results[i].geometry.location.lat, results[i].geometry.location.lng);
    }
    return json;
  }

  mapBoxGeocoding(text, callResponse) {
    googleMapsClient.geocode({
      address: text,
      region: 'ca'
    }, function(err, response) {
      if (!err) {
        callResponse(response);
      }
    });
  }


  locationAcquired(position) {
    this.location.lat = position.coords.latitude;
    this.location.lng = position.coords.longitude;
    var self = this;
    if (typeof this.map === 'undefined') {
        this.map = leaflet.map('map').setView([this.location.lat, this.location.lng], 16);
    }

    this.map.addControl(new L.Control.Search({
        sourceData: this.mapBoxGeocoding,
        formatData: this.formatJSON,
        filterData: (text, records) => records,
        markerLocation: true,
        autoType: false,
        autoCollapse: true,
        minLength: 2,
        marker: DefaultIcon,
        moveToLocation: function (latlng, title, map) {
            self.location.lat = latlng.lat;
            self.location.lng = latlng.lng;
            map.setView(latlng);
        }
    }));
    this.renderMap();
  }

  locationFailed(){
    console.log('failed to get location')
  }

  renderMap() {
    this.initTiles();
    this.setPin();
  }

  getDeviceLocation() {
    if ('geolocation' in navigator) {
      this.onMessage('looking');
      navigator.geolocation.getCurrentPosition(this.locationAcquired.bind(this), this.locationFailed);
    } else {
      this.onMessage('no device access...')
    }
  }

  initTiles() {
    this.onMessage('');
    leaflet.tileLayer(TILE_URL, {
      attribution: ATTRIBUTION,
      maxZoom: 18,
      id: 'mapbox.streets',
      accessToken: TOKEN
    }).addTo(this.map);
  }

  bind() {
    this.getDeviceLocation();
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
        <div id="map" class=""></div>    
      `
    )
  }

}