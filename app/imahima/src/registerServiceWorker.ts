/* eslint-disable no-console */

import { register } from 'register-service-worker'

import Axios, {AxiosRequestConfig} from 'axios'
Axios.defaults.baseURL = process.env.VUE_APP_API_ENDPOINT_PROTOCOL +"://"+process.env.VUE_APP_API_ENDPOINT_HOST+"/";
Axios.interceptors.request.use((config: AxiosRequestConfig) => {
    if(config.headers && localStorage.getItem('token')){
        config.headers.Authorization = "Token " + localStorage.getItem('token')
    }
    return config
});


// サービスワーカーを更新させるための無意味な式(変更した場合はバージョンを繰り上げること)
const version = 3;
const dev_version = 1;

// Utils functions:

function urlBase64ToUint8Array (base64String:any) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  const base64 = (base64String + padding)
          .replace(/-/g, '+')
          .replace(/_/g, '/')

  const rawData = window.atob(base64)
  const outputArray = new Uint8Array(rawData.length)

  for (let i = 0; i < rawData.length; ++i) {
          outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray;
}

function loadVersionBrowser () {
  if ("userAgentData" in navigator) {
          // navigator.userAgentData is not available in
          // Firefox and Safari
          const uaData = navigator.userAgentData;
          // Outputs of navigator.userAgentData.brands[n].brand are e.g.
          // Chrome: 'Google Chrome'
          // Edge: 'Microsoft Edge'
          // Opera: 'Opera'
          let browsername;
          let browserversion;
          let chromeVersion = null;
          for (let i = 0; i < uaData.brands.length; i++) {
                  const brand = uaData.brands[i].brand;
                  browserversion = uaData.brands[i].version;
                  if (brand.match(/opera|chrome|edge|safari|firefox|msie|trident/i) !== null) {
                          // If we have a chrome match, save the match, but try to find another match
                          // E.g. Edge can also produce a false Chrome match.
                          if (brand.match(/chrome/i) !== null) {
                                  chromeVersion = browserversion;
                          }
                          // If this is not a chrome match return immediately
                          else {
                                  browsername = brand.substr(brand.indexOf(' ')+1);
                                  return {
                                          name: browsername,
                                          version: browserversion
                                  }
                          }
                  }
          }
          // No non-Chrome match was found. If we have a chrome match, return it.
          if (chromeVersion !== null) {
                  return {
                          name: "chrome",
                          version: chromeVersion
                  }
          }
  }
  // If no userAgentData is not present, or if no match via userAgentData was found,
  // try to extract the browser name and version from userAgent
  const userAgent = navigator.userAgent;
  const ua = userAgent;
  let tem, M = ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
  if (/trident/i.test(M[1])) {
          tem = /\brv[ :]+(\d+)/g.exec(ua) || [];
          return {name: 'IE', version: (tem[1] || '')};
  }
  if (M[1] === 'Chrome') {
          tem = ua.match(/\bOPR\/(\d+)/);
          if (tem != null) {
                  return {name: 'Opera', version: tem[1]};
          }
  }
  M = M[2] ? [M[1], M[2]] : [navigator.appName, navigator.appVersion, '-?'];
  if ((tem = ua.match(/version\/(\d+)/i)) != null) {
          M.splice(1, 1, tem[1]);
  }
  return {
          name: M[0],
          version: M[1]
  };
}

const applicationServerKey = process.env.VUE_APP_WEBPUSH_APPSERVERKEY
// Utils functionsおわり


// service-worker登録処理
if (process.env.NODE_ENV === 'production') {
  register(`${process.env.BASE_URL}service-worker.js`, {
    ready () {
      console.log(
        'App is being served from cache by a service worker.\n' +
        'For more details, visit https://goo.gl/AFskqB'
      )
    },
    registered () {
      console.log('Service worker has been registered.')
    },
    cached () {
      console.log('Content has been cached for offline use.')
    },
    updatefound () {
      console.log('New content is downloading.')
    },
    updated () {
      console.log('New content is available; please refresh.')
    },
    offline () {
      console.log('No internet connection found. App is running in offline mode.')
    },
    error (error) {
      console.error('Error during service worker registration:', error)
    }
  })
  navigator.serviceWorker.ready.then((registration) => {
    registration.update();
//     registration.pushManager.getSubscription().then(function(subscription) {
//         subscription?.unsubscribe().then(function(successful) {
//           // 登録解除が成功
//         }).catch(function(e) {
//           // 登録解除が失敗
//         })
//       });
    registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(applicationServerKey)
    }).then(function (sub) {
      const browser = loadVersionBrowser();
      const endpointParts = sub.endpoint.split('/');
      const registration_id = endpointParts[endpointParts.length - 1];
      const p256dh = sub.getKey('p256dh') || new ArrayBuffer(0);
      const auth = sub.getKey('auth') || new ArrayBuffer(0);
      const data = {
              'browser': browser.name.toUpperCase(),
              'p256dh': btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(p256dh)))),
              'auth': btoa(String.fromCharCode.apply(null, Array.from(new Uint8Array(auth)))),
              'registration_id': registration_id
      };
      // requestPOSTToServer(data);
      Axios.post("/api/regist_webpush/",data);
    })
  });
}

