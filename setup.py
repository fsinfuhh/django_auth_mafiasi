import setuptools

setuptools.setup(
    name="django_auth_mafiasi",
    version="1.2.0",
    author="Finn-Thorben Sell",
    author_email="7sell@informatik.uni-hamburg.de",
    description="Django authentication library for working with Mafiasi",
    url="https://git.mafiasi.de/mafiasi-ag/django_auth_mafiasi",
    license="MIT",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "django>=3.1",
        "oic>=1.2",
    ],
    extras_require={
        "django-configurations": "django-configurations>=2.2",
        "djangorestframework": ["djangorestframework>=3.12", "py-jwt-verifier>=0.7"],
    },
)
