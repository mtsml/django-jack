# django-jack

## 本番環境
https://django-jack.herokuapp.com/

## 環境構築
```bash
$ git clone https://github.com/mtsml/django-jack.git
```
```bash
$ pip install -r requirements.txt
```
```bash
$ python manage.py runserver
```
多分これで動く

## 開発手順
1. issue切る
2. branch切る
3. 修正する
4. プルリク出す
5. 承認されたらマージされる

## デプロイ
masterブランチに変更があった場合ぶ自動的にHerokuへデプロイされる