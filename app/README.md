# 使っているもの
## 技術要素
- node:16.13(今のLTSバージョン)
- Volta：jsバージョン管理(nodeのバージョン管理に使う)
- Vue3
- Bootstrap5
  - bootstrap-vueやvuetifyは現時点でVue3に対応していないのでまだ使っていない
  - 対応したら使うかもだが、デザインも自分でやるので使わないかもしれない
- serviceworker
  - 通知用

### nodeモジュールメモ  
- axios 

# 公開環境へのデプロイ
server側のREADME参照のこと
## 環境変数
- docker-compose内で定義する。
  - 開発環境と公開環境でcomposeの形自体もどうせ違うので環境変数だけ切り出さなくても良いかなと。

# ディレクトリ構成
## 基本方針
atomic designに従って大きい順で管理する  
https://design.dena.com/design/atomic-design-%E3%82%92%E5%88%86%E3%81%8B%E3%81%A3%E3%81%9F%E3%81%A4%E3%82%82%E3%82%8A%E3%81%AB%E3%81%AA%E3%82%8B

## 命名規則
### css
- ライブラリ：cabab(foo-bar)
- 独自定義：snake(foo_bar)
  - ライブラリとの混同を防ぐため

# 開発環境について
## 通知機能
通知機能はビルド後の本番モードでないと発動できないので、以下の手順で確認する
1. npm run build
2. chromeアプリのWeb serverなどでdistフォルダをアプリとして起動する  
3. 以下のパスで接続する(サーバ側でホワイトリスト設定されているもの)
```
http://localhost:8887/
```
4. service-worker.jsに更新がある場合は、unregisterで削除したあとに2回リロードする。
  - 登録用とコントロールする用の2回

※通知を出すだけならregisterServiceWorker.tsをいじればserviceworkerの登録はできる。  
buildをしないとカスタムのService workerが入らないので、通知を押したあとの挙動が実行できなくなる。(まあページ遷移ぐらいかもしれないが。。)
