try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

setup(name='iperfidy',
      version='2017.12.05',
      description=("Iperf REST Server."),
      author="russell",
      platforms=['linux'],
      author_email="necromuralist@gmail.com",
      packages=find_packages(),
      )
