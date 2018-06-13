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
          "git+https://github.com/NewKnowledge/nk_ape@fc4f10737bc7c498c261687f32ff70b680832176#egg=nk_ape-1.0.0"
      ],
      entry_points={
          'd3m.primitives': [
              'distil.ape = APEd3mWrapper:ape'
          ],
      }
      )
