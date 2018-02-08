import Input from './input';
const URL = '';

export default class ImageInput extends Input {
  constructor() {
    super(...arguments);
    this.file = null;
  }

  bind() {
    document.getElementById(this.props.key).addEventListener('change', (event) => {
      let files = event.target.files;
      const file = files[0];
      this.file = file;
    });
  }

  uploadDummy() {
    return new Promise((resolve, reject) => {
      window.setTimeout(() => {
        resolve({ url: 'testurl' })
      }, 1000);
    })
  }

  get value() {
    return this.file;
  }

  upload() {
    return new Promise((resolve, reject) => {
      let formData = new FormData();
      let xhr = new XMLHttpRequest();

      formData.append(this.props.key, this.file, this.file.name);

      xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
          if (xhr.status === 200) {
            resolve(JSON.parse(xhr.response));
          } else {
            reject(xhr.response);
          }
        }
      };

      xhr.open('POST', URL, true);
      xhr.send(formData);
    });
  }

  get template() {
    const heading = this.props.heading ? `<h4>${this.props.heading}</h4>` : '';
    return (`
      <div class="file-field input-field">
        ${heading}
        <div class="btn">
          <span>Picture</span>
          <input id="${this.props.key}" type="file" accept="image/*;capture=camera">
        </div>
        <div class="file-path-wrapper">
          <input class="file-path validate" type="text">
        </div>
      </div>
      `
    )
  }
}