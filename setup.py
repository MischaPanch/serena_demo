from setuptools import setup, find_packages

setup(
    name="project-documentation-agent",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        line.strip() for line in open("requirements.txt")
        if not line.startswith("#") and line.strip()
    ],
    entry_points={
        "console_scripts": [
            "doc-agent=src.main:main",
        ],
    },
    python_requires=">=3.9",
    author="AI Team",
    author_email="ai@example.com",
    description="An agent for automated project documentation generation",
    keywords="documentation, automation, ai, notion, jira, google-drive",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
