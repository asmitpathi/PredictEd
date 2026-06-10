from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT= "-e ."
def get_requirements(file_path: str)->List[str]:    #file_path should be str and output should be list
    # returns requirements as a list
    requirements=[]
    with open(file_path, 'r') as file_obj:
        requirements= file_obj.readlines()
        requirements= [req.replace("\n", "") for req in requirements]
    
    if HYPHEN_E_DOT in requirements:       ##-e . need not be installed as requirements, it will automatically get installed and connected
        requirements.remove(HYPHEN_E_DOT)
    
    return requirements

setup(
    name= 'PredictEd',
    version='0.0.1',
    author='Asmit',
    author_email= 'asmitpathi27@gmail.com',
    packages= find_packages(), ##Finds the folders containing __init__.py and treat them as package
    install_requires= get_requirements('requirements.txt')
)