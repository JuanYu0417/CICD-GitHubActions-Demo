# CICD-GitHubActions-Demo
### The purpose of generating a new Base64 string is to embed all necessary Kubernetes certificate data directly into the Kubeconfig file (making it "self-contained"), thereby eliminating the CI/CD Runner's dependency on local file paths (like /home/ubuntu/...) and ensuring authentication succeeds.
```bash
kubectl config view --raw --flatten --minify --kubeconfig=~/.kube/config > embedded_kubeconfig.yaml
#~/ not always to home,so
kubectl config view --raw --flatten --minify --kubeconfig=/home/ubuntu/.kube/config > embedded_kubeconfig.yaml
NEW_BASE64_STRING=$(cat embedded_kubeconfig.yaml | base64 -w 0)
echo $NEW_BASE64_STRING
```
### should "paste as plain text"when set Actions secrets.
### use k3s to slove ip connect
### use lowercase letters in Linux