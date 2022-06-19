/* eslint-disable-next-line no-redeclare */
/* global self */


// 未使用のため骨格だけ残しておく
// クライアントからのアクセスの制御
// self.addEventListener('message', event => {
//   // event は ExtendableMessageEvent オブジェクト
//   console.log(`The client sent me a message: ${event.data}`);
//   if(event.data.type == "connectWebsocket" ){
//     // 何か処理
//   }
// });


// fetch
async function fetchGetData(url = "", data = {}) {
  // 既定のオプションには * が付いています
  const baseURL = VUE_APP_API_ENDPOINT_PROTOCOL +"://"+ VUE_APP_API_ENDPOINT_HOST+"/";
  const response = await fetch(baseURL + url, {
    method: "GET", // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    },
  })
  return response.json(); // JSON のレスポンスをネイティブの JavaScript オブジェクトに解釈
}
async function fetchPostData(url = "", data = {}) {
  // 既定のオプションには * が付いています
  const baseURL = VUE_APP_API_ENDPOINT_PROTOCOL +"://"+ VUE_APP_API_ENDPOINT_HOST+"/";
  const response = await fetch(baseURL + url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data) // 本文のデータ型は "Content-Type" ヘッダーと一致させる必要があります
  })
  return response.json(); // JSON のレスポンスをネイティブの JavaScript オブジェクトに解釈
}


// 通知メッセージの受信
self.addEventListener('push', function(event) {  
  const response_json = event.data.json();
  if(response_json.type == "incleaseMembersNotice"){
    noticeOnlineMembers(response_json);
  }
  if(response_json.type == "receiveCreateEvent"){
    receiveCreateEvent(response_json);
  }
  if(response_json.type == "receiveManualMessage"){
    receiveManualMessage(response_json);
  }
  if(response_json.type == "receiveNewTalk"){
    receiveNewTalk(response_json);
  }

});


// 通知チェック
const checkNoticePermission =  async () =>{
  // 通知許可チェック
  if (Notification.permission === "granted") {
      return true;
  }else{
      // 許可はserviceworkerでは聞けないので、諦める
      return false;
  }
}


const noticeOnlineMembers = async (data) => {
  // 2人以上になったよの通知
  // 通知しつつ次の通知のインターバルを設定する。

  // 通知許可チェック
  const permission = await checkNoticePermission();
  if(!permission) return;

  const img = "../img/serviceWorker/app_icon.png";
  const text = data.count + "人ヒマな人がいます。";
  const options = {
      tag: "noticeOnlineMembers",
      icon: img,
      body: text,
      actions: [
          {action: 'enterRoom', title: "入る"}
          ],
      data: {
          baseUrl: self.location.origin,
          url: "/?#/House?houseId=" + data.houseId,
      }
  }
  registration.showNotification("ヒマですか？", options);
}

const receiveCreateEvent = async (data) => {
  // 指名されての通知
  // サーバ側で条件確認をしているのでここでは出すだけ。

  // 通知許可チェック
  const permission = await checkNoticePermission();
  if(!permission) return;

  const img = "../img/serviceWorker/app_icon.png";
  const title = "新しいお誘い";
  const msg = data.eventName + "  のお誘いが来ました";
  const options = {
      tag: "noticeCreateEvent",
      icon: img,
      body: msg,
      actions: [
          {action: 'lookEvent', title: "イベントを確認する"},
          {action: 'joinEvent', title: "参加する!"}
          ],
      data: {
          baseUrl: self.location.origin,
          url: "/?#/House?houseId=" + data.houseId + "&eventId=" + data.eventId,
          eventId: data.eventId,
          userId: data.userId,
      }
  }
  
  // 通知時間まで待つ
  setTimeout(() =>{registration.showNotification(title, options)}, data.noticeSecond * 1000);
}

const receiveManualMessage = async (data) => {
  // 指名されての通知
  // サーバ側で条件確認をしているのでここでは出すだけ。

  // 通知許可チェック
  const permission = await checkNoticePermission();
  if(!permission) return;

  const img = "../img/serviceWorker/app_icon.png";
  const title = data.userName + "  " + data.eventName;
  const options = {
      tag: "noticeManualMessage",
      icon: img,
      body: data.msg,
      actions: [
          {action: 'lookEvent', title: "イベントを確認する"}
          ],
      data: {
          baseUrl: self.location.origin,
          url: "/?#/House?houseId=" + data.houseId + "&eventId=" + data.eventId,
      }
  }
  
  // 通知時間まで待つ
  setTimeout(() =>{registration.showNotification(title, options)}, data.noticeSecond * 1000);
}

const receiveNewTalk = async (data) => {
  // 通知許可チェック
  const permission = await checkNoticePermission();
  if(!permission) return;

  const img = "../img/serviceWorker/app_icon.png";
  const title = data.userName;
  const options = {
      tag: "noticeNewTalk",
      icon: img,
      body: data.msg,
      actions: [
          {action: 'enterRoom', title: "入る"}
      ],
      data: {
          baseUrl: self.location.origin,
          url: "/?#/House?houseId=" + data.houseId,
      }
  }
  registration.showNotification(title, options);
}



// 受信時
const joinEvent = async (data) => {
  // イベント参加
  const sendData = {
    eventId: data.eventId,
    userId: data.userId,
  }
  await fetchPostData("api/join_event/",sendData);
}