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

const contents = {
  ISSUES: 'ISSUES',
  PICTURE: 'PICTURE',
  MAP: 'MAP',
  HAPPENING: 'HAPPENING',
  SUMMARY: 'SUMMARY',
};

const questions = [
  {
    questions: [
      {
        key: 'problem_type',
        type: contents.ISSUES,
        heading: 'What was the issue?',
        text: 'Choose whichever applies',
        required: true,
        error: 'Choose at least one option',
        values: [
          {
            key: 'absent',
            text: "No bike parking nearby"
          },
          {
            key: 'full',
            text: "Nearby bike parking is full"
          },
          {
            key: 'broken',
            text: "Bike parking is broken"
          },
          {
            key: 'unusable',
            text: "Bike parking is inaccessible or unusable"
          },
          {
            key: 'abandoned',
            text: "Report an abandoned bike"
          },
          {
            key: 'vandalized',
            text: "My bike was vandalized"
          },
          {
            key: 'stolen',
            text: "My bike was stolen"
          }
        ]
      }
    ]
  },
  {
    questions: [
      {
        key: 'picture',
        type: contents.PICTURE,
        heading: 'Add a photo',
        text: 'Optional',
        error: 'Picture is wrong format',
        required: false,
      }
    ]
  }, {
    questions: [
      {
        key: 'map',
        type: contents.MAP,
        heading: 'Where was the problem?',
        text: 'Pin the location',
        required: false,
      }
    ]
  }, {
    questions: [
      {
        key: 'happening',
        type: contents.HAPPENING,
        heading: 'When did this happen?',
        subtitle1: 'Date',
        subtitle2 : 'How long did you need to park?',
        error: 'Choose an option',
        required: true,
        values: [
          {
            key: '>1hour',
            text: "Less than 1 hour",
            class: 'half1'
          },
          {
            key: '1-2hours',
            text: "1 to 2 hours",
            class: 'half2'
          },
          {
            key: '4-8hours',
            text: "4 to 8 hours",
            class: 'half1'
          },
          {
            key: 'overnight+',
            text: "Overnight or longer",
            class: 'half2'
          }
        ]
      }
    ]
  }, {
    questions: [
      {
        key: 'summary',
        type: contents.SUMMARY,
        heading: 'Summary',
        required: false,
        final: true

      }
    ]
  },
];

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
        this.questions = questions;
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
                    var questions$$1 = this.questions;
                    console.log(questions$$1);
                    var problems = element.survey.problem_type.reduce((memo, value) => {
                        value = questions$$1[0].questions[0].values.find(entry => entry.key === value);
                        if (value) {
                            memo += '<div class="options"><li><em>' + value.text + '</em></li></div>';
                        }
                        return memo;
                    }, '');
                    var date = element.survey.happening ? new Date(element.survey.happening[0].date).toLocaleString('en-US', { month: 'long', day: 'numeric' }) : '';
                    var clock = element.survey.happening ? new Date(element.survey.happening[0].date).toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true }) : '';
                    var html = '<div class="popup"><h2>Problems</h2>\
                                <div id="problems">'+
                        problems + '\
                                </div>\
                                <div class="linebreak"></div>\
                                <h2>Date and time</h2>\
                                <div class="options third12">\
                                    <li><em id="date">'+ date + '</em></li>\
                                </div>\
                                <div class="options third3">\
                                    <li><em id="clock">'+ clock + '</em></li>\
                                </div>\
                                <div class="linebreak"></div>\
                                <img id="imagePopup" src="/api/pictures/'
                        + element.photo_uri + '">';
                    // make a marker for each feature and add to the map
                    new mapboxgl.Marker(el)
                        .setLngLat([element.longitude, element.latitude])
                        .setPopup(new mapboxgl.Popup({ offset: 25 })
                            .setHTML(html))
                        .addTo(map);



                });
            });

        });

    }
}
new Dashboard();

}());
