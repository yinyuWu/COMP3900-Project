

Set-Variable -Name "TEMPLATEFILE" -Value ".aws-sam/build/template.yaml"
Set-Variable -Name "PACKAGEFILE"  -Value ".aws-sam/build/package.yaml"
Set-Variable -Name "S3"           -Value "taxidi-code"
Set-Variable -Name "STACKNAME"    -Value "taxidi"
Set-Variable -Name "AWSPROFILE"   -Value "default"

sam build
sam validate

sam package --template-file $TEMPLATEFILE --output-template-file $PACKAGEFILE --s3-bucket $S3 --profile $AWSPROFILE

sam deploy --template-file $PACKAGEFILE --stack-name $STACKNAME --capabilities CAPABILITY_NAMED_IAM --profile $AWSPROFILE --parameter-overrides ProjectName=$STACKNAME


