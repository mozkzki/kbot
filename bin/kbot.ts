#!/usr/bin/env node
import * as cdk from "@aws-cdk/core";
import { KbotStackLambda as KbotStackLambda } from "../lib/kbot-stack-lambda";

const app = new cdk.App();

new KbotStackLambda(app, "KbotStackLambda");
