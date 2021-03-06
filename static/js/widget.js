function loadOrganizeIframe() {
    var iframeTag = document.createElement('iframe');
    iframeTag.setAttribute('id', 'organize_iframe');
    // Support for cobranding over widget
    if (typeof organizeBrandId !== 'undefined' && organizeBrandId !== '') {
        iframeTag.setAttribute('src', 'https://register.organize.org/?cobrand_id=' + organizeBrandId);
    }
    else {
        iframeTag.setAttribute('src', 'https://register.organize.org/?widget_id=' + organizeWidgetId);
    }
    iframeTag.setAttribute('class', 'organize-iframe');
    iframeTag.setAttribute('width', '100%');
    iframeTag.setAttribute('height', '100%');

    document.getElementById('organize_modal_content').appendChild(iframeTag);
    document.getElementById('organize_modal').setAttribute('class', 'organize-modal organize-modal-opened');
}

function closeOrganizeIframe() {
    document.getElementById('organize_modal').setAttribute('class', 'organize-modal');
    document.getElementById('organize_modal_content').removeChild(document.getElementById('organize_iframe'));
}

function popupWindow() {
    url = 'https://register.organize.org/?widget_id=' + organizeWidgetId;
    // Support for cobranding over widget
    if (typeof organizeBrandId !== 'undefined' && organizeBrandId !== '') {
        url = 'https://register.organize.org/?cobrand_id=' + organizeBrandId;
    }
    title = 'ORGANIZE / Register to become an organ donor'
    h = screen.height - screen.height * 0.3;
    w = screen.width - screen.width * 0.3;
    wLeft = (window.screenLeft ? window.screenLeft : window.screenX) + (screen.width - w) / 2;
    wTop = (window.screenTop ? window.screenTop : window.screenY) + (screen.height - h) / 2;

    //var left = wLeft + (window.innerWidth / 2) - (w / 2);
    //var top = wTop + (window.innerHeight / 2) - (h / 2);
    return window.open(url, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=no, copyhistory=no, width=' + w + ', height=' + h + ', top=' + wTop + ', left=' + wLeft);
}

(function() {
    var isMobile = false;
    // device detection
    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || screen.width <= 480)
    {
        isMobile = true;
    }

    var linkTag = document.createElement('link');
    linkTag.setAttribute('rel', 'stylesheet');
    linkTag.setAttribute('href', '//db9ziq0aoct85.cloudfront.net/static/css/modal.css');
    linkTag.setAttribute('type', 'text/css');
    document.getElementsByTagName('head')[0].appendChild(linkTag);

    var organizeRegistrationBtnTag = document.createElement('div');

    if (isMobile == false)
    {
        if (typeof organizeAlwaysOpenInPage === 'undefined' || organizeAlwaysOpenInPage == true) {
            if (window != window.top) {
                organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: popupWindow();');
            }
            else if (window.location.protocol != 'https:') {
                organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: popupWindow();');
            }
            else {
                var organizeModalDivTag = document.createElement('div');
                organizeModalDivTag.setAttribute('id', 'organize_modal');
                organizeModalDivTag.setAttribute('class', 'organize-modal');


                var organizeModalContentDivTag = document.createElement('div');
                organizeModalContentDivTag.setAttribute('class', 'organize-modal-content');
                organizeModalContentDivTag.setAttribute('id', 'organize_modal_content');

                var organizeModalCloseDivTag = document.createElement('div');
                organizeModalCloseDivTag.setAttribute('onclick', 'javascript: closeOrganizeIframe()');
                organizeModalCloseDivTag.setAttribute('class', 'organize-close');
                organizeModalCloseDivTag.innerHTML = '&times;';

                organizeModalContentDivTag.appendChild(organizeModalCloseDivTag);
                organizeModalDivTag.appendChild(organizeModalContentDivTag);

                document.getElementsByTagName('body')[0].appendChild(organizeModalDivTag);

                organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: loadOrganizeIframe();');
            }
        }
        else {
            organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: popupWindow();');
        }
    }
    else
    {
        // Support for cobranding over widget
        if (typeof organizeBrandId !== 'undefined' && organizeBrandId !== '') {
            organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: window.open(\'https://register.organize.org/?cobrand_id=' + organizeBrandId + '\');');
        }
        else {
            organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: window.open(\'https://register.organize.org/?widget_id=' + organizeWidgetId + '\');');
        }
    }

    organizeRegistrationBtnTag.setAttribute('class', 'organize-registration-btn');
    organizeRegistrationBtnTag.setAttribute('id', 'organize_registration_btn');
    var widgetChoiceImagePath = "//db9ziq0aoct85.cloudfront.net/static/images/widget/" + organizeWidgetChoice + ".png";
    organizeRegistrationBtnTag.innerHTML = '<img style="height: 100%;border:1px solid #021a40;" src="' + widgetChoiceImagePath + '"/>';

    organizeScriptNode = document.getElementById('organize_widget_script');
    parentNode = organizeScriptNode.parentNode;

    parentNode.insertBefore(organizeRegistrationBtnTag, organizeScriptNode);

})();



