from functools import reduce

import numpy as np
from scipy.stats import multinomial

from ssrm_test import ssrm_test as st


class SSRMSuite:
    def setup(self):
        self.intended_p_alloc = [0.1, 0.5, 0.4]
        self.actual_p_alloc = [0.1, 0.49, 0.41]
        self.n = 1000
        self.alpha = 0.01
        self.dirichlet_probability = np.array([1, 3, 2])
        self.dirichlet_concentration = 1
        self.dirichlet_alpha = self.dirichlet_probability * self.dirichlet_concentration
        self.observations = multinomial.rvs(1, self.actual_p_alloc, size=self.n)
        self.observations_sum = reduce(lambda x, y: x + y, self.observations)
        self.posterior = {
            "log_marginal_likelihood_M1": -23.585991739528254,
            "log_marginal_likelihood_M0": -76546.65811250894,
            "posterior_M1": [88519.5, 12540.25, 13002.25],
            "posterior_M0": [0.75, 0.125, 0.125],
        }
        self.final_posterior = st.sequential_posteriors(
            self.observations,
            self.actual_p_alloc,
            dirichlet_probability=self.dirichlet_probability,
            dirichlet_concentration=self.dirichlet_concentration,
        )[-1]

    def time_sequential_posteriors(self):
        st.sequential_posteriors(
            self.observations,
            self.intended_p_alloc,
            dirichlet_probability=self.dirichlet_probability,
            dirichlet_concentration=self.dirichlet_concentration,
        )

    def time_bayes_factor(self):
        st.bayes_factor(self.posterior)

    def time_posterior_probability(self):
        final_bayes_factor = st.bayes_factor(self.final_posterior)
        st.posterior_probability(final_bayes_factor)

    def time_log_marginal_likelihood_M1(self):
        st.log_posterior_predictive(self.observations_sum, self.dirichlet_alpha)

    def time_log_marginal_likelihood_M0(self):
        st.multinomiallogpmf(
            self.observations_sum, self.observations_sum.sum(), self.actual_p_alloc
        )

    def time_get_bayes_factor_threshold(self):
        st.get_bayes_factor_threshold(
            self.observations_sum, self.dirichlet_alpha, self.alpha
        )

    def time_sequential_posterior_probabilities(self):
        st.sequential_posterior_probabilities(self.observations, self.intended_p_alloc)

    def time_sequential_p_values(self):
        st.sequential_p_values(self.observations, self.intended_p_alloc)

    def time_sequential_bayes_factors(self):
        st.sequential_bayes_factors(self.observations, self.intended_p_alloc)

    def time_srm_test(self):
        st.srm_test(self.observations, self.intended_p_alloc)
