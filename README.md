# Open edX release demo platform CD

This repo holds the continuous deployment (CD) scripts to deploy the Open edX release demo platforms. As of April 24, 2025, it is used to deploy and configure a test instance of the Ulmo release.

⚠ THIS REPO IS NOT FOR PUBLIC CONSUMPTION ⚠ It is only used to deploy and configure a test instance for the [Build/Test/Release working group](https://discuss.openedx.org/c/working-groups/build-test-release/30). Detected issues should be reported to the working group.

URLs:

- LMS: https://ulmo.demo.edly.io
- Studio: https://studio.ulmo.demo.edly.io

You may log in with the following credentials:

- Student user:
  - username: student
  - email: student@edly.io
  - password: student
- Administrator user:
  - username: admin
  - email: admin@edly.io
  - password: admin

The platform is reset weekly, every Monday at 2 am UTC.

The [deployment script](https://github.com/overhangio/openedx-release-demo/blob/master/.github/workflows/deploy.yml) is included in this repository. If you are working on testing the latest release and you would like to modify this script, please open a pull request.

The following plugins are enabled on the demo platform:

- ✅ [tutor-mfe](https://github.com/overhangio/tutor-mfe/tree/ulmo)
- ✅ [tutor-discovery](https://github.com/overhangio/tutor-discovery/tree/ulmo)
- ✅ [tutor-credentials](https://github.com/overhangio/tutor-credentials/tree/ulmo)
- ✅ [tutor-minio](https://github.com/overhangio/tutor-minio/tree/ulmo)
- ✅ [tutor-forum](https://github.com/overhangio/tutor-forum/tree/ulmo)
- ✅ [tutor-notes](https://github.com/overhangio/tutor-notes/tree/ulmo)
- ✅ [tutor-xqueue](https://github.com/overhangio/tutor-xqueue/tree/ulmo)
- ✅ [tutor-android](https://github.com/overhangio/tutor-android/tree/ulmo)
- ✅ [tutor-jupyter](https://github.com/overhangio/tutor-jupyter/tree/ulmo)
- ✅ [tutor-contrib-codejail](https://github.com/eduNEXT/tutor-contrib-codejail/tree/ulmo)
- ✅ [tutor-contrib-aspects](https://github.com/openedx/tutor-contrib-aspects/tree/ulmo-dev)
- ✅ [tutor-contrib-notifications](https://github.com/openedx/tutor-contrib-notifications/tree/ulmo)

If you are interested in upgrading these plugins to Ulmo, please submit a PR by following the regular [plugin upgrade instructions](https://discuss.overhang.io/t/how-to-upgrade-a-tutor-plugin/1488) and mention it in the [sandbox tracking ticket](https://github.com/overhangio/tutor/issues/1281).

## Testing

The deployment script can be tested with [act](https://github.com/nektos/act). Define your secrets::

    # edit the resulting .secrets file
    cp .secrets.sample .secrets

Note that multi-line strings are not supported in secrets files, so you should replace carriage returns with "\n".

Then run::

    act workflow_dispatch

## Server provisioning

We need to be careful not to exceed the disk space and the server memory to avoid filled disks, excessive build times and crashes.

### Prerequisites

Install the utilities required to run the platform:

    #!/usr/bin/env bash

    set -e

    # DOCKER CONFIG
    # Add Docker's official GPG key:
    sudo apt update
    sudo apt install ca-certificates curl python3.12-venv -y
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

    sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    sudo systemctl status docker

    docker compose version

    sudo usermod -aG docker "$USER"

### Docker builder

We must configure the docker builder not to use more than 4 CPU and always leave some free space on disk. Edit `buildkit.toml` and add the following content:

    # https://docs.docker.com/build/buildkit/toml-configuration/
    # Apply configuration by stopping and removing build container:
    #
    #    docker stop buildx_buildkit_max4cpu0
    #    docker rm buildx_buildkit_max4cpu0
    #    docker buildx create --use --name=max4cpu --node=max4cpu0 --config=./buildkitd.toml
    #    docker buildx inspect --bootstrap
    #    docker exec buildx_buildkit_max4cpu0 cat /etc/buildkit/buildkitd.toml

    # Enable debug mode, such that we can log gc events and detect them with:
    #
    #    docker logs -f buildx_buildkit_max4cpu0 2>&1 | grep garbage
    debug = true
    [worker.oci]
      max-parallelism = 4
      gc = true
      # Keep some space for cache
      reservedSpace = "25GB"
      # Always leave some free space
      minFreeSpace = "10GB"

Then create the builder with:

    docker buildx create --use --name=max4cpu --config=./buildkit.toml

In case we are updating an existing builder, we need to stop and delete the container to apply the changes:

    docker buildx create --use --name=max4cpu --node=max4cpu0 --config=./buildkitd.toml
    docker stop buildx_buildkit_max4cpu0
    docker container rm buildx_buildkit_max4cpu0

### Image cache

First, we need to limit the amount of space used by Docker images. This can be achieved with the help of [docuum](https://github.com/stepchowfun/docuum):

    mkdir -p ~/apps/docuum
    cd ~/apps/docuum
    vim docker-compose.yml

Add the following services:

    services:
        # auto-clean least-recently used docker images
        docuum:
            image: stephanmisc/docuum:latest
            init: true
            volumes:
              - /var/run/docker.sock:/var/run/docker.sock
              - ./data/docuum:/root/.local/share/docuum
            command: "--threshold=50GB"
            restart: unless-stopped

And start it with:

    docker compose up -d

## Troubleshooting

### Connection timout
If you get a connection timeout error while applying migrations:

    botocore.exceptions.ConnectTimeoutError: Connect timeout on endpoint URL:

Then disable `ufw`:

    sudo ufw disable

Verify with:

    sudo ufw status
## License

This work is licensed under the terms of the [GNU Affero General Public License (AGPL)](https://github.com/overhangio/tutor/blob/master/LICENSE.txt).
