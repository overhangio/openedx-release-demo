# Open edX Nutmeg demo platform CD

This repo holds the continuous deployment (CD) scripts to deploy the [nutmeg.demo.overhang.io](https://nutmeg.demo.overhang.io) platform.

URLs:

- LMS: https://nutmeg.demo.overhang.io
- Studio: https://studio.nutmeg.demo.overhang.io

You may login with the following credentials:

- Student user:
    - username: student
    - email: student@overhang.io
    - password: student
- Administrator user:
    - username: admin
    - email: admin@overhang.io
    - password: admin

## Testing

The deployment script can be tested with [act](https://github.com/nektos/act). Define your secrets::

    # edit the resulting .secrets file
    cp .secrets.sample .secrets

Note that multi-line strings are not supported in secrets files, so you should replace carriage returns by "\n".

Then run::

    act workflow_dispatch
