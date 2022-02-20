# 使っているもの
## 技術要素
docker:動作環境閉じ込めたい  
python3.10:現時点の最新だった  
django:ログイン画面とか色々やってくれるというので

## アプリの動作環境について 
Herokuで無料範囲の環境を使用する  
HerokuサーバとaddonのPostgresを使う  
herokku postgresは1GB 1万行までがfreeらしい。。  
まあ、写真にだけ気を付けていれば普通に使う分には大丈夫か。  

## 開発環境について
- dockerで必要なものは立つ用にしている  
- 必要なもの
  - docker
  - git
  - vscode(エディタならなんでも)

### docker環境の立ち上げ方
appやserviceと同じ階層で実行
```
docker-compose up -d --build
```

### docker立ち上げ時のTips
- starting container process caused: exec: "/usr/src/server/entrypoint.sh": permission denied: unknown
  - 実行権限を付与する
    - chmod +x server/imahima_mura/entrypoint.sh server/imahima_mura/manage.py

### docker環境への入り方
リモートエクスプローラー
1. docker環境を立ち上げる
2. vscodeのリモートエクスプローラーを開いて、appとserverでAttach to Containerを選択する
3. 開くを選択し、以下のディレクトリを指定してOKを押す
  - app: /usr/src/app/
  - server: /usr/src/server/
4. これで実行中のdockerの中に入れるので作業を開始する

execコマンド
```
docker exec -it imahima_server_dev bash
```

### ローカルpostgres
```
docker-compose exec postgres psql --username=django_db_user --dbname=django_db
```

### swagger
API単体確認用
```
http://localhost:8000/swagger  
```
必要なトークンなどはauthで発行する

## django実行メモ
- 接続先
  - http://localhost:8000/
- Djangoの起動
  - python manage.py runserver
- DBの反映
  - python manage.py migrate

## vue
http://localhost:8080/

# 公開環境へのデプロイ
## 使用環境
- heroku
## デプロイ方法
- herokuのコンテナレジストリに公開してそこからリリース
  - github連携だといちいちコミットが必要になってきてしまうので気軽に試すのが難しくなりそうだったので。
  - serverとappでレポジトリを分けるのが面倒だったというのもある。
- server側をRestAPIとして作るつもりで、バックグラウンド処理ではなかったのでHeroku上1サーバにするのは無理だった
- デプロイにはheroku cliが必要
## 環境変数
- docker-compose内で定義する。
  - 開発環境と公開環境でcomposeの形自体もどうせ違うので環境変数だけ切り出さなくても良いかなと。


# ディレクトリ構成
- テーブルの塊ごとにファイルにする。
- modelsとviewsとserializersはセット
- カスタム要素がある場合は、viewsの中で対処する

# DB定義
- 削除方式：物理削除
  - 現在の状態を綺麗に保つため
- ID形式：uuid
  - APIでIDをキーに操作することもあるので予測しづらいIDにする
  - ユーザだけは人目に触れやすいので桁数を減らして使用する