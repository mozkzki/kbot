# kbot

bot。

## 始め方

下記がベースなので最初に読んでください。

- [mozkzki/selenium-in-lambda](https://github.com/mozkzki/selenium-in-lambda)

## CDK 周り

### デプロイ

スタックをデプロイ。Lambdaバージョン付け、Alias更新までやる。

※ .shはトークン記載してるのでpushしていない (要対応)

```sh
# 開発
./deploy_dev.sh
# 本番
./deploy_prd.sh
```

### 実行

```sh
aws lambda invoke --function-name kbot response.json --log-type Tail --query 'LogResult' --output text | base64 -d
# or
# cdk.jsonがある場所で
make start
```

### テスト

CDKコードのテスト。

```sh
make test
```

### スタック削除

```sh
cdk destroy
```

## Python コード開発

`lambda`ディレクトリ以下で開発する。

```sh
cd lambda
# lint
make lint
# 環境変数設定
cp env_sample.sh env.sh
vi env.sh
source env.sh
# unit test
make ut
```
