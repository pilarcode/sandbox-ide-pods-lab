# Docker Image for the API

To generate the Docker image for the API, follow these steps:

## Step 1: Build the Docker image

``` sh
docker build -t ide-api .
```

## Step 2: Run the container to verify it works

``` sh
docker run -p 8000:8000 ide-api
```

## Step 3: Log in to GHCR using Docker

You need a Personal Access Token (PAT) with the scope `write:packages`
and `read:packages`.

Go to **Settings → Developer settings → Personal access tokens → Tokens
(classic)**.

Create a token with: - `write:packages` - `read:packages` - `repo` (if
you want to upload to private repositories)

Log in to GHCR using Docker:

``` sh
echo <YOUR_PAT> | docker login ghcr.io -u pilarcode --password-stdin
```

## Step 4: Tag your image

GHCR recommends using semantic versions (`1.0.0`) instead of `latest`.

``` sh
docker tag ide-api:latest ghcr.io/pilarcode/ide-api:0.0.1
```

## Step 5: Push your image

This command will push your image to the Github registry.

``` sh
docker push ghcr.io/pilarcode/ide-api:0.0.1
```

## Step 6: Verify on Github \> Packages

``` sh
docker pull ghcr.io/pilarcode/ide-api:0.0.1
docker run -p 8000:8000 ghcr.io/pilarcode/ide-api:0.0.1
```



# Docker Image for Coder

## Step 1: Create your Docker image for Coder:

``` sh
docker build -t coder-compi -f coder/DockerfileCoder
```

## Step 2: Tag your image
``` sh
docker tag coder-app:latest ghcr.io/pilarcode/coder-app:0.0.1
```

## Step 3: Push your image
``` sh
docker push ghcr.io/pilarcode/coder-app:0.0.1
```

## Step 3: Validate that you can pull the image
``` sh
docker pull ghcr.io/pilarcode/coder-app:0.0.1
docker run -p 8080:8080 ghcr.io/pilarcode/coder-app:0.0.1
```


# Deploying the API in the Cluster

## Step 1 :Create a namespace:

``` sh
kubectl create namespace sandbox
```


## Step 2: Create a secret for the Docker registry:

``` sh
kubectl create secret docker-registry regcred   --docker-server=ghcr.io   --docker-username=pilarcode   --docker-password=<PAT>   --docker-email=<EMAIL>   --namespace=sandbox
```

## Step 3: Apply the deployment YAML file:

``` sh
kubectl apply -f devops/ide-api-deploy.yaml
```

## Step 4: Apply the RBAC YAML file
We need the API has permission to create new objects (namespace, pods, nodes, etc) in the kubernetes cluster. For instance, When the user call the api, the api will create pods with the visual studio code image container.

``` sh
kubectl apply -f devops/ide-api-rbac.yaml
```


## Step 5: Port-forward the service:

``` sh
kubectl port-forward svc/ide-api 8000:8000 -n sandbox
```
Note: In production we will do this step differently.



# Commands to check the status of the deployment

## Get services in the sandbox namespace:

``` sh
kubectl get svc -n sandbox
```

## Get service accounts, roles, and role bindings in the sandbox namespace:

``` sh
kubectl get sa,role,rolebinding -n sandbox
```

## Get the cluster role:

``` sh
kubectl get clusterrole ide-api-role
```

## Get the cluster role binding:

``` sh
kubectl get clusterrolebinding ide-api-nodes-binding
```
