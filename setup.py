from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements()->List[str]:
    requirement_list:List[str] = []
    
    with open('requirements.txt') as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement.replace('\n','') for requirement in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list

setup(
    name='llm-rag',
    version='0.0.1',
    author='Rohit Kumar',
    author_email='rohit.kr.0310@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)