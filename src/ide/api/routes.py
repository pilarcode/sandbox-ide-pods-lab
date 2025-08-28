from fastapi import APIRouter, HTTPException
from ide.schemas.schemas import VSCodeRequest, VsCodeResponse,VsCodeStatus,NamespaceResponse
from ide.utils.settings import settings
from ide.services.kubernetes_service import KubernetesService
from ide.utils import logger

from typing import List

# Initialize the logger
log = logger.get_logger(__name__)


# Create a router for the API
# This will allow us to group related endpoints together
router = APIRouter()


@router.post("/ide/instances", tags=["ide"], response_model=VsCodeResponse)
async def deploy_vscode(req: VSCodeRequest)->VsCodeResponse:
    """
    Create a VSCode instance in Kubernetes
    """
    try:
        kubernetes_service = KubernetesService()
        log.info(f"Creating VSCode {req.username} with minutes {req.minutes} and seconds {req.seconds} and environmentVariables {req.environmentVariables}")
        url = kubernetes_service.create_deployment(username=req.username,minutes=req.minutes,seconds=req.seconds)
        response = VsCodeResponse(url=url,username=req.username, status=VsCodeStatus.CREATED, message=f"VSCode {req.username} created")
        log.info(f"VSCode {req.username} created")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/ide/instances/{username}", tags=["ide"], response_model=VsCodeResponse)
async def delete_vscode(username: str)->VsCodeResponse:
    """
    Delete a VSCode instance in Kubernetes
    """
    try:
        kubernetes_service = KubernetesService()
        kubernetes_service.delete_deployment(username=username)
        response = VsCodeResponse(username=username, status=VsCodeStatus.DELETED, message=f"VSCode {username} deleted")
        log.info(f"VSCode {username} deleted")
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    


@router.post("/create_namespace/{namespace}", tags=["admin"])
def create_namespace(namespace:str):
    """
    Create a namespace in Kubernetes
    """
    kubernetes_service = KubernetesService()
    kubernetes_service.create_namespace_if_not_exists(namespace)
    return {"message": f"Namespace {namespace} created"}

@router.delete("/delete_namespace/{namespace}", tags=["admin"])
def delete_namespace(namespace:str):    
    """
    Delete a namespace in Kubernetes
    """
    kubernetes_service = KubernetesService()

    kubernetes_service.delete_namespace(namespace)
    return {"message": f"Namespace {namespace} deleted"}


