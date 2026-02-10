from setuptools import setup, find_packages

setup(
    name="wifi-deauth",
    version="2.0.0",
    author="bad-antics",
    description="WiFi deauthentication attack and detection toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=["requests", "colorama", "pyyaml", "rich"],
)
