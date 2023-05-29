
function getCookieValue(key) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        const [name, value] = cookie.split('=');
        if (name === key) {
            return value;
        }
    }
    return null;
}

function setCookie(name, value, seconds) {
    var max_age = "";
    if (seconds) {
        max_age = "; max-age=" + seconds;
        console.log(max_age)
    }
    console.log(name + "=" + (value || "") + max_age + ";")
    document.cookie = name + "=" + (value || "") + max_age + ";";
}



const userAgent = navigator.userAgent;

let deviceType;
if (/iPhone|iPad|iPod/i.test(userAgent)) {
  deviceType = 'iOS';
} else if (/Android/i.test(userAgent)) {
  deviceType = 'Android';
} else if (/Windows Phone/i.test(userAgent)) {
  deviceType = 'Windows Phone';
} else if (/Windows/i.test(userAgent)) {
  deviceType = 'Windows';
} else if (/Macintosh/i.test(userAgent)) {
  deviceType = 'Macintosh';
} else if (/Linux/i.test(userAgent)) {
  deviceType = 'Linux';
} else {
  deviceType = 'Unknown';
}
const browserType = userAgent.match(/Chrome|Firefox|Safari|Edge|Opera/i)[0];

let osType;
if (/Windows/.test(userAgent)) {
  osType = 'Windows';
} else if (/Mac OS/.test(userAgent)) {
  osType = 'macOS';
} else if (/Linux/.test(userAgent)) {
  osType = 'Linux';
} else if (/Android/.test(userAgent)) {
  osType = 'Android';
} else if (/iOS/.test(userAgent)) {
  osType = 'iOS';
} else {
  osType = 'Unknown';
}

const language = navigator.language || navigator.userLanguage;

const referer = window.location.hostname;
let ipAddress = null; // Use a third-party API to get the IP address
fetch('https://api.db-ip.com/v2/free/self')
  .then(response => response.json())
  .then(data => {
    const ipAddress = data.ipAddress;
    // Create data object
    const metadata = {
      'referer': referer,
      'device_type': deviceType,
      'browser_type': browserType,
      'user_agent': userAgent,
      'os_type': osType,
      'ip': ipAddress,
      'language': language.slice(0, 2),
      'created_at': new Date().toISOString(),
      visitor_unique_key: getCookieValue("unique_key"),
      visit_id: getCookieValue("visit_id")
    };

const csrftoken = getCookieValue('csrftoken');
const xhr = new XMLHttpRequest();

xhr.onreadystatechange = function() {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    if (xhr.status === 200) {
      const response = JSON.parse(xhr.responseText);
      const unique_key = response.unique_key;
      const visit_id = response.visit_id;
      setCookie('unique_key', unique_key);
      setCookie('visit_id', visit_id, 1800);
    } else {
      console.log('Error sending data: ' + xhr.status);
    }
  }
};

let counter = document.getElementById("counter_id"); // получить элемент с идентификатором "counter_id"
let value = counter.textContent; // получить текстовое значение элемента
console.log(value)
xhr.open('POST', `https://site-stats.ya.uenv.ru/api/getmetadata/${value}`);
xhr.setRequestHeader('X-CSRFToken', csrftoken);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send(JSON.stringify(metadata));

});


