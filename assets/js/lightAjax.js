class LightAjax {
    constructor(token) {
        this.xhr = new XMLHttpRequest();
        this.xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', token);
    }

    get(url) {
        this.xhr.open('GET', url);
        this.xhr.send()
    }

    post(url, payload) {
        this.xhr.open("POST", url);
        xhr.send(JSON.stringify(payload));
    }
}
