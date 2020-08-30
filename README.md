# django-jack

## 本番環境
https://django-jack.herokuapp.com/

## 環境構築
クローンする
```bash
$ git clone https://github.com/mtsml/django-jack.git
$ cd django-jack
```

ローカルで不要なパッケージを削除する
```bash
$ cat requirements.txt | (rm requirements.txt; sed '/^django-heroku/d' > requirements.txt)
```
※OSXのPOSIX sedで動作させるために冗長な記述になっている

必要なパッケージをインストールする
```bash
$ pip install -r requirements.txt
```

開発環境で使う設定ファイルを作成する
```bash
$ echo """import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True""" > django-jack/local_settings.py
```

マイグレーションする
```bash
$ python manage.py migrate
```

開発サーバーを起動する
```bash
$ python manage.py runserver
```

多分これで動く

## 開発手順
1. issue切る
2. branch切る
3. 修正する
4. プルリク出す（見てもらいたい場合は承認者を指定する）
5. マージするorされる

## デプロイ
masterブランチに変更があった場合に自動的にHerokuへデプロイされる