# 公式からpython3.10 on slim-busterイメージをpull
# 同期関数あたりでバグにあたったので、3.10.1が出るまでは3.9を使う(channelsのredis書き込みあたり)
# https://github.com/aio-libs/janus/issues/358
FROM python:3.9.9-slim-buster

# 作業ディレクトリを設定
WORKDIR /usr/src/server

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

# 必要ライブラリのインストール
RUN apt-get update
RUN apt-get -y install libpq-dev gcc

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/server/requirements.txt
RUN pip install -r requirements.txt

# ホストのカレントディレクトリ（現在はserverディレクトリ）を作業ディレクトリにコピー
COPY imahima_mura/ /usr/src/server/

ENV PORT=8000
# entrypoint.shを実行
ENTRYPOINT ["/usr/src/server/entrypoint.sh"]
CMD python manage.py runserver 0.0.0.0:$PORT