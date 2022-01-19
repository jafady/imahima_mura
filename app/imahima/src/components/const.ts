export interface STATUS {
    hima:string,
    maybe:string,
    busy:string,
    ongame:string
}
export interface BASE64 {
    header:string
}

export default Object.freeze({
    STATUS : {
        hima: "ヒマ",
        maybe: "予定ではヒマ",
        busy: "ヒマじゃない",
        ongame: "ゲーム中"
    },
    BASE64 : {
        header: "data:image/png;base64,"
    }
});