# 公式からpython3.10 on slim-busterイメージをpull
FROM python:3.10-slim-buster

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
COPY . /usr/src/server/

# entrypoint.shを実行
ENTRYPOINT ["/usr/src/server/entrypoint.sh"]