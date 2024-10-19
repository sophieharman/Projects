import random
import wordle
import numpy as np

def load_words(filen):
    """
    Loads all of the words from the given file, ensuring that they
    are formatted correctly.
    """
    with open(filen, 'r') as file:
        # Get all 5-letter words
        words = [line.strip() for line in file.readlines() if len(line.strip()) == 5]
    return words


def compute_highest_entropy(all_guess_results, allowed_guesses):
    """
    Compute the entropy of each allowed guess.

    Arguments:
        all_guess_results ((n,m) ndarray) - the array found in
            all_guess_results.npy, containing the results of each
            guess for each secret word, where n is the the number
            of allowed guesses and m is number of possible secret words.
        allowed_guesses (list of strings) - list of the allowed guesses
    Returns:
        (string) The highest-entropy guess
    """

    # Initialize Variables
    maxEntropy = 0
    word = ''
    m = len(all_guess_results[0])
    
    # Iterate through Allowed Guesses
    for i, guess in enumerate(all_guess_results):
        _, counts = np.unique(guess, return_counts=True)

        # Calculate Entropy
        prob = counts / m
        entropy = - np.sum([prob * np.log2(prob)])

        # Update Guess with Highest Entropy
        if entropy > maxEntropy:
            maxEntropy = entropy
            word = allowed_guesses[i]

    # Return Guess with Highest Entropy
    return word

def filter_words(all_guess_results, allowed_guesses, possible_secret_words, guess, result):
    """
    Return a filtered list of possible words that are still possible after
    knowing the result of a guess. Also return a filtered version of the array
    of all guess results that only contains the results for the secret words
    still possible after making the guess. This array will be used to compute
    the entropies for making the next guess.

    Arguments:
        all_guess_results (2-D ndarray)
            The array found in all_guess_results.npy,
            containing the result of making any allowed
            guess for any possible secret word
        allowed_guesses (list of str)
            The list of words we are allowed to guess
        possible_secret_words (list of str)
            The list of possible secret words
        guess (str)
            The guess we made
        result (tuple of int)
            The result of the guess
    Returns:
        (list of str) The filtered list of possible secret words
        (2-D ndarray) The filtered array of guess results
    """

    # Convert Result to Base-3 S
    resultUpdate = 0
    for i, word in enumerate(result):
        resultUpdate += 3**i * word
  
    # Filtered List of Guesses
    idx = allowed_guesses.index(guess)
    mask = (all_guess_results[idx] == resultUpdate)
    filteredGuesses = all_guess_results[:, mask]

    # Filtered List of Possible Secret Words
    possible_secret_words = np.array(possible_secret_words)
    filteredSecretWords = possible_secret_words[mask]
    
    return filteredSecretWords, filteredGuesses

def play_game_naive(game, all_guess_results, possible_secret_words, allowed_guesses, word=None, display=False):
    """
    Plays a game of Wordle using the strategy of making guesses at random.

    Return how many guesses were used.

    Arguments:
        game (wordle.WordleGame)
            the Wordle game object
        all_guess_results ((n,m) ndarray)
            The array found in all_guess_results.npy,
            containing the result of making any allowed
            guess for any possible secret word
        possible_secret_words (list of str)
            list of possible secret words
        allowed_guesses (list of str)
            list of allowed guesses

        word (optional)
            If not None, this is the secret word; can be used for testing.
        display (bool)
            If true, output will be printed to the terminal by the game.
    Returns:
        (int) Number of guesses made
    """
    # Initialize the game
    game.start_game(word=word, display=display)

    while True:

        # Check if Game is Finished
        if game.is_finished():
            break

        # Check if there is only one Allowed Guess
        if len(possible_secret_words) == 1:
            guess = possible_secret_words[0]
            game.make_guess(guess)
            break
  
        # Random Guess
        guess = random.choice(allowed_guesses)
        result, count = game.make_guess(guess)

        # Filter List of Possible Words
        possible_secret_words, all_guess_results = filter_words(all_guess_results, allowed_guesses, possible_secret_words, guess, result)

    return count

def play_game_entropy(game, all_guess_results, possible_secret_words, allowed_guesses, word=None, display=False):
    """
    Plays a game of Wordle using the strategy of guessing the maximum-entropy guess.

    Return how many guesses were used.

    Arguments:
        game (wordle.WordleGame)
            the Wordle game object
        all_guess_results ((n,m) ndarray)
            The array found in all_guess_results.npy,
            containing the result of making any allowed
            guess for any possible secret word
        possible_secret_words (list of str)
            list of possible secret words
        allowed_guesses (list of str)
            list of allowed guesses

        word (optional)
            If not None, this is the secret word; can be used for testing.
        display (bool)
            If true, output will be printed to the terminal by the game.
    Returns:
        (int) Number of guesses made
    """
    # Initialize the game
    game.start_game(word=word, display=display)

    while True:
        # Check if Game is Finished
        if game.is_finished():
            break

        # Check if there is only one Allowed Guess
        if len(possible_secret_words) == 1:
            guess = possible_secret_words[0]
        else:
            # Compute Entropies
            guess = compute_highest_entropy(all_guess_results, allowed_guesses)

        result, count = game.make_guess(guess)

        # Filter List of Possible Words
        possible_secret_words, all_guess_results = filter_words(all_guess_results, allowed_guesses, possible_secret_words, guess, result)

    return game.guess_ct


def compare_algorithms(all_guess_results, possible_secret_words, allowed_guesses, n=20):
    """
    Compare the naive algorithm's performance with the entropy algorithm's performance by
    running n simulations on each.

    Arguments:
        all_guess_results ((n,m) ndarray)
            The array found in all_guess_results.npy,
            containing the result of making any allowed
            guess for any possible secret word
        possible_secret_words (list of str)
            list of possible secret words
        allowed_guesses (list of str)
            list of allowed guesses
        n (int)
            Number of games to run
    Returns:
        (float) - average number of guesses needed by naive algorithm
        (float) - average number of guesses needed by entropy algorithm
    """

    game = wordle.WordleGame()

    naive_guesses = []
    entropy_guesses = []
    for i in range(n):
        naive = play_game_naive(game, all_guess_results, possible_secret_words, allowed_guesses, word=None, display=False)
        strategy = play_game_entropy(game, all_guess_results, possible_secret_words, allowed_guesses, word=None, display=False)

        # Append Counts
        naive_guesses.append(naive)
        entropy_guesses.append(strategy)

    return np.mean(naive_guesses), np.mean(entropy_guesses)
