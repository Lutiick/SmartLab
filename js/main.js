let lst = document.getElementsByClassName('switch')
for (let btn of lst) {
    btn.addEventListener('click', () => {
        if (window.XMLHttpRequest) {
            httpRequest = new XMLHttpRequest();
            if (httpRequest.overrideMimeType) {
                httpRequest.overrideMimeType('text/xml');
            }
        } else if (window.ActiveXObject) {
            try {
                httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                try {
                    httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e) {}
            }
        }
        if ('on' in btn.classList) {
            httpRequest.onreadystatechange = () => {
                if (httpRequest.readyState == 4) {
                    if (httpRequest.status == 200) {
                        btn.classList.remove('on');
                        btn.classList.add('off');
                    } else {
                        
                    }
                }
            };
            url = document.location.origin + "/on?name=" + btn.id  
        }
        else {
            httpRequest.onreadystatechange = () => {
                if (httpRequest.readyState == 4) {
                    if (httpRequest.status == 200) {
                        btn.classList.add('on');
                        btn.classList.remove('off');
                    } else {

                    }
                }
            };
            url = document.location.origin + "/on?name=" + btn.id;
        }
        httpRequest.open('POST', url, true);
        httpRequest.send(null);
    })
}