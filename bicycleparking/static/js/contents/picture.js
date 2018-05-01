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
      document.getElementById("preview").classList.add('hiddenPicture');
      document.getElementById("buttonRed").classList.add('hiddenPicture');
    });
    document.getElementById("deviceCamera").addEventListener('change', (event) => {
      let files = event.target.files;
      const file = files[0];
      this.file = file;
      var reader = new FileReader();

      reader.onload = function (e) {
        document.getElementById('picture').src = e.target.result
        document.getElementsByClassName("options")[0].classList.add('hiddenPicture');
        document.getElementsByClassName("options")[1].classList.add('hiddenPicture');
        document.getElementById("picture").classList.remove('hiddenPicture');
        document.getElementById("buttonRed").classList.remove('hiddenPicture');;
        document.getElementById("preview").classList.remove('hiddenPicture');
      }
      reader.readAsDataURL(file);


    });
    document.getElementById("picture").classList.add('hiddenPicture');
    document.getElementById("buttonRed").classList.add('hiddenPicture');
    document.getElementById("preview").classList.add('hiddenPicture');

    function getOrientation(file, callback) {
      var reader = new FileReader();
      reader.onload = function (e) {

          var view = new DataView(e.target.result);
          if (view.getUint16(0, false) != 0xFFD8) {
              return callback(-2);
          }
          var length = view.byteLength, offset = 2;
          while (offset < length) {
              if (view.getUint16(offset + 2, false) <= 8) return callback(-1);
              var marker = view.getUint16(offset, false);
              offset += 2;
              if (marker == 0xFFE1) {
                  if (view.getUint32(offset += 2, false) != 0x45786966) {
                      return callback(-1);
                  }

                  var little = view.getUint16(offset += 6, false) == 0x4949;
                  offset += view.getUint32(offset + 4, little);
                  var tags = view.getUint16(offset, little);
                  offset += 2;
                  for (var i = 0; i < tags; i++) {
                      if (view.getUint16(offset + (i * 12), little) == 0x0112) {
                          return callback(view.getUint16(offset + (i * 12) + 8, little));
                      }
                  }
              }
              else if ((marker & 0xFF00) != 0xFF00) {
                  break;
              }
              else {
                  offset += view.getUint16(offset, false);
              }
          }
          return callback(-1);
      };
      reader.readAsArrayBuffer(file);
    }

    function resizeAndResetOrientation(srcBase64, srcOrientation, callback) {
      var img = new Image();

      img.onload = function () {
          var MAX_WIDTH = 800;
          var MAX_HEIGHT = 600;

          var width = img.width,
              height = img.height,
              canvas = document.createElement('canvas'),
              ctx = canvas.getContext("2d");

          if (width > height) {
              if (width > MAX_WIDTH) {
                  height *= MAX_WIDTH / width;
                  width = MAX_WIDTH;
              }
          } else {
              if (height > MAX_HEIGHT) {
                  width *= MAX_HEIGHT / height;
                  height = MAX_HEIGHT;
              }
          }

          // set proper canvas dimensions before transform & export
          if (4 < srcOrientation && srcOrientation < 9) {
              canvas.width = height;
              canvas.height = width;
          } else {
              canvas.width = width;
              canvas.height = height;
          }

          // transform context before drawing image
          switch (srcOrientation) {
              case 2:
                  ctx.transform(-1, 0, 0, 1, width, 0);
                  break;
              case 3:
                  ctx.transform(-1, 0, 0, -1, width, height);
                  break;
              case 4:
                  ctx.transform(1, 0, 0, -1, 0, height);
                  break;
              case 5:
                  ctx.transform(0, 1, 1, 0, 0, 0);
                  break;
              case 6:
                  ctx.transform(0, 1, -1, 0, height, 0);
                  break;
              case 7:
                  ctx.transform(0, -1, -1, 0, height, width);
                  break;
              case 8:
                  ctx.transform(0, -1, 1, 0, 0, width);
                  break;
              default:
                  break;
          }

          // draw image
          ctx.drawImage(img, 0, 0, width, height);

          // export base64
          callback(canvas.toDataURL());
      };

      img.src = srcBase64;
    };

    // usage
    var input = document.getElementById('deviceCamera');
    input.onchange = function (e) {
      getOrientation(input.files[0], function (orientation) {
          var image = document.getElementById('picture');
          resizeAndResetOrientation(image.src, orientation, function (resetBase64Image) {
              image.src = resetBase64Image;
          });
      });
    }
  }

  get template() {
    return (`
        <div class="screen1 visible">
          <div class="progress prog2"></div>
          <h1>${this.props.heading}</h1>
          <h2>${this.props.text}</h2>
            <ul>
                <div class="doubleoption">
                    <input id="deviceCamera" class="cameraButton" type="file" accept="image/*;capture=camera"/>
                    <div id="preview" class="imagepreview hiddenPicture">
                        <img id="picture" src="#" />
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
      `
    )
  }
}