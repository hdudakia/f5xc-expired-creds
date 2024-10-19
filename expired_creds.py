import json
import subprocess
from datetime import datetime, timezone

# Variables for dynamic input
# Variables for dynamic input
hostname = ""
path_to_cert = ""
cert_pass = ""

# Function to run the curl command and fetch credentials
def fetch_credentials(endpoint):
    command = (
        f"curl -k -s --cert-type P12 --cert {path_to_cert}:{cert_pass} "
        f"https://{hostname}/api/web/namespaces/system/{endpoint}"
    )
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error fetching credentials: {result.stderr}")
        return None
    return json.loads(result.stdout)

# Function to revoke credentials
def revoke_credential(name, revoke_endpoint):
    revoke_command = (
        f"curl -X 'POST' -d '{{\"name\":\"{name}\"}}' "
        f"-H 'Content-Type: application/json' "
        f"https://{hostname}/api/web/namespaces/system/{revoke_endpoint} "
        f"--cert-type P12 --cert {path_to_cert}:{cert_pass}"
    )
    revoke_result = subprocess.run(revoke_command, shell=True, capture_output=True, text=True)
    if revoke_result.returncode == 0:
        print(f"Successfully revoked credential: {name}")
    else:
        print(f"Error revoking credential {name}: {revoke_result.stderr}")

# Main logic to check for expired credentials and handle revocation
def main():
    print("Choose credential type:")
    print("1. Self Credentials")
    print("2. Service Credentials")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        endpoint = "api_credentials"
        kube_config_revoke_endpoint = "revoke/kube_config"
        global_kube_config_revoke_endpoint = "revoke/global-kubeconfigs"  # Added this for SITE_GLOBAL_KUBE_CONFIG
        api_token_revoke_endpoint = "revoke/api_credentials"
    elif choice == '2':
        endpoint = "service_credentials"
        kube_config_revoke_endpoint = "revoke/service_credentials"
        api_token_revoke_endpoint = "revoke/service_credentials"
    else:
        print("Invalid choice.")
        return

    credentials = fetch_credentials(endpoint)
    if not credentials or 'items' not in credentials:
        print("No credentials found or error occurred.")
        return

    now = datetime.now(timezone.utc)
    expired_non_api_tokens = []
    expired_api_tokens = []

    # Handle SERVICE_ prefixed types for Service Credentials
    for item in credentials['items']:
        expiry_time = datetime.fromisoformat(item['expiry_timestamp'].replace('Z', '+00:00'))
        if expiry_time < now:
            if choice == '2' and item['type'].startswith('SERVICE_'):
                item_type = item['type'].replace('SERVICE_', '')
            else:
                item_type = item['type']

            if item_type == 'API_TOKEN':
                expired_api_tokens.append(item['name'])
            elif item_type == 'SITE_GLOBAL_KUBE_CONFIG':
                # For SITE_GLOBAL_KUBE_CONFIG, use the global-kubeconfigs revoke endpoint
                expired_non_api_tokens.append((item['name'], global_kube_config_revoke_endpoint))
            else:
                expired_non_api_tokens.append((item['name'], kube_config_revoke_endpoint))

    # Handle non-API_TOKEN credentials
    if expired_non_api_tokens:
        print("Expired non-API_TOKEN credentials:")
        for name, _ in expired_non_api_tokens:
            print(f"- {name}")

        proceed = input("Do you want to revoke all expired non-API_TOKEN credentials? (yes/no): ")
        if proceed.lower() == 'yes':
            for name, revoke_endpoint in expired_non_api_tokens:
                revoke_credential(name, revoke_endpoint)
        else:
            print("Skipping revocation of non-API_TOKEN credentials.")
    else:
        print("No expired non-API_TOKEN credentials found.")

    # Handle API_TOKEN credentials separately, even if non-API_TOKEN credentials were skipped
    if expired_api_tokens:
        print("\nExpired API_TOKEN credentials:")
        for name in expired_api_tokens:
            print(f"- {name}")

        proceed_api_tokens = input("Do you want to revoke expired API_TOKEN credentials? (yes/no): ")
        if proceed_api_tokens.lower() == 'yes':
            for name in expired_api_tokens:
                revoke_credential(name, api_token_revoke_endpoint)
        else:
            print("Skipping revocation of API_TOKEN credentials.")
    else:
        print("No expired API_TOKEN credentials found.")

if __name__ == "__main__":
    main()

