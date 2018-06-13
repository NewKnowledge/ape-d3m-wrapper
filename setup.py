from distutils.core import setup


setup(name='APEd3mWrapper',
      version='1.0.0',
      description='Abstractive Prediction via (Concept) Embedding primitive.',
      packages=['APEd3mWrapper'],
      keywords=['d3m_primitive'],
      install_requires=['pandas >= 0.22.0, < 0.23.0',
                        'numpy >= 1.13.3',
                        'nk_ape >= 1.0.0'],
      dependency_links=[
          "git+https://github.com/NewKnowledge/nk_ape@68370736ec683fa4515f4f47b13c047cc0f328fe#egg=nk_ape-1.0.0"
      ],
      entry_points={
          'd3m.primitives': [
              'distil.ape = APEd3mWrapper:ape'
          ],
      }
      )
