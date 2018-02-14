import Content from './content';
import leaflet from 'leaflet';
import 'leaflet-search';
import GoogleMapsClient from '@google/maps';

const GOOGLE_AUTH = 'AIzaSyD3HcEXo5I-XxTyZPf34c6gTw20zBWFiNg';
const MAPBOX_TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';
const TILE_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
const ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';

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

export default class Map extends Content {
  constructor() {
    super(...arguments);
    this.values = [];
    this.marker = null;
    this.location = {
      lat: 43.6580617,
      lng: -79.3864974
    }; // general toronto coords
    this.haveLocation = false;
    this.watchId = null;
  }

  get value() {
    return this.values;
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

   geocoding(text, callResponse) {
    googleMapsClient.geocode({
      address: text,
      components: {
        country: 'CA',
      }
    }, function(err, response) {
      if (!err) {
        callResponse(response);
      }
    });
  }


  locationAcquired(position) {
    this.haveLocation = true;
    this.location.lat = position.coords.latitude;
    this.location.lng = position.coords.longitude;
    this.buildMap();
  }

  getDeviceLocation() {
    if ('geolocation' in navigator) {
      this.watchId = navigator.geolocation.watchPosition(this.locationAcquired.bind(this), this.locationFailed.bind(this), {timeout: 10 * 1000});
      console.log(this.watchId);
    } else {
      this.buildMap();
    }
  }

  locationFailed(){
    this.buildMap();
  }

  bind() {
    this.getDeviceLocation();
  }

  buildMap() {
    var self = this;
    var zoom_level = 13; // general view if there's no location
    if (this.haveLocation) { zoom_level = 16; }
    if (typeof this.map === 'undefined') {
        this.map = leaflet.map('map').setView([this.location.lat, this.location.lng], zoom_level);

        var searchControl = new L.Control.Search({
          sourceData: this.geocoding,
          formatData: this.formatJSON,
          filterData: (text, records) => records, // don't filter
          markerLocation: true,
          autoType: false,
          autoCollapse: true,
          minLength: 2,
          marker: DefaultIcon,
          moveToLocation: function (latlng, title, map) {
            if(this.watchId !== null) {
              navigator.geolocation.clearWatch(self.watchId); // stop updating location
            }
            self.location.lat = latlng.lat;
            self.location.lng = latlng.lng;
            map.setView(latlng);
        }
        })

        searchControl.on('search:locationfound', function(e) {
          if(this.watchId !== null) {
              navigator.geolocation.clearWatch(this.watchId);
          }
        });

        this.map.addControl(searchControl);
    } else {
      this.map.panTo([this.location.lat, this.location.lng]);
      this.map.setZoom(zoom_level);
    }

    this.renderMap();
  }

  renderMap() {
    this.initTiles();
    this.setPin();
  }

  initTiles() {
    leaflet.tileLayer(TILE_URL, {
      maxZoom: 19,
      attribution: ATTRIBUTION,
      id: 'mapbox.streets',
      accessToken: MAPBOX_TOKEN
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

  get valid() {
    return this.values.length > 0;
  }

  get template() {
    return (`
      <div class="screen1">
        <div class="progress prog3"></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.text}</h2>
        <div id="map" class=""></div>

      </div>
      `
    )
  }
}