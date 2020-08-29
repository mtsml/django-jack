# django-jack

## Herokuへのデプロイ
[こちら](https://qiita.com/okoppe8/items/76cdb202eb15aab566d1)を参考

`dj-database-url`により特別な設定を行わず**Heorku Postgres**を使用することができる

APサーバーは`Gunicorn`

`django-heroku`のインストールが`psycopg2`のせいでコケるので、依存パッケージを省く`--no-deps`オプションを付与してインストールする
```bash
$ pip install --no-deps django-heroku
```
依存パッケージは別途インストールする（`psycopg2`はかわりに`psycopg2-binary`を入れる）

## DBをPotgresqlに変更する

```bash
$ pip install psycopg2-binary
```

[こちら](https://qiita.com/shigechioyo/items/9b5a03ceead6e5ec87ec)を少しだけ参考にした

## チュートリアル
https://docs.djangoproject.com/ja/3.1/intro/tutorial01/