# Open edX release demo platform CD

This repo holds the continuous deployment (CD) scripts to deploy the Open edX release demo platforms. As of October 23, 2024, it is used to deploy and configure a test instance of the Sumac release.

⚠ THIS REPO IS NOT FOR PUBLIC CONSUMPTION ⚠ It is only used to deploy and configure a test instance for the [Build/Test/Release working group](https://discuss.openedx.org/c/working-groups/build-test-release/30). Detected issues should be reported to the working group.

URLs:

- LMS: https://sumac.demo.edly.io
- Studio: https://studio.sumac.demo.edly.io

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

- tutor-android ([PR](https://github.com/overhangio/tutor-android/pull/28) by @muhammadali286 & @Abdul-Muqadim-Arbisoft)
  - The mobile apk can be downloaded from https://mobile.sumac.demo.edly.io/app.apk.
- ~~tutor-cairn (TBA)~~
  - tutor-contrib-aspects ([v1.2.0](https://github.com/openedx/tutor-contrib-aspects/tree/v1.2.0))
  - aspects has been enabled in place of cairn for testing of certain Product features.
- tutor-contrib-codejail ([PR](https://github.com/eduNEXT/tutor-contrib-codejail/pull/59) by @MoisesGSalas)
- tutor-credentials ([PR](https://github.com/overhangio/tutor-credentials/pull/49) by @Faraz32123)
- tutor-discovery ([PR](https://github.com/overhangio/tutor-discovery/pull/87) by @Faraz32123)
- tutor-ecommerce ([PR](https://github.com/overhangio/tutor-ecommerce/pull/84) by @Faraz32123)
- tutor-forum ([PR](https://github.com/overhangio/tutor-forum/pull/49) by @ghassanmas)
- tutor-indigo ([PR](https://github.com/overhangio/tutor-indigo/pull/101) by @hinakhadim)
- tutor-mfe ([PR](https://github.com/overhangio/tutor-mfe/pull/227) by @hinakhadim and @DawoudSheraz)
- tutor-minio ([PR](https://github.com/overhangio/tutor-minio/pull/51) by @Faraz32123)
- tutor-notes ([PR](https://github.com/overhangio/tutor-notes/pull/41) by @jfavellar90)
- tutor-webui ([PR](https://github.com/overhangio/tutor-webui/pull/19) by @Abdul-Muqadim-Arbisoft & @hinakhadim)
- tutor-xqueue ([PR](https://github.com/overhangio/tutor-xqueue/pull/34) by @jfavellar90)
- tutor-jupyter ([PR](https://github.com/overhangio/tutor-jupyter/pull/15) by @Abdul-Muqadim-Arbisoft)
  - LTI passport is `jupyterhub:openedx:jupyter-lti-password`.

If you are interested in upgrading these plugins to Sumac, please submit a PR by following the regular [plugin upgrade instructions](https://discuss.overhang.io/t/how-to-upgrade-a-tutor-plugin/1488).

## Testing

The deployment script can be tested with [act](https://github.com/nektos/act). Define your secrets::

    # edit the resulting .secrets file
    cp .secrets.sample .secrets

Note that multi-line strings are not supported in secrets files, so you should replace carriage returns with "\n".

Then run::

    act workflow_dispatch

## Server provisioning

We need to be careful not to exceed the disk space and the server memory to avoid filled disks, excessive build times and crashes.

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

    docker buildx create --use --name=max4cpu --config=./buildkitd.toml

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

## License

This work is licensed under the terms of the [GNU Affero General Public License (AGPL)](https://github.com/overhangio/tutor/blob/master/LICENSE.txt).
