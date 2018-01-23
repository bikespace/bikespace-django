(function () {
'use strict';

function __$styleInject(css, returnValue) {
  if (typeof document === 'undefined') {
    return returnValue;
  }
  css = css || '';
  var head = document.head || document.getElementsByTagName('head')[0];
  var style = document.createElement('style');
  style.type = 'text/css';
  head.appendChild(style);
  
  if (style.styleSheet){
    style.styleSheet.cssText = css;
  } else {
    style.appendChild(document.createTextNode(css));
  }
  return returnValue;
}

const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';

class Dashboard {
    constructor() {
        console.log('Start dashboard ...');
        mapboxgl.accessToken = TOKEN;
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [-79.402, 43.663],
            zoom: 12
        });
        fetch(`${document.location.origin}/api/survey`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(response => {
            response.json().then(data => {
                data.forEach(element => {
                    console.log(element);
                    var el = document.createElement('div');
                    el.className = 'marker';

                    // make a marker for each feature and add to the map
                    new mapboxgl.Marker(el)
                        .setLngLat([element.longitude, element.latitude])
                        .setPopup(new mapboxgl.Popup({ offset: 25 })
                        .setHTML('<h3>' + element.survey.report_date + '</h3><img id="imagePopup" src="/api/pictures/'+element.photo_uri + '">'))
                        .addTo(map);
                });
            });

        });

    }
}

new Dashboard();

}());
