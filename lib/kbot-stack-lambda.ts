import * as path from "path";
import * as cdk from "@aws-cdk/core";
import * as lambda from "@aws-cdk/aws-lambda";
import * as lambdapython from "@aws-cdk/aws-lambda-python";
import * as iam from "@aws-cdk/aws-iam";
import {
  Deployment,
  LambdaIntegration,
  LambdaRestApi,
  RestApi,
  Stage,
} from "@aws-cdk/aws-apigateway";
import { Duration } from "@aws-cdk/core";

export class KbotStackLambda extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

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

    const kBotFunction = new lambdapython.PythonFunction(this, "fn-kbot", {
      functionName: "kbot",
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
        LINE_CHANNEL_ACCESS_TOKEN: "dummy",
        LINE_CHANNEL_SECRET: "dummy",
        LINE_SEND_ID_1: "dummy",
        LINE_SEND_GROUP_ID_1: "dummy",
        LIBRARY_CHECK_RENTAL_FUNCTION_ARN: "dummy",
        LIBRARY_CHECK_EXPIRE_FUNCTION_ARN: "dummy",
        LIBRARY_CHECK_RESERVE_FUNCTION_ARN: "dummy",
        LIBRARY_CHECK_PREPARE_FUNCTION_ARN: "dummy",
      },
    });
    cdk.Tags.of(kBotFunction).add("runtime", "python");

    // 図書館チェック系Functionをinvoke出来る必要がある
    const awsAccount = process.env.CDK_AWS_ACCOUNT;
    const awsRegion = process.env.CDK_AWS_REGION;
    const phase = process.env.PHASE;
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

    // 最新バージョンを取得
    const currentVersion = kBotFunction.currentVersion;
    // development エイリアスは最新バージョンを指定
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

    //+++++++++++++++++++++++++++++++++++
    // prd function version and alias
    //+++++++++++++++++++++++++++++++++++

    const prodFunctionVersion = process.env.CDK_KBOT_LAMBDA_FUNCTION_VERSION;
    const prodVersion = lambda.Version.fromVersionArn(
      this,
      "ProductionVersion",
      `${kBotFunction.functionArn}:${prodFunctionVersion}`
    );
    const production = prodVersion.addAlias("prod");

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
