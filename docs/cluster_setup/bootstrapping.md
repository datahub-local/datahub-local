# Bootstraping

Now, that we have ready our Hardware and the devices are accessible via SSH. Next thing is to bootstrap our Kubernetes cluster so it has the base services needed to run any kind of workload.


## 1. Creating Ansible inventory


## 2. Executing Ansible playbook

1. Ensure that the OS has the minimum packages for executing Ansible

    ```bash
    ansible k3s_cluster -i inventory.yml -b -m shell -a "apt-get update && apt-get install -y python3 python3-pip python3-apt"
    ```

2. Execute site playbook

    ```bash
    ansible-playbook playbook/site.yml -i inventory.yml
    ```

3. Execute bootstraping playbook

    ```bash
    ansible-playbook playbook/bootstrap.yml -i inventory.yml
    ```

## 3. Other usefull commands

- Reboot the cluster

  ```bash
  ansible-playbook playbook/reboot.yml -i inventory.yml
  ```

- Shutdown the cluster

  ```bash
  ansible-playbook playbook/shutdown.yml -i inventory.yml
  ```