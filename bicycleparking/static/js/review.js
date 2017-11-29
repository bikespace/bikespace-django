import leaflet from 'leaflet';
const TILE_URL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';
const ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';

export default class Review {
  constructor(survey) {
    this.survey = survey;

  }

  render() {
    this.el = this.el || document.getElementById('render');
    this.el.innerHTML = this.template();
    this.bind();
  }

  bind() {
    document.getElementById('button').addEventListener('click', (event) => {
      this.survey.router.navigate(`/`);
    });
    this.createReadMap();
    this.createPicture();

  }

  createPicture() {
    if (this.survey.state.photo) {
      var ctx = $('#picture')[0].getContext('2d');
      var img = new Image();
      img.onload = function () {
        ctx.drawImage(img, 0, 0, $('#picture')[0].width, $('#picture')[0].height);
      }
      img.src = URL.createObjectURL(this.survey.state.photo);
    }
  }

  createReadMap() {
    this.map = leaflet.map('map').setView([this.survey.state.location.lat, this.survey.state.location.lng], 16);
    leaflet.tileLayer(TILE_URL, {
      attribution: ATTRIBUTION,
      maxZoom: 18,
      id: 'mapbox.streets',
      accessToken: TOKEN
    }).addTo(this.map);
    this.marker = L.marker(this.survey.state.location, {
      draggable: false
    });
    this.marker.addTo(this.map);
    this.map.dragging.disable();
    this.map.touchZoom.disable();
    this.map.doubleClickZoom.disable();
    this.map.scrollWheelZoom.disable();
    this.map.boxZoom.disable();
    this.map.keyboard.disable();
    this.map.zoomControl.disable()
  }
  template() {
    return (`
      <h1> Thanks !</h1>
      <div class="row">
        <form class="col s12">
        <div class="row col s12">
          <p>Thank you for your involvement.</p>
          <p>You want to park your bike on ${this.survey.state.report_date} a ${this.survey.state.report_time} for a ${this.survey.state.duration} time</p>      
        </div>
        <div class="row col s12">
          <div class="input-field">
            <p>Desired location</p>
            <div id="map" class=""></div>    
          </div>
        </div>
        <div class="row col s12">
          <div class="input-field">
            <canvas id="picture"></canvas>
          </div>
        </div>
        <button id="button" class="waves-effect waves-light btn">Come back to home</button>

        </form>
      </div>
      `
    )
  }
}