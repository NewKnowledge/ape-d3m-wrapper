import os
import sys
import typing
import numpy as np
import pandas as pd

from nk_ape import *

from d3m.primitive_interfaces.base import PrimitiveBase, CallResult

from d3m import container, utils
from d3m.metadata import hyperparams, base as metadata_base, params

__author__ = 'Distil'
__version__ = '1.0.0'

Inputs = container.pandas.DataFrame
Outputs = container.pandas.DataFrame


class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    pass


class ape(PrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    metadata = metadata_base.PrimitiveMetadata({
        # Simply an UUID generated once and fixed forever. Generated using "uuid.uuid4()".
        'id': '42a29a5a-68fd-4d9f-bbe4-ca1cc3620177',
        'version': __version__,
        'name': "ape",
        # Keywords do not have a controlled vocabulary. Authors can put here whatever they find suitable.
        'keywords': ['text augmentation', 'concept description', 'text analysis'],
        'source': {
            'name': __author__,
            'uris': [
                # Unstructured URIs.
                "https://github.com/NewKnowledge/ape-d3m-wrapper",
            ],
        },
        # A list of dependencies in order. These can be Python packages, system packages, or Docker images.
        # Of course Python packages can also have their own dependencies, but sometimes it is necessary to
        # install a Python package first to be even able to run setup.py of another package. Or you have
        # a dependency which is not on PyPi.
        "installation": [
            {
                "type": "FILE",
                "key": "en.model",
                "file_uri": "http://public.datadrivendiscovery.org/en_1000_no_stem/en.model",
                "file_digest": "e974c8783b8ce9aa3e598c555a8ffa9cb5bdfe970955fed00702850b855e3257"
            },
            {
                "type": "FILE",
                "key": "en.model.syn0.npy",
                "file_uri": "http://public.datadrivendiscovery.org/en_1000_no_stem/en.model.syn0.npy",
                "file_digest": "1b30f64c99a90c16a133cf06eb4349d012de83ae915e2467b710b7b6417a9d56"
            },
            {
                "type": "FILE",
                "key": "en.model.syn1.npy",
                "file_uri": "http://public.datadrivendiscovery.org/en_1000_no_stem/en.model.syn1.npy",
                "file_digest": "aa88b503ca1472d6efd7babe42b452e21178a74df80e01a7eb253c5eff96cd50"
            },

            {
                "type": "PIP",
                "package_uri": "git+https://github.com/NewKnowledge/nk_ape.git@68370736ec683fa4515f4f47b13c047cc0f328fe#egg=nk_ape"
            },
            {
                "type": "PIP",
                "package_uri": "git+https://github.com/NewKnowledge/ape-d3m-wrapper.git@{git_commit}#egg=APEd3mWrapper".format(
                    git_commit=utils.current_git_commit(os.path.dirname(__file__))
                ),
            }
        ],
        # The same path the primitive is registered with entry points in setup.py.
        'python_path': 'd3m.primitives.distil.ape',
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.
        "algorithm_types": [
            metadata_base.PrimitiveAlgorithmType.WORD2VEC
        ],
        "primitive_family": metadata_base.PrimitiveFamily.FEATURE_CONSTRUCTION
    })

    def __init__(self, *, hyperparams: Hyperparams, volumes: typing.Dict[str,str]=None)-> None:
        super().__init__(hyperparams=hyperparams, volumes=volumes)

        self._volumes = volumes

    def fit(self) -> None:
        pass

    def get_params(self) -> Params:
        return self._params

    def set_params(self, *, params: Params) -> None:
        self.params = params

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        pass

    def produce(self, *, inputs: Inputs) -> CallResult[Outputs]:
        """
            Produce a constellation of similar concepts that may be at
            a higher level of abstraction (i.e., summaries) than the input.

        Parameters
        ----------
        inputs : pandas dataframe where a column is a pd.Series and each cell
            contains a list or string of unstructured text (concepts)

        Returns
        -------
        output : input pandas dataframe augmented with related concepts as
            predicted by APE.
        """
        try:
            target_columns = self.hyperparams['target_columns']
            output_labels = self.hyperparams['output_labels']

            input_df = inputs
            tree = 'ontologies/class-tree_dbpedia_2016-10.json'
            embedding = self._volumes['en.model']
            row_agg_func = mean_of_rows
            tree_agg_func = np.mean
            source_agg_func = mean_of_rows
            max_num_samples = 1e6
            n_words = 10
            verbose = True

            for i, ith_column in enumerate(target_columns):
                # initialize an empty dataframe
                result_df = pd.DataFrame()
                output_label = output_labels[i]

                for concept_set in input_df.loc[:, ith_column]:

                    if not isinstance(concept_set, (list, tuple)):
                        concept_set = concept_set.split(' ')

                    ape_client = ConceptDescriptor(
                        concepts=concept_set,
                        tree=tree,
                        embedding=embedding,
                        row_agg_func=row_agg_func,
                        tree_agg_func=tree_agg_func,
                        max_num_samples=max_num_samples,
                        verbose=verbose
                    )

                    result = ape_client.get_top_n_words(n_words)

                    result_df = result_df.append(
                        {output_label + '_concepts': [i['concept'] for i in result],
                         output_label + '_confs': [i['conf'] for i in result]},
                        ignore_index=True)

                input_df = pd.concat(
                    [input_df.reset_index(drop=True), result_df], axis=1)

            return input_df

        except:
            return "APE failed to complete abstractive prediction"


if __name__ == '__main__':
    client = ape(hyperparams={'target_columns': ['test_column'],
                               'output_labels': ['test_column_prefix']})
    input_df = pd.DataFrame(
        pd.Series([['gorilla', 'chimp', 'orangutan', 'gibbon', 'human'],
                   ['enzyme', 'gene', 'hormone', 'lipid', 'polysaccharide']]))
    input_df.columns = ['test_column']
    result = client.produce(inputs=input_df)
    print(result.head)
