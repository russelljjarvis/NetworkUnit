import sciunit
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from abc import ABCMeta, abstractmethod
from networkunit.plots import sample_histogram


class two_sample_test(sciunit.Test):
    """
    Parent class for specific two sample test scenarios which enables
    initialization via a data model instead of a direct observation,
    interchangeable test scores, and basic sample visualization.
    """
    __metaclass__ = ABCMeta

    # required_capabilites = (ProducesSample, ) # Replace by more appropriate
                                              # capability in child class
                                              # i.e ProduceCovariances

    def __init__(self, observation=None, name=None, **params):
        super(two_sample_test,self).__init__(observation, name=name, **params)

    def generate_prediction(self, model, **kwargs):
        """
        To be overwritten by child class
        """
        self.params.update(kwargs)
        try:
            return model.produce_sample(**self.params)
        except:
            raise NotImplementedError("")

    def compute_score(self, observation, prediction):
        score = self.score_type.compute(observation, prediction, **self.params)
        return score

    def _create_plotting_samples(self, model1=None, model2=None, palette=None):
        samples = []
        if palette is None:
            palette = []
            fill_palette = True
        else:
            fill_palette = False
        if self.observation is not None:
            samples += [self.observation]
            if fill_palette:
                try:
                    palette = palette + [self.observation_params['color']]
                except:
                    palette = palette + [sns.color_palette()[0]]
        if model1 is not None:
            samples += [self.generate_prediction(model1, **self.params)]
            if fill_palette:
                try:
                    palette = palette +[model1.params['color']]
                except:
                    palette = palette + [sns.color_palette()[len(samples)-1]]
        if model2 is not None:
            samples += [self.generate_prediction(model2, **self.params)]
            if fill_palette:
                try:
                    palette = palette + [model1.params['color']]
                except:
                    palette = palette + [sns.color_palette()[len(samples)-1]]

        return samples, palette

    def visualize_sample(self, model1=None, model2=None, ax=None, bins=100,
                         palette=None,
                         sample_names=['observation', 'prediction'],
                         var_name='Measured Parameter', **kwargs):

        samples, palette = self._create_plotting_samples( model1=model1,
                                                         model2=model2,
                                                         palette=palette)

        sample_histogram(sample1=samples[0], sample2=samples[1],
                         ax=ax, bins=bins,
                         palette=palette, sample_names=sample_names,
                         var_name=var_name, **kwargs)
        return ax

    def visualize_score(self, model1, model2=None, ax=None, palette=None,
                        **kwargs):
        """
        When there is a specific visualization function called plot() for the
        given score type, score_type.plot() is called;
        else call visualize_sample()
        Parameters
        ----------
        ax : matplotlib axis
            If no axis is passed a new figure is created.
        palette : list of color definitions
            Color definition may be a RGB sequence or a defined color code
            (i.e 'r'). Defaults to current color palette.
        Returns : matplotlib axis
        -------
        """
        # try:
        samples, palette = self._create_plotting_samples(model1=model1,
                                                         model2=model2,
                                                         palette=palette)

        kwargs.update(self.params)
        ax = self.score_type.plot(samples[0], samples[1],
                                  ax=ax, palette=palette, **kwargs)
        # except:
        #     self.visualize_sample(model=model, ax=ax, palette=palette)

        return ax
