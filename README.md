# Open edX release demo platform CD

This repo holds the continuous deployment (CD) scripts to deploy the Open edX release demo platforms. As of October 11th 2022 it is used to deploy and configure a test instance of the Palm release.

⚠ THIS REPO IS NOT FOR PUBLIC CONSUMPTION ⚠ It is only used to deploy and configure a test instance for the [Build/Test/Release working group](https://discuss.openedx.org/c/working-groups/build-test-release/30). Detected issues should be reported to the working group.

URLs:

- LMS: https://palm.demo.overhang.io
- Studio: https://studio.palm.demo.overhang.io

You may login with the following credentials:

- Student user:
    - username: student
    - email: student@overhang.io
    - password: student
- Administrator user:
    - username: admin
    - email: admin@overhang.io
    - password: admin

The platform is reset weekly, every Monday at 7 am UTC.

The [deployment script](https://github.com/overhangio/openedx-release-demo/blob/master/.github/workflows/deploy.yml) is included in this repository. If you are working on testing the latest release and you would like to modify this script, please do open a pull request.

The following plugins are enabled on the demo platform:

- tutor-mfe ([PR](https://github.com/overhangio/tutor-mfe/pull/120) by @regisb)
- tutor-forum ([PR])(https://github.com/overhangio/tutor-forum/pull/22 by @ghassanmas)

The following plugins have not been installed, yet:

- tutor-minio
- tutor-indigo
- tutor-android
- tutor-notes
- tutor-xqueue
- tutor-contrib-codejail
- tutor-discovery
- tutor-ecommerce

If you are interested in upgrading these plugins to Palm, please submit a PR by following the regular [plugin upgrade instructions](https://discuss.overhang.io/t/how-to-upgrade-a-tutor-plugin/1488).

## Testing

The deployment script can be tested with [act](https://github.com/nektos/act). Define your secrets::

    # edit the resulting .secrets file
    cp .secrets.sample .secrets

Note that multi-line strings are not supported in secrets files, so you should replace carriage returns by "\n".

Then run::

    act workflow_dispatch

## License

This work is licensed under the terms of the [GNU Affero General Public License (AGPL)](https://github.com/overhangio/tutor/blob/master/LICENSE.txt).
