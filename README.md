# Open edX release demo platform CD

This repo holds the continuous deployment (CD) scripts to deploy the Open edX release demo platforms. As of October 11th 2022 it is used to deploy and configure a test instance of the Olive release.

⚠ THIS REPO IS NOT FOR PUBLIC CONSUMPTION ⚠ It is only used to deploy and configure a test instance for the [Build/Test/Release working group](https://discuss.openedx.org/c/working-groups/build-test-release/30). Detected issues should be reported to the working group.

URLs:

- LMS: https://olive.demo.overhang.io
- Studio: https://studio.olive.demo.overhang.io

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

- tutor-mfe ([PR](https://github.com/overhangio/tutor-mfe/pull/66) by @ghassanmas)
- tutor-indigo ([PR](https://github.com/overhangio/tutor-indigo/pull/38) by @regisb)
- tutor-android ([PR](https://github.com/overhangio/tutor-android/pull/5) by @regisb): app can be downloaded from https://mobile.olive.demo.overhang.io/app.apk.
- tutor-forum ([PR](https://github.com/overhangio/tutor-forum/pull/11) by @ghassanmas)
- tutor-notes ([PR](https://github.com/overhangio/tutor-notes/pull/18) by @jfavellar90)
- tutor-xqueue ([PR](https://github.com/overhangio/tutor-xqueue/pull/13) by @jfavellar90)
- tutor-contrib-codejail ([PR](https://github.com/eduNEXT/tutor-contrib-codejail/pull/28) by @mariajgrimaldi)
- tutor-discovery ([PR](https://github.com/overhangio/tutor-discovery/pull/36) by @regisb)
- tutor-ecommerce ([PR](https://github.com/overhangio/tutor-ecommerce/pull/35) by @regisb): admin user can login with the credentials above at https://ecommerce.olive.demo.overhang.io/
- tutor-minio ([PR](https://github.com/overhangio/tutor-minio/pull/31) by @FahadKhalid210)

The following plugins have not been installed, yet:


If you are interested in upgrading these plugins to Olive, please submit a PR by following the regular [plugin upgrade instructions](https://discuss.overhang.io/t/how-to-upgrade-a-tutor-plugin/1488).

## Testing

The deployment script can be tested with [act](https://github.com/nektos/act). Define your secrets::

    # edit the resulting .secrets file
    cp .secrets.sample .secrets

Note that multi-line strings are not supported in secrets files, so you should replace carriage returns by "\n".

Then run::

    act workflow_dispatch

## License

This work is licensed under the terms of the [GNU Affero General Public License (AGPL)](https://github.com/overhangio/tutor/blob/master/LICENSE.txt).
