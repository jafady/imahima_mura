/* eslint-disable-next-line no-redeclare */
/* global self */

const state = {
  userId: "",
  userToken: "",
  userStatus: "hima",
  websocket: null,
  noticeIntervalMinOM: 10,
  latestNoticeData: {},
}

const STATUS = {
  hima: "ヒマ",
  maybe: "予定ではヒマ",
  busy: "ヒマじゃない",
  ongame: "ゲーム中"
}

// クライアントからのアクセスの制御
self.addEventListener('message', event => {
  // event は ExtendableMessageEvent オブジェクトです
  console.log(`The client sent me a message: ${event.data}`);
  if(event.data.type == "connectWebsocket" ){
    state.userToken = event.data.token || state.userToken;
    state.userId = event.data.userId || state.userId;
    connectWebsocket(event.data);
  }
  if(event.data.type == "addConnect" ){
    addConnect(event.data.houseId);
  }
  if(event.data.type == "disconnectWebsocket" ){
    state.websocket.close();
  }
});


// ステータスの名前変換
const getStatusByName = function(data){
  const statuses = STATUS;
  const result = Object.keys(statuses).filter((key) => { 
      return statuses[key] === data
  }).shift();
  return result || ""
}

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
      'Content-Type': 'application/json',
      'Authorization': "Token " + state.userToken
    },
    // redirect: 'follow', // manual, *follow, error
    // referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    // body: JSON.stringify(data) // 本文のデータ型は "Content-Type" ヘッダーと一致させる必要があります
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
      'Content-Type': 'application/json',
      'Authorization': "Token " + state.userToken
    },
    // redirect: 'follow', // manual, *follow, error
    // referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // 本文のデータ型は "Content-Type" ヘッダーと一致させる必要があります
  })
  return response.json(); // JSON のレスポンスをネイティブの JavaScript オブジェクトに解釈
}

const waitWSConnection = (callback, interval) => {
  const ws = state.websocket;
  if (!ws) return;
  if (ws.readyState === 1) {
    callback();
  } else {
      // optional: implement backoff for interval here
      setTimeout(function () {
        waitWSConnection(callback, interval);
      }, interval);
  }
}

const sendWebsocket = (message) => {
  waitWSConnection(()=>{
    state.websocket?.send(message);
  }, 1000);
}



// websocket接続
const connectWebsocket = (data) => {
  if(data.token == null || state.websocket != null) {
    return;
  }
  const token = data.token;
  const socket = new WebSocket(
      VUE_APP_WEBSOCKET_ENDPOINT_PROTOCOL
      + "://"
      + VUE_APP_API_ENDPOINT_HOST
      + "/ws/imahima/"
      + "?token="
      + token
  );
  socket.onmessage = (e)=>{
      const data = JSON.parse(e.data);
      if(data.type == "someOneChangeStatus"){
        someOneChangeStatus(data);
      }
      if(data.type == "receiveCreateEvent"){
        receiveCreateEvent(data);
      }
      if(data.type == "receiveManualMessage"){
        receiveManualMessage(data);
      }
  }
  socket.onclose = (e) => {
      console.error("Chat socket closed unexpectedly");
      connectWebsocket();
  }
  state.websocket = socket;
}

const addConnect = (houseId) =>{
  sendWebsocket(JSON.stringify({
    "type": "addConnect",
    "houseId": houseId,
  }));
}


// 通知チェック
const checkNoticePermission =  async () =>{
  // 通知許可チェック
  if (Notification.permission === "granted") {
      return true;
  }else{
      // 許可されてないので許可を依頼する
      const result = await Notification.requestPermission();
      return result === "granted";
  }
}

// 通知制御
const someOneChangeStatus =  async (data) =>{
  // 誰かがステータス更新した。
  // ステータス情報をカウントして通知出すかを判断する

  const res = await checkCanNoticeOnlineMembers(data);
  // 通知の開発時には一時的にコメントアウトする
  if (!res){
      return
  }

  // 人数チェック & 人数増加チェック(規定時間ごとの確認のため)
  // houseIdを基に問い合わせ。人数チェックする
  const houseId = data.houseId;
  let himaCount = 0;
  await fetchGetData("api/users/" + houseId + "/").then((response) => {
    const res = response
    for (const key in res) {
      if (getStatusByName(res[key].nowStatus) == "hima") {
        himaCount += 1;
      }
    }
  });

  if(himaCount < 2 || state.latestNoticeData[houseId].latestNoticeHouseMatesNumOM >= himaCount) {
      return;
  }

  noticeOnlineMembers({
      houseId:houseId,
      count:himaCount
  });
}

const checkCanNoticeOnlineMembers = async (data) => {
  // 誰かの更新の際に全員分取り直しているので、自分含めて最新を持っているはず。
  // 人数チェック(人数を通知に使うのでこれは別口で。)
  // 増えた時だけ通知
  if(data.status != "hima"){
      return false;
  }

  // 自分のステータスチェック(予定ではヒマとヒマに送る)
  let myStatus = "hima";
  await fetchGetData("api/user_base_info/" + state.userId + "/").then((response) => {
    const res = response[0];
    myStatus = getStatusByName(res.nowStatus);
  });
  if(myStatus != "hima" && myStatus != "maybe"){
      return false;
  }

  // 指定のhouseIdがあるかチェック なければinitデータを作る
  const houseId = data.houseId;
  if(state.latestNoticeData[houseId] == undefined){
    // init
    state.latestNoticeData[data.houseId] = {
      houseId: houseId,
      latestNoticeTimeOM: new Date(),
      latestNoticeHouseMatesNumOM: 0
    }
  }

  // 日付処理
  const latestNoticeTimeOM = new Date(state.latestNoticeData[houseId].latestNoticeTimeOM.getTime());

  // 前回記録時から日付が変わっていたら人数カウントリセット
  if(latestNoticeTimeOM.getDate() != new Date().getDate()){
    state.latestNoticeData[houseId].latestNoticeHouseMatesNumOM = 0;
  }

  // 前回の通知から規定時間以上立っていたら送る
  latestNoticeTimeOM.setMinutes( latestNoticeTimeOM.getMinutes() + state.noticeIntervalMinOM);
  if(latestNoticeTimeOM > new Date()){
      return false;
  }

  return true;
}

const noticeOnlineMembers = async (data) => {
  // 2人以上になったよの通知
  // 通知しつつ次の通知のインターバルを設定する。

  // 通知許可チェック
  const permission = await checkNoticePermission();
  if(!permission) return;

  // 人数と通知時間の記録(家ごとに)
  state.latestNoticeData[data.houseId] = {
    houseId: data.houseId,
    latestNoticeTimeOM: new Date(),
    latestNoticeHouseMatesNumOM: data.count
  }

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
  
  // インターバルよりも少し多く待つ
  setTimeout(() =>{someOneChangeStatus({houseId: data.houseId, status:"hima"})}, state.noticeIntervalMinOM * 60 * 1000 + 1000);
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





// 受信時
const joinEvent = async (data) => {
  // イベント参加
  const sendData = {
    eventId: data.eventId,
    userId: data.userId,
  }
  await fetchPostData("api/join_event/",sendData);
}