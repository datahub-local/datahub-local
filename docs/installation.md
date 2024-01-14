

echo "$USER ALL=(ALL:ALL) NOPASSWD:$(which apt)" | sudo tee -a "/etc/sudoers.d/dont-prompt-$USER-for-sudo-password" 

create ssh key

mount sdd disk:
2 partitions:
    /var/lib/rook
    /var/lib/rancher/k3s




cert-manager
https://bryanbende.com/development/2021/07/01/k3s-raspberry-pi-cert-manager


KUBESEAL_VERSION='0.24.5'
wget "https://github.com/bitnami-labs/sealed-secrets/releases/download/v${KUBESEAL_VERSION:?}/kubeseal-${KUBESEAL_VERSION:?}-linux-amd64.tar.gz"
tar -xvzf kubeseal-${KUBESEAL_VERSION:?}-linux-amd64.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal


echo -n bar | kubectl create secret generic mysecret --dry-run=client --from-file=foo=/dev/stdin -o json \
  | kubeseal > mysealedsecret.json



kubectl -n argo-cd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d



k3d cluster create -p "8443:443@loadbalancer" --agents 2


cat << EOF | k -n default apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: helmfile-example
spec:
  project: namespace-default
  source:
    repoURL: https://github.com/christianknell/blog-code.git
    targetRevision: main
    path: deploying-helm-charts-using-argocd-and-helmfile
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
EOF