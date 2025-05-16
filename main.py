
import os
from dotenv import load_dotenv
from modules.nlp_processor import NLPProcessor
from modules.kubernetes_handler import KubernetesHandler
from modules.github_handler import GitHubHandler
import argparse
import yaml

def main():
    load_dotenv()
    
    # Initialize components
    nlp_processor = NLPProcessor()
    k8s_handler = KubernetesHandler()
    github_handler = GitHubHandler(os.getenv("GITHUB_TOKEN"))
    
    parser = argparse.ArgumentParser(description="Natural Language to Kubernetes/GitHub Commands")
    parser.add_argument("command", type=str, help="Natural language command")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()
    
    # Process natural language
    processed = nlp_processor.process_natural_language(args.command)
    
    if args.verbose:
        print("Processed understanding:")
        print(processed)
    
    # Determine target system and execute
    if processed.get("target_system") == "kubernetes" or processed.get("kubernetes"):
        if not k8s_handler.current_context:
            k8s_handler.set_context("minikube")  # default
            
        action = processed.get("action", processed["verbs"][0] if processed["verbs"] else "get")
        resource = processed.get("target_resource", processed["nouns"][0] if processed["nouns"] else "pods")
        
        result = k8s_handler.execute_command(action, resource, processed.get("parameters", {}))
        cmd = k8s_handler.generate_kubectl_command(action, resource, processed.get("parameters", {}))
        
        print(f"Command: {cmd}")
        print("\nResult:")
        print(result)
        
    elif processed.get("target_system") == "github" or processed.get("github"):
        operation = processed.get("action", processed["verbs"][0] if processed["verbs"] else "list_repos")
        
        result = github_handler.execute_command(operation, processed.get("parameters", {}))
        cmd = github_handler.generate_gh_command(operation, processed.get("parameters", {}))
        
        print(f"Command: {cmd}")
        print("\nResult:")
        print(result)
    else:
        print("Could not determine if this is a Kubernetes or GitHub command")

if __name__ == "__main__":
    main()
