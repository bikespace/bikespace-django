import Input from './input';
const URL = '';

export default class ImageInput extends Input {
  constructor() {
    super(...arguments);
    this.file = null;
  }

  bind() {
    document.getElementById('input').addEventListener('change', (event) => {
      let files = event.target.files;
      const file = files[0];
      this.file = file;
    });
  }

  uploadDummy() {
    return new Promise((resolve, reject) => {
      window.setTimeout(() => {
        resolve({url: 'testurl'})
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
    return (`
      <div className="question">
        <input type="file" id="input" />
      </div>
      `
    )
  }
}