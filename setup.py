from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='flask_llm_renderer',
    version='0.1.0',
    author='Ismaeel Bashir',
    author_email='ismaeelbashir2003@gmail.com',
    description='A Flask extension to render HTML dashboards with LLMs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ismaeelbashir03/flask-llm-renderer',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'openai',
        'anthropic',
        'eventlet'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Flask',
    ],
    python_requires='>=3.7',
)
