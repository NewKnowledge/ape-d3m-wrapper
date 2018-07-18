from distutils.core import setup


setup(name='APEd3mWrapper',
      version='1.0.0',
      description='Abstractive Prediction via (Concept) Embedding primitive.',
      packages=['APEd3mWrapper'],
      keywords=['d3m_primitive'],
      install_requires=['pandas >= 0.22.0, < 0.23.0',
                        'numpy >= 1.13.3',
                        'nk_ape >= 1.0.2'],
      dependency_links=[
          "git+https://github.com/NewKnowledge/nk_ape@414064de018d5cfd6a7dae593ae275aee79c4170#egg=nk_ape-1.0.2"
      ],
      entry_points={
          'd3m.primitives': [
              'distil.ape = APEd3mWrapper:ape'
          ],
      }
      )
