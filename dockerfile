# ベースイメージを指定
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# 環境変数を設定
ENV PYTHONPATH="/app:$PYTHONPATH"

# Uvicornを実行してアプリケーションを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
