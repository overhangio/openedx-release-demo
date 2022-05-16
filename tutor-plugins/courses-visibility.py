from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-dockerfile-post-python-requirements",
        """
        RUN pip install --editable git+https://github.com/ghassanmas/edx-search@fix-visbile-courses#egg=edx-search
        """
    )
)
