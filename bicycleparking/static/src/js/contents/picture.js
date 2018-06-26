import Content from './content';
const pica = require('pica/dist/pica')({ features: ['js', 'ww', 'cib'] })

export default class Picture extends Content {
    constructor() {
        super(...arguments);
        this.dataURL = null;
        this.originalDataURL = null;
        this.values = [];
        this.imageSelected = false;
    }

    get value() {
        this.originalDataURL = document.getElementById('picture').toDataURL();
        this.dataURL = document.getElementById('dst-cvs').toDataURL();
        if (!this.imageSelected) {
            this.originalDataURL = null;
            this.dataURL = null;
        }
        this.values = this.dataURL;
        return this.values;
    }

    bind() {
        this.values = this.getDataFromSession(this.props['key']);
        if (this.originalDataURL) {
            var img = new Image;
            img.onload = function () {
                var src = document.getElementById('picture');
                src.width = img.width;
                src.height = img.height;
                var ctx = src.getContext("2d");
                ctx.drawImage(img, 0, 0);
                document.getElementsByClassName("options")[0].classList.add('hiddenPicture');
                document.getElementsByClassName("options")[1].classList.add('hiddenPicture');
                document.getElementById("picture").classList.remove('hiddenPicture');
                document.getElementById("buttonRed").classList.remove('hiddenPicture');;
                document.getElementById("preview").classList.remove('hiddenPicture');
                document.getElementById("deviceCamera").classList.add('displayNone');
                document.getElementById("pictureText").classList.add('displayNone');
            };
            img.src = this.originalDataURL;
        }
        document.getElementById("buttonRed").addEventListener('click', (event) => {
            document.getElementsByClassName("options")[0].classList.remove('hiddenPicture');
            document.getElementsByClassName("options")[1].classList.remove('hiddenPicture');
            document.getElementById("picture").classList.add('hiddenPicture');
            document.getElementById("preview").classList.add('hiddenPicture');
            document.getElementById("buttonRed").classList.add('hiddenPicture');
            document.getElementById("deviceCamera").classList.remove('displayNone');
            document.getElementById("pictureText").classList.remove('displayNone');
            this.dataURL = null;
            this.originalDataURL = null;
            this.imageSelected = false;
        });

        document.getElementById("deviceCamera").addEventListener('change', (event) => {
            var img = new Image();
            img.onload = function () {
                document.getElementsByClassName("options")[0].classList.add('hiddenPicture');
                document.getElementsByClassName("options")[1].classList.add('hiddenPicture');
                document.getElementById("picture").classList.remove('hiddenPicture');
                document.getElementById("buttonRed").classList.remove('hiddenPicture');;
                document.getElementById("preview").classList.remove('hiddenPicture');


                var src = document.getElementById('picture');
                src.width = img.width;
                src.height = img.height;

                var ctx = src.getContext("2d");
                ctx.drawImage(img, 0, 0);

                var dst = document.getElementById('dst-cvs');
                dst.width = 300;
                dst.height = img.height * dst.width / img.width;

                ctx = dst.getContext("2d")
                ctx.drawImage(img, 0, 0, dst.width, dst.height);
                document.getElementById("deviceCamera").classList.add('displayNone');
                document.getElementById("pictureText").classList.add('displayNone');
            }

            img.src = window.URL.createObjectURL(event.target.files[0]);
            this.imageSelected = true;
        });

        document.getElementById("picture").classList.add('hiddenPicture');
        document.getElementById("buttonRed").classList.add('hiddenPicture');
        document.getElementById("preview").classList.add('hiddenPicture');

    }

    get template() {
        return (`
        <div class="screen1 visible">
          <div class="progLine"><div class="progress prog4"></div></div>
          <h1>${this.props.heading}</h1>
          <h2 id="pictureText" class="">${this.props.text}</h2>
            <ul>
                <div class="doubleoption">
                    <input id="deviceCamera" class="cameraButton" type="file" accept="image/*;capture=camera"/>
                    <div id="preview" class="imagepreview hiddenPicture">
                        <canvas id="picture" src="#" ></canvas>
                        <canvas id="dst-cvs" class="img-responsive"></canvas>
                    </div>
                    <div class="options">
                        <li><em>Camera</em></li>
                        <div class="check camera"> </div>
                    </div>
                    <div class="options">
                        <li><em>Upload</em></li>
                        <div class="check upload"> </div>
                    </div>
                </div>
            </ul>
        </div>
            <footer>
            <div class="nav">
                <div id="buttonRed" class="button red">
                    <p><em>Remove photo</em></p>
                </div>
            </div>
        </footer>  
        </div>
      `
        )
    }
}