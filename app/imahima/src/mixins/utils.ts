import CONST from '../components/const'

// 共通処理用のファイル
export default function utils():Record<string, any> {
  const dateTimeToString = function(data:Date):string{
    const date:Date = new Date(data.getTime());
    const stringVal:string = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + " "
                              + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
    return stringVal;
  }

  const getStatusByName = function(data:string):string{
    const swho:Record<string, unknown> = CONST.STATUS;
    const result = Object.keys(swho).filter((key:string) => { 
        return swho[key] === data
    }).shift();
    return result || ""
  }

  return {
    dateTimeToString,
    getStatusByName
  }
  
}