let lst = document.getElementsByClassName('switch')
for (let btn of lst) {
    btn.addEventListener('click', () => {
        if (window.XMLHttpRequest) { // Mozilla, Safari, ...
            httpRequest = new XMLHttpRequest();
            if (httpRequest.overrideMimeType) {
                httpRequest.overrideMimeType('text/xml');
                // Читайте ниже об этой строке
            }
        } else if (window.ActiveXObject) { // IE
            try {
                httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) {}
            }
        }
        if ('on' in btn.classList) {
            console.log('hello')
            httpRequest.onreadystatechange = () => {
                if (httpRequest.readyState == 4) {
                    if (httpRequest.status == 200) {
                        btn.classList.remove('on');
                        btn.classList.add('off');
                    } else {
                        alert('С запросом возникла проблема.');
                    }
                }
            };
            url = document.location.origin + "/on?name=" + btn.id  
        }
        else {
            console.log('by')
            httpRequest.onreadystatechange = () => {
                if (httpRequest.readyState == 4) {
                    if (httpRequest.status == 200) {
                        btn.classList.add('on');
                        btn.classList.remove('off');
                    } else {
                        alert('С запросом возникла проблема.');
                    }
                }
            };
            url = document.location.origin + "/on?name=" + btn.id;
        }
        httpRequest.open('POST', url, true);
        httpRequest.send(null);
    })
}