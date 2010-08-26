from setuptools import setup, find_packages

setup(
    name='django-plebian',
    version='0.1.1',
    description='Commonly-used applications for Django projects',
    author='C. Alan Zoppa',
    author_email='alan.zoppa@gmail.com',
    url='http://github.com/alanzoppa/django-plebian',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
