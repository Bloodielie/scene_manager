import setuptools


requirements = [
    "aiogram==2.9.*",
    "aioredis==1.3.1",
    "pydantic==1.5.1",
    "python-dotenv==0.13.0",
    "loguru==0.5.1",
]


setuptools.setup(
    name="scene_manager",
    python_requires=">=3.7",
    version="0.1.0",
    packages=setuptools.find_packages(),
    url="https://github.com/Bloodielie/scene_manager",
    license="MIT",
    author="Bloodie_lie",
    author_email="riopro2812@gmail.com",
    description="Scenes manager for aiogram",
    install_requires=requirements,
    include_package_data=False
)