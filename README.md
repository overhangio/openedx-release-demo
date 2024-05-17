# Open edX release demo platform CD

This repo holds the continuous deployment (CD) scripts to deploy the Open edX release demo platforms. As of May 9, 2024, it is used to deploy and configure a test instance of the Redwood release.

⚠ THIS REPO IS NOT FOR PUBLIC CONSUMPTION ⚠ It is only used to deploy and configure a test instance for the [Build/Test/Release working group](https://discuss.openedx.org/c/working-groups/build-test-release/30). Detected issues should be reported to the working group.

URLs:

- LMS: https://redwood.demo.edly.io
- Studio: https://studio.redwood.demo.edly.io

You may log in with the following credentials:

- Student user:
  - username: student
  - email: student@overhang.io
  - password: student
- Administrator user:
  - username: admin
  - email: admin@overhang.io
  - password: admin

The platform is reset weekly, every Monday at 7 am UTC.

The [deployment script](https://github.com/overhangio/openedx-release-demo/blob/master/.github/workflows/deploy.yml) is included in this repository. If you are working on testing the latest release and you would like to modify this script, please open a pull request.

The following plugins are enabled on the demo platform:

- tutor-android (TBD)
- ~~tutor-cairn ([PR](https://github.com/overhangio/tutor-cairn/pull/39) by @FahadKhalid210)~~
  - tutor-contrib-aspects ([master branch](https://github.com/openedx/tutor-contrib-aspects/tree/master))
  - aspects has been enabled in place of cairn for testing of certain Product features.
- tutor-contrib-codejail ([PR](https://github.com/eduNEXT/tutor-contrib-codejail/pull/54) by @MoisesGSalas)
- tutor-credentials ([PR](https://github.com/overhangio/tutor-credentials/pull/42) by @Faraz32123)
- tutor-discovery ([PR](https://github.com/overhangio/tutor-discovery/pull/74) by @Faraz32123)
- tutor-ecommerce ([PR](https://github.com/overhangio/tutor-ecommerce/pull/81) by @Faraz32123)
- tutor-forum ([PR](https://github.com/overhangio/tutor-forum/pull/36) by @DawoudSheraz)
- tutor-indigo ([PR](https://github.com/overhangio/tutor-indigo/pull/79) by @hinakhadim)
- tutor-mfe ([PR](https://github.com/overhangio/tutor-mfe/pull/207) by @hinakhadim)
- tutor-minio ([PR](https://github.com/overhangio/tutor-minio/pull/40) by @FahadKhalid210)
- tutor-notes ([PR](https://github.com/overhangio/tutor-notes/pull/37) by @jfavellar90)
- tutor-webui (TBD)
- tutor-xqueue ([PR](https://github.com/overhangio/tutor-xqueue/pull/31) by @jfavellar90)
- tutor-jupyter (TBD)

If you are interested in upgrading these plugins to Redwood, please submit a PR by following the regular [plugin upgrade instructions](https://discuss.overhang.io/t/how-to-upgrade-a-tutor-plugin/1488).

## Testing

The deployment script can be tested with [act](https://github.com/nektos/act). Define your secrets::

    # edit the resulting .secrets file
    cp .secrets.sample .secrets

Note that multi-line strings are not supported in secrets files, so you should replace carriage returns with "\n".

Then run::

    act workflow_dispatch

## License

This work is licensed under the terms of the [GNU Affero General Public License (AGPL)](https://github.com/overhangio/tutor/blob/master/LICENSE.txt).
