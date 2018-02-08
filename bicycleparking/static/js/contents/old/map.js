import Input from './input';
import leaflet from 'leaflet';
import MapboxClient from 'mapbox/lib/services/geocoding';
import 'leaflet-search';

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
    for (var i in rawjson.features) {
      key = rawjson.features[i].place_name;
      json[key] = L.latLng(rawjson.features[i].center[1], rawjson.features[i].center[0]);
    }
    return json;
  }

  mapBoxGeocoding(text, callResponse) {
    this.geocoder = new MapboxClient(TOKEN);
    this.geocoder.geocodeForward(text, function (err, res) {
      callResponse(res);
    });
  }


  locationAcquired(position) {
    console.log('position ')
    this.location.lat = position.coords.latitude;
    this.location.lng = position.coords.longitude;
    var self = this;
    this.map = leaflet.map('map').setView([this.location.lat, this.location.lng], 16);
    this.map.addControl(new L.Control.Search({
      sourceData: this.mapBoxGeocoding,
      formatData: this.formatJSON,
      markerLocation: true,
      autoType: false,
      autoCollapse: true,
      minLength: 2,
      marker: DefaultIcon,
      moveToLocation: function(latlng, title, map) {
      	self.location.lat=latlng.lat;
        self.location.lng=latlng.lng;
        //var zoom = map.getBoundsZoom(latlng.layer.getBounds());
  			map.setView(latlng);
      }
    }));
    this.renderMap();
  }

  renderMap() {
    this.initTiles();
    this.setPin();
  }

  getDeviceLocation() {
    if ('geolocation' in navigator) {
      this.onMessage('looking')
      navigator.geolocation.watchPosition(this.locationAcquired.bind(this), this.locationFailed);
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