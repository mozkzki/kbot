import * as path from "path";
import * as cdk from "@aws-cdk/core";
import * as lambda from "@aws-cdk/aws-lambda";
import * as lambdapython from "@aws-cdk/aws-lambda-python";
import * as iam from "@aws-cdk/aws-iam";
import { LambdaRestApi } from "@aws-cdk/aws-apigateway";
import { Duration, RemovalPolicy } from "@aws-cdk/core";

export class KbotStackLambda extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    // 環境変数
    const phase = process.env.PHASE;

    super(scope, `${phase}-${id}`, props);

    ////////////////////////////
    // Python lambda
    ////////////////////////////

    // アプリケーションが依存するライブラリを載せたlayer
    const layerForApp = new lambdapython.PythonLayerVersion(
      this,
      "python-lambda-layer-for-app",
      {
        layerVersionName: "python-lambda-layer-for-app",
        entry: path.resolve(__dirname, "../lambda/layer/app"),
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_7],
      }
    );

    // コード差分がない場合のエラー抑止のため
    const uniqueVersionId = `${new Date().getTime()}`;

    const kBotFunction = new lambdapython.PythonFunction(this, "fn-kbot", {
      functionName: `${phase}-kbot`,
      description: `This lambda deployed at ${uniqueVersionId}`,
      runtime: lambda.Runtime.PYTHON_3_7,
      entry: path.resolve(__dirname, "../lambda/src/kbot"),
      index: "index.py",
      handler: "handler",
      layers: [layerForApp],
      timeout: Duration.seconds(300),
      memorySize: 512,
      environment: {
        ///////////////////////////////////////////////////////////////////////////
        // 注意: 下記の環境変数についてはAWSコンソールにて正式な値をセットすること
        ///////////////////////////////////////////////////////////////////////////
        LINE_CHANNEL_ACCESS_TOKEN:
          process.env.LINE_CHANNEL_ACCESS_TOKEN || "dummy",
        LINE_CHANNEL_SECRET: process.env.LINE_CHANNEL_SECRET || "dummy",
        LINE_SEND_ID_1: process.env.LINE_SEND_ID_1 || "dummy",
        LINE_SEND_GROUP_ID_1: process.env.LINE_SEND_GROUP_ID_1 || "dummy",
        LIBRARY_CHECK_RENTAL_FUNCTION_ARN:
          process.env.LIBRARY_CHECK_RENTAL_FUNCTION_ARN || "dummy",
        LIBRARY_CHECK_EXPIRE_FUNCTION_ARN:
          process.env.LIBRARY_CHECK_EXPIRE_FUNCTION_ARN || "dummy",
        LIBRARY_CHECK_RESERVE_FUNCTION_ARN:
          process.env.LIBRARY_CHECK_RESERVE_FUNCTION_ARN || "dummy",
        LIBRARY_CHECK_PREPARE_FUNCTION_ARN:
          process.env.LIBRARY_CHECK_PREPARE_FUNCTION_ARN || "dummy",
      },
    });
    cdk.Tags.of(kBotFunction).add("runtime", "python");

    // 図書館チェック系Functionをinvoke出来る必要がある
    const awsAccount = process.env.CDK_AWS_ACCOUNT;
    const awsRegion = process.env.CDK_AWS_REGION;
    kBotFunction.addToRolePolicy(
      new iam.PolicyStatement({
        resources: [
          `arn:aws:lambda:${awsRegion}:${awsAccount}:function:${phase}-library-checker-check-*`,
        ],
        actions: ["lambda:InvokeFunction"],
      })
    );

    //+++++++++++++++++++++++++++++++++++
    // dev function version and alias
    //+++++++++++++++++++++++++++++++++++
    if (phase === "dev") {
      // development エイリアスに最新バージョンを指定
      const currentVersion = kBotFunction.currentVersion;
      const development = new lambda.Alias(this, "DevelopmentAlias", {
        aliasName: "develop",
        version: currentVersion,
      });

      // lambdaのdevelopエイリアスを、apiGateway "dev" ステージに紐付け
      const devApi = new LambdaRestApi(this, "KbotDevEndpoint", {
        handler: development,
        deployOptions: {
          stageName: "dev",
        },
        proxy: false,
      });
      // TODO: OpenAPI (Swagger) 対応
      devApi.root.addResource("line").addResource("bot").addMethod("POST");
    }

    //+++++++++++++++++++++++++++++++++++
    // prd function version and alias
    //+++++++++++++++++++++++++++++++++++
    if (phase === "prd") {
      // バージョンはデプロイごとに発行するが、エイリアスの切り替えまではしない
      new lambda.Version(this, `version-kbot-${uniqueVersionId}`, {
        lambda: kBotFunction,
        // prdは検証してから切り替えたいので、古いバージョンを残す
        removalPolicy: RemovalPolicy.RETAIN,
      });

      // エイリアスが紐づくバージョンは固定している
      // 動作に問題なければlive.shで目的のバージョンにエイリアスを切り替える
      const production = new lambda.Alias(this, "ProductionAlias", {
        aliasName: "prod",
        version: lambda.Version.fromVersionArn(
          this,
          "ProductionVersion",
          `${kBotFunction.functionArn}:1` // 固定(live.shで切り替え)
        ),
      });

      // lambdaのprodエイリアスを、apiGateway "prd" ステージに紐付け
      // TODO: 1つのAPIでmulti stageを紐付けたかったがCDKでやり方が分からなかった
      const prdApi = new LambdaRestApi(this, "KbotProdEndpoint", {
        handler: production,
        deployOptions: {
          stageName: "prd",
        },
        proxy: false,
      });
      // TODO: OpenAPI (Swagger) 対応
      prdApi.root.addResource("line").addResource("bot").addMethod("POST");
    }
  }
}
