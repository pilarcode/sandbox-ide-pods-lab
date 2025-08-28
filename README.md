# IDE API
![Static Badge](https://img.shields.io/badge/version-0.0.1-blue)

## Description
The API is responsible for creating and deleting resources in Kubernetes to install instances of Visual Studio for each user.


## Functionality
The API interacts with the Kubernetes API to perform the following actions:
- Creates a deployment and service for each user
- Deletes the deployment and service for each user.

## Prerequisites
- Python 3.12+

## Getting started

1️⃣. Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2️⃣. Install dependencies
```sh
pip install -r requirements.txt
```

3️⃣. Install the project

```sh
uv pip install -e .
```


4️⃣ Set up the environment variables:

```sh
cp .env.example .env
```


## Usage

To run the app use the main.py script.

```bash
python src\main.py 
```


The swagger ui is available at http://localhost:8000/docs


## Docker image for the API

To generate the docker image for the API follow these steps:

1️⃣. Build the Docker image:
```sh
docker build -t ide-api . 
```

2️⃣. Run the container to verify that works.
```sh
docker run -p 8000:8000 ide-api
```


3️⃣. Inicia sesión en GHCR usando Docker:

Necesitas un Personal Access Token (PAT) con el scope write:packages y read:packages.
Ve a Settings → Developer settings → Personal access tokens → Tokens (classic).
Crea un token con:
- write:packages
- read:packages
- repo (si quieres subir a repos privados)

Inicia sesión en GHCR usando Docker:

```sh
echo <YOUR_PAT> | docker login ghcr.io -u pilarcode --password-stdin
```
4️⃣ Tag you image

GHCR recommends using semantic versiones (1.0.0) instead of the **latest**

```sh
docker tag ide-api:latest ghcr.io/pilarcode/ide-api:0.0.1
```

5️⃣ Push your image
This command will push your image to the Github registry.
```sh
docker push ghcr.io/pilarcode/ide-api:0.0.1
```

6️⃣ You can verify Github > Packages
```sh
docker pull ghcr.io/pilarcode/ide-api:0.0.1
docker run -p 8000:8000 ghcr.io/pilarcode/ide-api:0.0.1
```

# Devops


## Docker image for the coder

More information about coder
- https://coder.com/docs/install/docker
- https://hub.docker.com/r/codercom/coder/tags


Create your docker image for coder
```sh
docker build -t coder-app -f coder/DockerfileCoder
```

```sh
docker tag coder-app:latest ghcr.io/pilarcode/coder-app:0.0.1
```

```sh
docker push ghcr.io/pilarcode/coder-app:0.0.1
```

```sh
docker pull ghcr.io/pilarcode/coder-app:0.0.1
docker run -p 8080:8080 ghcr.io/pilarcode/coder-app:0.0.1
```

## Deployment the api in the cluster
```sh
kubectl create namespace sandbox
```


```sh
kubectl create secret docker-registry regcred  --docker-server=ghcr.io  --docker-username=pilarcode --docker-password=<PAT>  --docker-email=<EMAIL> --namespace=sandbox
```

```sh
kubectl apply -f devops/ide-api-deploy.yaml
```

```sh
kubectl apply -f devops/ide-api-rbac.yaml
```

```sh
kubectl port-forward svc/ide-api 8000:8000 -n sandbox
```


# commands
```sh
kubectl get svc -n sandbox
kubectl get sa,role,rolebinding -n sandbox
kubectl get clusterrole ide-api-role
kubectl get clusterrolebinding ide-api-nodes-binding
```