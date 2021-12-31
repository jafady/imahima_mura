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

### docker環境への入り方
docker exec -it imahima_server_dev bash

### ローカルpostgres
docker-compose exec postgres psql --username=django_db_user --dbname=django_db

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