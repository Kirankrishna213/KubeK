
from kubernetes import client, config
from kubernetes.client import ApiClient
import yaml
from typing import Dict, Optional
import subprocess
from pathlib import Path

class KubernetesHandler:
    def __init__(self, contexts_config: str = "config/k8s_contexts.yaml"):
        self.contexts = self._load_contexts(contexts_config)
        self.current_context = None
        self.api_client = None
        
    def _load_contexts(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)["contexts"]
    
    def set_context(self, context_name: str) -> bool:
        for ctx in self.contexts:
            if ctx["name"] == context_name:
                try:
                    config.load_kube_config(context=context_name)
                    self.current_context = context_name
                    self.api_client = ApiClient()
                    return True
                except:
                    return False
        return False
    
    def execute_command(self, action: str, resource: str, params: Dict[str, str]) -> str:
        if not self.api_client:
            return "Error: No Kubernetes context selected"
            
        try:
            if action == "get":
                return self._handle_get(resource, params)
            elif action == "describe":
                return self._handle_describe(resource, params)
            elif action == "logs":
                return self._handle_logs(resource, params)
            elif action == "create":
                return self._handle_create(resource, params)
            elif action == "delete":
                return self._handle_delete(resource, params)
            elif action == "apply":
                return self._handle_apply(resource, params)
            elif action == "scale":
                return self._handle_scale(resource, params)
            else:
                return f"Unsupported action: {action}"
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def _handle_get(self, resource: str, params: Dict[str, str]) -> str:
        namespace = params.get("namespace", "default")
        
        if resource == "pods":
            v1 = client.CoreV1Api(self.api_client)
            pods = v1.list_namespaced_pod(namespace)
            return "\n".join([pod.metadata.name for pod in pods.items])
        elif resource == "deployments":
            apps_v1 = client.AppsV1Api(self.api_client)
            deployments = apps_v1.list_namespaced_deployment(namespace)
            return "\n".join([deploy.metadata.name for deploy in deployments.items])
        # Add more resource types as needed
    
    def _handle_describe(self, resource: str, params: Dict[str, str]) -> str:
        name = params.get("name")
        if not name:
            return "Error: Name parameter required for describe"
            
        namespace = params.get("namespace", "default")
        
        cmd = f"kubectl describe {resource} {name} -n {namespace}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    
    # Implement other handlers similarly...
    
    def generate_kubectl_command(self, action: str, resource: str, params: Dict[str, str]) -> str:
        cmd = f"kubectl {action} {resource}"
        
        if "name" in params:
            cmd += f" {params['name']}"
            
        if "namespace" in params:
            cmd += f" -n {params['namespace']}"
            
        if "output" in params:
            cmd += f" -o {params['output']}"
            
        if "selector" in params:
            cmd += f" -l {params['selector']}"
            
        return cmd
