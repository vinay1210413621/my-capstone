# Python CI/CD Pipeline with GitHub Actions

Complete end-to-end CI/CD workflow that builds Python code, scans for vulnerabilities, pushes to AWS ECR, and deploys to Kind Kubernetes cluster.

## 📁 Project Structure

```
github_workspace/
├── .github/
│   └── workflows/
│       └── cicd.yml              # Main CI/CD workflow
├── main.py                       # Sample FastAPI application
├── test_main.py                  # Unit tests
├── Dockerfile                    # Docker container definition
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔄 Workflow Stages

### 1. **Build & Test** (`build-and-test`)
- Checkout code
- Setup Python 3.11
- Install dependencies
- Run linting tools:
  - **Black** - Code formatting
  - **isort** - Import sorting
  - **pylint** - Code analysis (min score: 8.0)
  - **flake8** - PEP 8 compliance
- Build Docker image
- Save and upload image artifact

### 2. **Dependency Scan** (`dependency-scan`)
- Install Python dependencies
- **Safety** - Check for known vulnerabilities in dependencies
- **Bandit** - Find security issues in Python code
- Upload Bandit JSON report

### 3. **Security Scan - Trivy** (`security-scan`)
- Download Docker image artifact
- Run **Trivy** vulnerability scan on container image
- Filter by CRITICAL and HIGH severity
- Upload SARIF results to GitHub Security tab
- Generate JSON report

### 4. **Push to AWS ECR** (`push-to-ecr`)
- Only runs on `main` branch pushes
- Configure AWS credentials
- Login to AWS ECR
- Push image with commit SHA tag and `latest` tag
- **Requires:** All previous jobs to pass

### 5. **Deploy to Kind Cluster** (`deploy-to-kind`)
- Only runs on `main` branch pushes
- Create local Kind Kubernetes cluster (3 nodes)
- Setup ECR credentials secret
- Deploy Python app with 2 replicas
- Configure health checks (liveness + readiness)
- Expose via LoadBalancer service
- Run smoke tests

### 6. **Cleanup Artifacts** (`cleanup-artifacts`)
- Remove temporary Docker image artifact

## 🔐 Required GitHub Secrets

Add these secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):

```
AWS_ACCESS_KEY_ID          # AWS IAM access key
AWS_SECRET_ACCESS_KEY      # AWS IAM secret key
AWS_ACCOUNT_ID             # Your AWS account ID (12 digits)
AWS_REGION                 # AWS region (e.g., us-east-1)
```

## 📋 Prerequisites

- GitHub repository
- AWS account with ECR access
- Python 3.11+
- Docker installed locally (for testing)

## 🚀 Quick Start

### 1. Clone/Setup Repository

```bash
cd github_workspace
git init
git add .
git commit -m "Initial commit: Python CI/CD pipeline setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Add GitHub Secrets

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Create new repository secrets with AWS credentials

### 3. Create ECR Repository

```bash
aws ecr create-repository \
  --repository-name my-python-app \
  --region us-east-1
```

### 4. Push Code

```bash
git push origin main
```

The workflow will automatically trigger!

## 📊 Monitoring Workflow

1. Go to your GitHub repo → Actions tab
2. Click on the workflow run
3. View real-time logs for each job
4. Check GitHub Security tab for Trivy scan results

## 🔍 Scan Results

### Black Formatting
Ensures consistent code style. Fix with:
```bash
black .
```

### isort Import Sorting
Organizes imports. Fix with:
```bash
isort .
```

### pylint Code Analysis
Checks code quality. View issues with:
```bash
pylint **/*.py
```

### flake8 Style Guide
Checks PEP 8 compliance. View issues with:
```bash
flake8 .
```

### Safety Dependencies
Checks for known vulnerabilities:
```bash
pip install -r requirements.txt
safety check
```

### Bandit Security Scan
Finds security issues in code:
```bash
bandit -r .
```

### Trivy Container Scan
Scans Docker image for CVEs:
```bash
trivy image IMAGE_URI
```

## 📦 Docker Image

The Dockerfile includes:
- Python 3.11 slim base image
- Dependency installation
- Application code
- Health checks for Kubernetes probes
- Uvicorn ASGI server on port 8000

## 🐳 Kubernetes Deployment

The workflow deploys:
- **Replicas:** 2 pods
- **Resource Limits:**
  - CPU: 250m (request) / 500m (limit)
  - Memory: 256Mi (request) / 512Mi (limit)
- **Health Checks:**
  - Liveness: Checks every 10s (30s delay)
  - Readiness: Checks every 5s (10s delay)
- **Service:** LoadBalancer on port 80 → 8000

## 🧪 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_main.py -v

# Run linting
black --check .
isort --check-only .
pylint **/*.py
flake8 .

# Build Docker image
docker build -t my-python-app:latest .

# Run container locally
docker run -p 8000:8000 my-python-app:latest

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/
```

## 🛠️ Customization

### Change Python Version
Edit `.github/workflows/cicd.yml`:
```yaml
python-version: '3.12'  # Change this
```

### Change AWS Region
```yaml
AWS_REGION: eu-west-1  # Change this
```

### Adjust Pylint Score
```yaml
pylint **/*.py --fail-under=7.0  # Change threshold
```

### Modify Kubernetes Deployment
Edit the `Create deployment manifest` step in the deploy job to customize:
- Replica count
- Resource limits
- Port configuration
- Environment variables

## 📝 Sample Application

The included `main.py` is a FastAPI application with:
- `/health` - Health check endpoint
- `/ready` - Readiness check endpoint
- `/` - Root endpoint
- `POST /items` - Create item
- `GET /items/{item_id}` - Get item

## 🔗 Useful Links

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Trivy Scanner](https://aquasecurity.github.io/trivy/)
- [Kind Kubernetes](https://kind.sigs.k8s.io/)
- [Bandit Security](https://bandit.readthedocs.io/)

## 📞 Troubleshooting

### Build fails with "no such file: requirements.txt"
Ensure `requirements.txt` is in the repo root.

### ECR push fails with credential error
Verify AWS secrets are configured correctly in GitHub.

### Kind deployment fails
Check if 3GB RAM is available (Kind needs ~1GB per node).

### Trivy scan shows too many vulnerabilities
Update base image: `FROM python:3.11-slim`

## 📄 License

MIT License - Use freely for your projects

---

**Created:** 2026-08-29  
**Maintained by:** Your Team
