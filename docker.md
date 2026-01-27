# Docker Install Directions

These directions are adapted from here: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

We will install with `apt`.  The `apt` program installs packages from repositories.  To get the latest Docker versions, we will need to add a repository:

```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

We will install specific versions of Docker and Docker Compose to make sure everybody's VM works the same way this semester:

```bash
DOCKER_VERSION=5:29.2.0-1~ubuntu.24.04~noble
COMPOSE_VERSION=5.0.2-1~ubuntu.24.04~noble
sudo apt install docker-ce=$DOCKER_VERSION docker-ce-cli=$DOCKER_VERSION containerd.io docker-buildx-plugin docker-compose-plugin=$5.0.2-1~ubuntu.24.04~noble
```

Follow the directions to make Docker usable without root: https://docs.docker.com/engine/install/linux-postinstall#manage-docker-as-a-non-root-user.

Do NOT do systemd part.
