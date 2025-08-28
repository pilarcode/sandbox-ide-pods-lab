class Utils:
    @staticmethod
    def get_namespace(username):
        return f"user-{username}"
    
    @staticmethod
    def get_app_name(username):
        return f"ide-{username}-app"


    @staticmethod
    def get_service_name(username):
        return f"ide-{username}-svc"
    
    @staticmethod
    def get_pod_name(username):
        return f"ide-{username}-pod"
    
    @staticmethod
    def get_container_name(username):
        return f"ide-{username}-container"
        
    @staticmethod
    def get_deployment_name(username):
        return f"ide-{username}-deployment"



    