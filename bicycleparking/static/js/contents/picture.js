import Content from './content';

export default class Picture extends Content {
  constructor() {
    super(...arguments);
    this.file = null;
    this.values = [];
  }

  get valid() {
    return this.file !== null;
  }

  get value() {
    return this.file;
  }

  bind() {
    this.file = null;
    document.getElementById("buttonRed").addEventListener('click', (event) => {
      document.getElementsByClassName("options")[0].classList.remove('hiddenPicture');
      document.getElementsByClassName("options")[1].classList.remove('hiddenPicture');
      document.getElementById("picture").classList.add('hiddenPicture');
      document.getElementById("buttonRed").classList.add('hiddenPicture');
    });
    document.getElementById("deviceCamera").addEventListener('change', (event) => {
      let files = event.target.files;
      const file = files[0];
      this.file = file;
      var ctx = document.getElementById('picture').getContext('2d');
      var img = new Image;
      img.onload = function () {
        ctx.drawImage(img, 0, 0);
        document.getElementsByClassName("options")[0].classList.add('hiddenPicture');
        document.getElementsByClassName("options")[1].classList.add('hiddenPicture');
        document.getElementById("picture").classList.remove('hiddenPicture');
        document.getElementById("buttonRed").classList.remove('hiddenPicture');

      }
      img.src = URL.createObjectURL(this.file);

    });
    document.getElementById("picture").classList.add('hiddenPicture');
    document.getElementById("buttonRed").classList.add('hiddenPicture');
  }

  get template() {
    return (`
        <div class="screen1">
          <div class="progress prog2"></div>
          <h1>${this.props.heading}</h1>
          <h2>${this.props.text}</h2>
            <ul>
                <div class="doubleoption">
                    <input id="deviceCamera" class="cameraButton" type="file" accept="image/*;capture=camera"/>
                    <div class="imagepreview">
                        <canvas id="picture"/>
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
                <div class="last"></div>
            </ul>            
        </div>
    <footer>
        <div class="nav">
            <div id="buttonRed" class="button red">    
                <p><em>Remove photo</em></p>
            </div>
        </div>
    </footer>
      `
    )
  }
}