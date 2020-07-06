from setuptools import setup
import sys
import json


PY2 = sys.version_info.major == 2
with open('metadata.json') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_blenchbenuecongo',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_blenchbenuecongo'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'blenchbenuecongo=lexibank_blenchbenuecongo:Dataset',
        ]
    },
    install_requires=[
        'pylexibank>=2.0',
    ]
)
