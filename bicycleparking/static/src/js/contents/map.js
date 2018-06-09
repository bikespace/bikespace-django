import Content from './content';
import GoogleMapsClient from '@google/maps';


export default class Map extends Content {
  constructor() {
    super(...arguments);
    this.marker = null;
    this.location = {
      lat: 43.6580617,
      lng: -79.3864974
    };
    this.haveLocation = false;
    this.watchId = null;
    this.marker = null;
  }

  get value() {
    this.values.push([this.marker.position.lat(), this.marker.position.lng()])
    return this.values;
  }

  bind() {
    this.values = this.getDataFromSession(this.props['key']);
    this.buildMap();
  }

  buildMap() {
    var self = this;
    var zoom_level = 13;
    if (this.haveLocation) { zoom_level = 16; }
    if (typeof this.map === 'undefined') {
      var my_localisation = JSON.parse(localStorage.getItem('my_localisation'));
      if(!my_localisation){
        my_localisation= this.location;
      }
      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: zoom_level,
        center: my_localisation
      });

      this.marker = new google.maps.Marker({
        position: my_localisation,
        draggable: true,
        map: map
      });
    }
  }

  moveBus(map, marker) {
    marker.setPosition(new google.maps.LatLng(0, 0));
    map.panTo(new google.maps.LatLng(0, 0));

  }

  get valid() {
    return this.values.length > 0;
  }

  get template() {
    return (`
      <div class="screen1 visible">
        <div class="progLine"><div class="progress prog3"></div></div>
        <h1>${this.props.heading}</h1>
        <h2>${this.props.text}</h2>
        <div id="map" class=""></div>

      </div>
      `
    )
  }
}