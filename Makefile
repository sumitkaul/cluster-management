#ap-ep
validate-dev-stack: 
		sam validate -t template-dev.yaml

dev-stack:
		sam deploy -t template-dev.yaml --s3-bucket harness-dev-stack --confirm-changeset


#runtime
validate-stage-stack: 
		sam validate -t template-stage.yaml

stage-stack:
		sam deploy -t template-stage.yaml --s3-bucket harness-stage-stack --confirm-changeset 


#ap-shared-int
validate-int-stack: 
		sam validate -t template-int.yaml

int-stack:
		sam deploy -t template-int.yaml --s3-bucket harness-int-stack --confirm-changeset


#ap-shared-prod
validate-prod-stack:
		sam validate -t template-prod-shared.yaml

prod-stack:
		sam deploy -t template-prod.yaml --s3-bucket harness-prod-stack --confirm-changeset






