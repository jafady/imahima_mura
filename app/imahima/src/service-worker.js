/* eslint-disable-next-line no-redeclare */
/* global self */

self.addEventListener('install', () => self.skipWaiting())

self.addEventListener('activate', () => {
  self.clients.claim();
})

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    // アクションごとの個別処理
    // if (event.action === 'archive') {
    //   console.log('this is archive');
    // } 

    // 指定URLへの遷移
    const host = location.host;
    event.waitUntil(clients.matchAll({ includeUncontrolled: true, type: 'window' }).then(clientsArr => {
      // 対象 URL に一致するウィンドウタブが既に存在する場合は、それにフォーカスして指定ページに遷移する。
      const hadWindowToFocus = clientsArr.some(windowClient => {
        if(windowClient.url.indexOf(host)){
          // serviceworkerのcontroll下にない場合はfocusだけでも行う。
          // その場合navigateの方は実行のエラーになる
          windowClient.focus();
          windowClient.navigate(event.notification.data.url);
          return true;
        }
        return false;
      });
      // それ以外の場合は、適切な URL への新しいタブを開いてフォーカスする。
      if (!hadWindowToFocus) clients.openWindow(event.notification.data.url).then(windowClient => windowClient ? windowClient.focus() : null);
    }));
  }, false);