class LightAjax {
    static token;

    /*
responseType: default "text", "arraybuffer", "blob", "document" (xml), "json"
handleResponse: takes xhr as argument
 */
    static prepareRequest(method, url, handleResponse, responseType) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        if (responseType == null)
            xhr.responseType = "json";
        else
            xhr.responseType = responseType;
        xhr.setRequestHeader('X-CSRFToken', this.token);
        if (handleResponse)
            xhr.onload = function () {
                handleResponse(xhr.status, xhr.response);
            }
        // TODO
        xhr.onerror = function () {
            console.error('request failed: ' + xhr.statusText)
        }
        return xhr;
    }

    static get(url, handleResponse, responseType) {
        let xhr = this.prepareRequest('GET', url, handleResponse, responseType);
        xhr.send();
        return xhr;
    }

    static post(url, payload, handleResponse, responseType) {
        let xhr = this.prepareRequest("POST", url, handleResponse, responseType);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(payload);
        return xhr;
    }

    static file_upload(url, file, handleResponse, handleProgress) {
        let formData = new FormData();
        formData.append('file', file)
        let xhr = this.prepareRequest("POST", url, handleResponse, '');
        // xhr.onloadend = function () {
        //     handleResponse(xhr.status, xhr.response)
        // }
        if (handleProgress)
            xhr.onprogress = function (event) {
                handleProgress(event.loaded, event.total)
            }
        xhr.send(formData);
        return xhr;
    }

    static delete(url, handleResponse, responseType) {
        let xhr = this.prepareRequest('DELETE', url, handleResponse, responseType);
        xhr.send();
        return xhr;
    }

    static patch(url, payload, handleResponse, responseType) {
        let xhr = this.prepareRequest("PATCH", url, handleResponse, responseType);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(payload);
        return xhr;
    }

    static put(url, payload, handleResponse, responseType) {
        let xhr = this.prepareRequest("PUT", url, handleResponse, responseType);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(payload);
        return xhr;
    }
}