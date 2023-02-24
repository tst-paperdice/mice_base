from distutils.core import setup

setup(
    name="mice_base",
    version="1.0",
    py_modules=["fe_types", "Features"],
    packages=['mice_base', 'mice_base.BaseFeatures'],
)
