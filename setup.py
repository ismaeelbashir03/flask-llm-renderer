from setuptools import setup, find_packages

setup(
    name='flask_llm_renderer',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'openai',
        'anthropic',
        'eventlet'
    ],
)
