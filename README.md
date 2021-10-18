# Internship Homework 2021

## Usage

This is packaged with Poetry, and so all dependencies can be installed with `poetry install`. Alternatively, a `requirements.txt` is provided. The main search can be used with a simple `from pexhomework import WordSearch`.

## The Problem

The problem, as I understand it, is to take a string of virtually unlimited length and given a row length `n`, convert it into a matrix of `nxn` size, and then be able to efficiently check if a given "word" (a string) exists from left-to-right within a row, or from top-to-bottom within a column. The ability to search through this matrix must be done without the knowledge of what words will be searched.

This problem may seem trivial at first but poses significant problems when scaled up to a large size (10000x10000 matrix and 1000000 words).

## Considerations

On first glance it may seem like you should convert the string to a 2D array as this is how we are presented the problem, however on further inspection when converting a string of extremely large size (such as with a 10000x10000 matrix which will give a string of length 100000000) we run into problems with how Python creates lists due to their dynamic size and how this works with the amount of memory it uses.

## My Approaches

### First (less efficient) Approach

You can see it [here](https://github.com/matthew-jones-uk/internship-homework-2021/blob/b89084602bfec32ec6122a60c4a1d15fe508bfb6/pexhomework/word_search.py).

#### Overview

Using the initial implementation we're given I first decided to go for a Pythonic slicing approach. The way I implemented this was, when given the word to search, to iterate through the grid string's letters and check when the first letter of the word is detected. The index of our current position is known as `i`. On detection we compute the index that the end of the word should be at when the word is from left-to-right and when the word is from top-to-bottom. To do the former we take simply do `i + length of word`. To do the latter is a bit more complex - we do `i + ((length of word - 1) * the row length) + 1`. Notice in both cases we get the index after the last letter of the word, this is due to how Python slicing works.

Now we have these two indexes we do a check to see if the slice from `i:right-index` or the slice from `i:bottom-index:row-length`. These slices yield the letters from index i (inclusive) to the right index (exclusive) and the index i (inclusive) to the bottom index (exclusive) with a step of the row length, meaning we skip `n` indexes before taking our next index. We check if the letters returned from this slice on the grid returns the word, if not we continue iterating. If it does then we continue with more checks:

For the top-to-bottom slice we simply check if the end index - 1 (because we've calculated the index after the final letter) is within the grid string, if it is then we return `True`, this word is in the grid.

For the left-to-right slice we also check if the end index - 1 is within the grid but we also check if the start index and end index are on the same row (as for a word to be left-to-right all letters need to be on the same row). We need to do this as the grid is still in the flattened matrix form and so we need to have some idea of 2D-ness, a.k.a. the rows. To do this we simply integer divide both indexes and check if they're the same. If all checks work, then we return `True`, as the word is in the grid.

When we have iterated to the end of the grid we return `False` as this means the word has not been detected in the grid string.

#### Issues

I thought this method would be fast due to the speed of slicing in Python but it turns out to be quite slow at scale. I assume this due to slicing not being quite as fast as I thought and although the time-complexity is O(n) we are still iterating through every position in the grid using a for loop and running multiple checks that require some some computation.

#### Benefits

This approach allows for easy expansion if we want to check right-to-left or bottom-to-top. It also has the space complexity of O(n). It requires no preprocessing.
