from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


extensions = [
    Extension(
        "triangle_mask",
        ["triangle_mask.pyx"]
    )
]


setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"}
    ),
    include_dirs=[np.get_include()]
)