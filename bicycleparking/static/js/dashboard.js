
const TOKEN = 'pk.eyJ1IjoidGVzc2FsdCIsImEiOiJjajU0ZGk4OTQwZDlxMzNvYWgwZmY4ZjJ2In0.zhNa8fmnHmA0d9WKY1aTjg';

import questions from './survey-questions';

class Dashboard {

    constructor() {
        console.log('Start dashboard ...')
        mapboxgl.accessToken = TOKEN
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
                    var questions = this.questions;
                    console.log(questions)
                    var problems = element.survey.problem_type.reduce((memo, value) => {
                        value = questions[0].questions[0].values.find(entry => entry.key === value)
                        if (value) {
                            memo += '<div class="options"><li><em>' + value.text + '</em></li></div>'
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
                        + element.photo_uri + '">'
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