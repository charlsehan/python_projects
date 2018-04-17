"""Count words."""

def count_words(s, n):
    """Return the n most frequently occuring words in s."""

    # TODO: Count the number of occurences of each word in s

    # TODO: Sort the occurences in descending order (alphabetically in case of ties)

    # TODO: Return the top n words as a list of tuples (<word>, <count>)

    wordList = s.split()
    wordDict = { word:wordList.count(word) for word in set(wordList) }
    print wordList
    print wordDict

    top = wordDict.items()
    print top
    top.sort()
    print top
    top.sort(key=lambda t:t[1], reverse=True)
    print top

    top_n = top[:n]
    print top_n

    return top_n

def test_run():
    """Test count_words() with some inputs."""
    print count_words("cat bat mat cat bat cat", 3)
    print count_words("betty bought a bit of butter but the butter was bitter", 3)

if __name__ == '__main__':
    test_run()