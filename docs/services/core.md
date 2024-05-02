# Core

After our Kubernertes cluster is ready to be used, we must install all the core services that will be used to create our Data platform.

## Deploying ArgoCD App

As discuess before, we will be using a GitOps approach to deploy our services usin [ArgoCD](https://argo-cd.readthedocs.io/). Therefore, the core services configuration is stored in [datahub-local-core](https://github.com/datahub-local/datahub-local-core). To depoy it, we must create an ```Application``` resource.


```bash
kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: datahub-local-core
  namespace: argo-cd
spec:
  project: default
  source:
    repoURL: https://github.com/datahub-local/datahub-local-core.git
    targetRevision: main
    path: .
  destination:
    server: "https://kubernetes.default.svc"
  syncPolicy:
    automated: {}
    syncOptions:
      - ServerSideApply=true
EOF
```