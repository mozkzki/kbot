#!/bin/bash -eu

version=$1
echo "<new version>=" $version

# update alias
aws lambda update-alias --no-cli-auto-prompt --function-name prd-kbot --name prod --function-version $version
