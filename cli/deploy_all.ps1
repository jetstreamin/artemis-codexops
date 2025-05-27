# Artemis CodexOps: PowerShell Full AWS Deployment Script

# 1. Deploy root infrastructure
Write-Host "Deploying root infrastructure stack..."
aws cloudformation deploy --template-file artemis-codexops/cloudformation-root-infra.yaml --stack-name codexops-root --capabilities CAPABILITY_NAMED_IAM

# 2. Build and push Docker images for each service (requires Docker and ECR login)
$services = @(
  "plugin-marketplace",
  "api-billing",
  "certificate-issuer",
  "affiliate-program",
  "pay-per-use",
  "white-label",
  "billing-invoicing",
  "live-events",
  "in-app-purchases",
  "auth"
)
$ecrRepo = "123456789012.dkr.ecr.us-east-1.amazonaws.com"
$s3Bucket = "codexops-assets-123456789012"
$dbUrl = "postgresql://codexopsadmin:codexopspassword@codexops-db.xxxxxxxx.us-east-1.rds.amazonaws.com:5432/codexops"

foreach ($svc in $services) {
  $pyPath = "artemis-codexops/agents/$svc.py"
  if (Test-Path $pyPath) {
    Write-Host "Building and pushing $svc..."
    docker build -t "$ecrRepo/$svc:latest" -f artemis-codexops/Dockerfile .
    aws ecr get-login-password | docker login --username AWS --password-stdin $ecrRepo
    docker push "$ecrRepo/$svc:latest"
  }
}

# 3. Deploy each service using the modular template
foreach ($svc in $services) {
  $pyPath = "artemis-codexops/agents/$svc.py"
  if (Test-Path $pyPath) {
    Write-Host "Deploying $svc..."
    bash artemis-codexops/cli/deploy_service.sh $svc "$ecrRepo/$svc:latest" 8080 $dbUrl $s3Bucket
  }
}

Write-Host "Deployment complete. Check AWS CloudFormation and ECS dashboards for status."
