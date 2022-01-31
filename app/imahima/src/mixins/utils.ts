import CONST from '../components/const'
import Store from '@/store'

// 共通処理用のファイル
export default function utils():Record<string, any> {

  const dateTimeToString = function(data:Date):string{
    const date:Date = new Date(data.getTime());
    const stringVal:string = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + " "
                              + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
    return stringVal;
  }

  const time2Date = (time:string):Date => {
    const day = new Date();
    const HH = parseInt(time.substring(0,2)) || 0;
    const mm = parseInt(time.substring(3,5)) || 0;
    day.setHours(HH);
    day.setMinutes(mm);
    return day;
  }

  const sortTime = (a:string, b:string):number => {
    const aTime = time2Date(a);
    const bTime = time2Date(b);
    if(aTime > bTime){
        return 1;
    }
    if(aTime < bTime){
        return -1;
    }
    return 0;
  }
  

  const getStatusByName = function(data:string):string{
    const statuses:Record<string, unknown> = CONST.STATUS;
    const result = Object.keys(statuses).filter((key:string) => { 
        return statuses[key] === data
    }).shift();
    return result || ""
  }

  const cutSeconds = function(fullTime:string):string{
    if(!fullTime){
      return fullTime;
    }
    return fullTime.substring(0,5);
  }

  const waitWSConnection = (callback:()=>void, interval:number) => {
    const ws = Store.state.websocket;
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

  const sendWebsocket = (message:string) => {
    waitWSConnection(()=>{
      Store.state.websocket?.send(message);
    }, 1000);
  }

  const checkNoticePermission =  async ():Promise<boolean> =>{
      // 通知許可チェック
      if (!("Notification" in window)) {
          // ブラウザ自体が未対応なので無視する
          return false;
      }
      if (Notification.permission === "granted") {
          return true;
      }else{
          // 許可されてないので許可を依頼する
          const result = await Notification.requestPermission();
          return result === "granted";
      }
  }

  return {
    dateTimeToString,
    time2Date,
    sortTime,
    getStatusByName,
    cutSeconds,
    sendWebsocket,
    checkNoticePermission
  }
  
}