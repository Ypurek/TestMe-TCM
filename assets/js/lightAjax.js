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

// <script>
//     // code from https://developers.google.com/web/fundamentals/native-hardware/user-location?hl=ru&authuser=0
//     $(document).ready(function () {
//         if (navigator.geolocation) {
//             console.log('Geolocation is supported!');
//         } else {
//             console.error('Geolocation is not supported for this Browser/OS version yet.');
//         }
//         ;
//         let geoOptions = {
//             maximumAge: 5 * 60 * 1000,
//         }
//         let geoSuccess = function (position) {
//             let x = Number(position.coords.latitude).toFixed(3);
//             let y = Number(position.coords.longitude).toFixed(3);
//             console.log('latitude ' + x + 'longitude ' + y);
//             $('.latitude').text(x);
//             $('.longitude').text(y);
//
//         };
//         let geoError = function (position) {
//             let message = ''
//             switch (position.code) {
//                 case 0:
//                     message = 'unknown error';
//                     break;
//                 case 1:
//                     message = 'permission denied';
//                     break;
//                 case 2:
//                     message = 'position unavailable';
//                     break;
//                 case 3:
//                     message = 'timeout';
//                     break;
//                 default:
//                     message = 'shit happened'
//             }
//             console.error('Error occurred: ' + message);
//         };
//         navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
//     })
//
// </script>

