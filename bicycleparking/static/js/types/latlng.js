import Input from './input';
const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';
import MapboxClient from 'mapbox/lib/services/geocoding';
import Map from './map';
import { on } from '../util';

export default class LatLngInput extends Input {
  constructor() {
    super(...arguments);
    this.state = {
      lat: null,
      lng: null
    }
    this.map = null;
    this.mapBoxClient = new MapboxClient(TOKEN);
    this.output = null;
  }

  get template() {
    return (
      `<div class="View View--light" />
        <div id="search">
          <button type="button" id="locate" class="button button--orange StepOne__button">Get Current Location</button>
          <div id="output" class="StepOne__output"></div>
        </div>
        <div id="map" class=""></div>
      </div>`
    )
  }

  get query() {
    const loc = window.location.href.split('?');
    if (loc.length > 1) {
      const params = loc[1].split('&');
      return params.reduce((memo, param) => {
        const [key, value] = param.split('=');
        return Object.assign({}, memo, {
          [key]: value
        })
      }, {})
    } else {
      return {}
    }
  }

  setQuery(query) {
    const string = Object.keys(query).reduce((memo, key) => {
      memo += `${key}=${query[key]}&`
    }, '?');
    window.location.replace(window.location.href + string)
  }
  
  locationAcquired(position) {
    this.onMessage('')
    if (!this.query) {
      this.setQuery({
        lat: position.coords.latitude,
        lng: position.coords.longitude
      })
    }
    this.map = new Map([position.coords.latitude, position.coords.longitude], this.onSelect.bind(this));
    this.renderMap();
  }

  onSelect(latlng) {
    this.submit(latlng);
  }

  renderMap() {
    this.map.render();
  }

  locationFailed() {
    alert("Sorry, no position available.");
  }

  getDeviceLocation() {
    if ('geolocation' in navigator) {
      this.onMessage('looking')
      navigator.geolocation.watchPosition(this.locationAcquired.bind(this), this.locationFailed);
    } else {
      this.onMessage('no devie access...')
    }
  }

  bind() {
    document.getElementById('locate').addEventListener('click', (evt) => {
      this.getDeviceLocation();
    });
    if (this.query.lat && this.query.lng) {
      this.locationAcquired({
        coords: {
          latitude: this.query.lat,
          longitude: this.query.lng
        }
      });
    }
  }
}