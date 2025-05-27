# Artemis CodexOps: One-Command AWS Deployment

ROOT_STACK=codexops-root
SERVICES=plugin-marketplace api-billing certificate-issuer affiliate-program pay-per-use white-label billing-invoicing live-events in-app-purchases auth
ECR_REPO=123456789012.dkr.ecr.us-east-1.amazonaws.com
S3_BUCKET=codexops-assets-123456789012
DB_URL=postgresql://codexopsadmin:codexopspassword@codexops-db.xxxxxxxx.us-east-1.rds.amazonaws.com:5432/codexops

.PHONY: deploy-all deploy-root deploy-services build-images

deploy-all: deploy-root build-images deploy-services

deploy-root:
	aws cloudformation deploy --template-file artemis-codexops/cloudformation-root-infra.yaml --stack-name $(ROOT_STACK) --capabilities CAPABILITY_NAMED_IAM

build-images:
	@for svc in $(SERVICES); do \
		if [ -f artemis-codexops/agents/$$svc.py ]; then \
			echo "Building $$svc..."; \
			docker build -t $(ECR_REPO)/$$svc:latest -f artemis-codexops/Dockerfile .; \
			aws ecr get-login-password | docker login --username AWS --password-stdin $(ECR_REPO); \
			docker push $(ECR_REPO)/$$svc:latest; \
		fi \
	done

deploy-services:
	@for svc in $(SERVICES); do \
		if [ -f artemis-codexops/agents/$$svc.py ]; then \
			echo "Deploying $$svc..."; \
			bash artemis-codexops/cli/deploy_service.sh $$svc $(ECR_REPO)/$$svc:latest 8080 $(DB_URL) $(S3_BUCKET); \
		fi \
	done

validate:
	@echo "Validating all endpoints..."
	# Add curl or health check commands here for each service

clean:
	aws cloudformation delete-stack --stack-name $(ROOT_STACK)
	@for svc in $(SERVICES); do \
		aws cloudformation delete-stack --stack-name codexops-$$svc; \
	done
