# Dynamic Input Variables for Script

This script is designed to handle dynamic input variables related to certificate credentials for a specific use case. It serves as an interim solution to assist with housekeeping for expired credentials until a native API endpoint is available.

## Variables

- `hostname`: The tenant hostname. Example: `acmecorp.console.ves.volterra.io`

- `path_to_cert`: The path to the p12 certificate retrieved from F5 XC. This requires appropriate permissions for the credentials API.

- `cert_pass`: The password associated with the certificate.

## Usage

1. **Provide Dynamic Inputs**:
   - Update the following variables in the script to match your specific requirements:
     - `hostname`: Set this variable to your tenant hostname, such as `acmecorp.console.ves.volterra.io`.
     - `path_to_cert`: Specify the path to the p12 certificate obtained from F5 XC.
     - `cert_pass`: Input the password associated with the certificate.

2. **Execution**:
   - Execute the script after setting the dynamic input variables.
   
3. **Adjustments**:
   - If you are using an API token instead of a certificate for authorization, make the necessary adjustments to the script to pass the authorization header via curl as per your requirements.

## Note

- This script assumes that the credential is in the form of a certificate. Modify the script accordingly if you are using an API token for passing the authorization header via curl.

- The purpose of this script is to facilitate maintenance for expired credentials until a native API endpoint becomes available for this specific functionality.

