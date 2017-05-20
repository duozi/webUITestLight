#coding=utf-8
from setuptools import setup, find_packages, findall
setup(
    name='WebUITestLight',
    version='1.0.0',
    author='lyzsh',
    author_email='lyzsh@66.com',
    url='http://www.baidu.com/',
    description='Manage configuration files',
    packages=['WebUITestLight','WebUITestLight.Utils'], # packages=find_packages(),
    #data_files=[('WebUITestLight/Utils', ['WebUITestLight/Utils/ReportTemplate.html'])],
    include_package_data=True,
    package_data={"WebUITestLight.Utils": ["WebUITestLight/Utils/ReportTemplate.html"]},
    #setup_requires=['nose>=1.0'], # 指定依赖项
    long_description=open('README.txt').read(),
    zip_safe=False
 )
