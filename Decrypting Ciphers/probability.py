import numpy as np

class CharCounter:
    """
    Class responsible for counting character occurrences and transitions from a given set of tokens.
    """

    def __init__(self, train_tokens: list[str]):
        """
        Initializes the CharCounter instance and trains character probabilities and transitions.

        Args:
            train_tokens (list[str]): A list of tokens to train the character probabilities and transitions.
        """
        self.pi, self.M = self._train(train_tokens)

    def _update_pi(self, pi, ch_indices):
        """
        Updates the initial character probabilities based on the character indices.

        Args:
            pi (np.array): The initial character probabilities.
            ch_indices (np.array): An array of character indices representing the token.

        Returns:
            None
        """
        pi[ch_indices[0]] += 1

    def _update_transition_matrix(self, M: np.array, ch_indices: np.array):
        """
        Updates the transition matrix based on the character indices.

        Args:
            M (np.array): The transition matrix representing character transitions.
            ch_indices (np.array): An array of character indices representing the token.

        Returns:
            None
        """
        M[ch_indices[:-1], ch_indices[1:]] += 1

    def _train(self, tokens: list[str]) -> tuple[np.array]:
        """
        Trains the character probabilities and transitions based on a list of tokens.

        Args:
            tokens (list[str]): A list of tokens to train the character probabilities and transitions.

        Returns:
            tuple[np.array]: A tuple containing the initial character probabilities and the transition matrix.
        """
        pi, M = np.zeros(26), np.ones((26, 26))
        for token in tokens:
            ch_indices = np.array([ord(ch) - 97 for ch in token])
            self._update_pi(pi, ch_indices)
            self._update_transition_matrix(M, ch_indices)

        pi /= len(tokens)
        M /= M.sum(axis=1, keepdims=True)
        return pi, M


class ProbabilityCalculator:
    """
    Class responsible for calculating the probability of a sequence of tokens based on the trained character probabilities and transitions.
    """

    def __init__(self, counter: CharCounter):
        """
        Initializes the ProbabilityCalculator instance.

        Args:
            counter (CharCounter): The CharCounter instance containing character probabilities and transitions.
        """
        self.counter = counter
        self.k = 0.1

    def _get_token_prob(self, token: str):
        """
        Calculates the log-probability of a token based on the trained character probabilities and transitions.

        Args:
            token (str): The token for which to calculate the log-probability.

        Returns:
            float: The log-probability of the token.
        """
        ch_indices = np.array([ord(ch) - 97 for ch in token])
        logp = np.log(self.counter.pi[ch_indices[0]])
        logp += np.sum(np.log(self.counter.M[i, j]) for i, j in zip(ch_indices[:-1], ch_indices[1:]))
        return logp

    def get_prob(self, tokens: list[str]) -> float:
        """
        Calculates the probability of a list of tokens based on the trained character probabilities and transitions.

        Args:
            tokens (list[str]): A list of tokens for which to calculate the probability.

        Returns:
            float: The probability of the list of tokens.
        """
        return sum(self._get_token_prob(token) for token in tokens)
