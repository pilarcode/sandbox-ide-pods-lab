from datetime import datetime, timezone, timedelta
from kubernetes import client, config
from fastapi import HTTPException
from ide.utils import logger
from ide.utils.settings import settings
from ide.utils.utils import Utils
from ide.schemas.schemas import EnvironmentVariable
from typing import List
import os

# Initialize the logger
log = logger.get_logger(__name__)

class KubernetesService:
    """
    Service for interacting with Kubernetes, including creating namespaces, user pods, and deleting resources.
    """
    def __init__(self):
       
        # Load Kubernetes configuration
        try:
            config.load_kube_config()
            log.info("Kubernetes configuration loaded from kubeconfig file. Local enviroment detected.")
        except config.ConfigException:
            try:
                config.load_incluster_config()
                log.info("Kubernetes configuration loaded from in-cluster configuration. AKS enviroment detected.")
            except config.ConfigException as e:
                log.error("Failed to load Kubernetes configuration: %s", str(e))
                raise HTTPException(status_code=500, detail="Error loading Kubernetes configuration")

    def create_namespace_if_not_exists(self, namespace: str):
        # Create the namespace
        namespace_manifest = client.V1Namespace(
            metadata=client.V1ObjectMeta(name=namespace)
        )
        try:
            core_v1 = client.CoreV1Api()
            core_v1.create_namespace(namespace_manifest)
            log.info(f"Namespace {namespace} created")
        except client.exceptions.ApiException as e:
            if e.status == 409:  # Namespace already exists
                log.info(f"Namespace {namespace} already exists")
            else:
                raise HTTPException(status_code=500, detail=str(e))

    def delete_namespace(self, namespace: str):
        log.info(f"Deleting namespace {namespace}")
        core_v1 = client.CoreV1Api()
        core_v1.delete_namespace(namespace)
        log.info(f"Namespace {namespace} deleted")

    def is_running_in_aks(self) -> bool:
        log.info("Checking if running in AKS")
        core_v1 = client.CoreV1Api()
        
        nodes = core_v1.list_node()
        for node in nodes.items:
            for label, value in node.metadata.labels.items():
                if "azure" in value.lower():
                    return True
        return False
        
    def create_deployment(self, username: str, minutes: int, seconds: int)->str:
    
        log.info(f"Creating deployment for {username}")
        deployment_name = Utils.get_deployment_name(username)
        service_name = Utils.get_service_name(username)
        container_name = Utils.get_container_name(username)
        pod_name = Utils.get_pod_name(username)
        app_name = Utils.get_app_name(username)

        labels = {"app": app_name, "user": username}
        service_type = "LoadBalancer" if self.is_running_in_aks() else "NodePort"

        # Create the deployment
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=deployment_name, labels=labels),
            spec=client.V1DeploymentSpec(
                replicas=1,
                selector=client.V1LabelSelector(match_labels=labels),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels=labels),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=container_name,
                                image=settings.pod_container_image,
                                ports=[client.V1ContainerPort(container_port=settings.pod_container_port)],
                                security_context=client.V1SecurityContext(
                                    run_as_user=1000,
                                    run_as_group=3000,
                                    allow_privilege_escalation=False
                                ),
                                resources=client.V1ResourceRequirements(
                                    requests={"cpu": "250m", "memory": "512Mi"},
                                    limits={"cpu": "500m", "memory": "1Gi"}
                                )
                            )
                        ],
                    )
                )
            )
        )

        # Create the service
        service = client.V1Service(
            metadata=client.V1ObjectMeta(name=service_name),
            spec=client.V1ServiceSpec(
                selector=labels,
                ports=[
                    client.V1ServicePort(
                        port=settings.pod_container_port,
                        target_port=settings.pod_container_port
                    )
                ],
                type=service_type
            )
        )

        try:
            apps_api = client.AppsV1Api()
            core_api = client.CoreV1Api()

            apps_api.create_namespaced_deployment(
                namespace=settings.namespace, body=deployment
            )
            core_api.create_namespaced_service(
                namespace=settings.namespace, body=service
            )

            log.info(f"Deployment {deployment_name} and Service {service_name} created.")

            # Obtener endpoint del servicio
            created_service = core_api.read_namespaced_service(
                name=service_name, namespace=settings.namespace
            )

            endpoint = None
            if service_type == "LoadBalancer":
                ingress = created_service.status.load_balancer.ingress
                if ingress:
                    endpoint = f"http://{ingress[0].ip}:{settings.pod_container_port}"
            elif service_type == "NodePort":
                node_port = created_service.spec.ports[0].node_port
                # en NodePort necesitas la IP de un nodo del cluster
                nodes = core_api.list_node()
                if nodes.items:
                    # Tomamos la primera IP interna
                    node_ip = nodes.items[0].status.addresses[0].address
                    endpoint = f"http://{node_ip}:{node_port}"

            log.info(f"Deployment {deployment_name} and Service {service_name} created with endpoint {endpoint}")
            return endpoint

        except Exception as e:
            log.error(f"Error creating deployment/service: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def delete_deployment(self, username: str):
        apps_api = client.AppsV1Api()
        core_api = client.CoreV1Api()

        service_name = Utils.get_service_name(username)
        deployment_name = Utils.get_deployment_name(username)

        try:
            # Eliminar Deployment
            apps_api.delete_namespaced_deployment(
                name=deployment_name,
                namespace=settings.namespace,
                body=client.V1DeleteOptions(propagation_policy="Foreground")
            )
            log.info(f"Deployment {deployment_name} deleted")

            # Eliminar Service
            core_api.delete_namespaced_service(
                name=service_name,
                namespace=settings.namespace,
                body=client.V1DeleteOptions()
            )
            log.info({"message": f"Deployment {deployment_name} and Service {service_name} deleted"})

        except client.exceptions.ApiException as e:
            if e.status == 404:
                log.warning(f"Deployment or Service for {username} not found")
                raise HTTPException(status_code=404, detail="Deployment or Service not found")
            else:
                log.error(f"Error deleting resources for {username}: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
