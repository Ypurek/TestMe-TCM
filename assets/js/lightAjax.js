class LightAjax {
    static token;

    /*
responseType: default "text", "arraybuffer", "blob", "document" (xml), "json"
handleResponse: takes xhr as argument
 */
    static #prepareRequest(method, url, handleResponse, responseType) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        if (responseType == null)
            xhr.responseType = "json";
        else
            xhr.responseType = responseType;
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', this.token);
        xhr.onload = function () {
            handleResponse(xhr.status, xhr.response);
        }
        xhr.onerror = function () {
            console.error('request failed: ' + xhr.statusText)
        }
        return xhr;
    }

    static get(url, handleResponse, responseType) {
        let xhr = this.#prepareRequest('GET', url, handleResponse, responseType);
        xhr.send();
    }

    static post(url, payload, handleResponse, responseType) {
        let xhr = this.#prepareRequest("POST", url, handleResponse, responseType);
        xhr.send(payload);
    }

    static delete(url, handleResponse, responseType) {
        let xhr = this.#prepareRequest('DELETE', url, handleResponse, responseType);
        xhr.send();
    }

    static patch(url, payload, handleResponse, responseType) {
        let xhr = this.#prepareRequest("PATCH", url, handleResponse, responseType);
        xhr.send(payload);
    }

    static put(url, payload, handleResponse, responseType) {
        let xhr = this.#prepareRequest("PUT", url, handleResponse, responseType);
        xhr.send(payload);
    }
}