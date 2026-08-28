from wordfreq import iter_wordlist

def get_solution_pool(pool_size=2000, word_length=5):
    """Get most common {word_length}-letter words to use as a full answer pool."""
    pool = []
    for word in iter_wordlist('en'):
        if len(word) == word_length and word.isalpha():
            pool.append(word)
        if len(pool) == pool_size:
            break
    return pool