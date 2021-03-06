# Internship Homework 2021

## Usage

This is packaged with [Poetry](https://github.com/python-poetry/poetry), and so all dependencies can be installed with `poetry install`. No `requirements.txt` is given as there are no dependencies for normal usage, only pytest and black for development. The code is all formatted using [Black](https://github.com/psf/black). The main `WordSearch` class can be used with a simple `from pexhomework import WordSearch`.

## The Problem

The problem, as I understand it, is to take a string of virtually unlimited length and given a row length `n`, convert it into a matrix of `nxn` size, and then be able to efficiently check if a given "word" (a string) exists from left-to-right within a row, or from top-to-bottom within a column. The ability to search through this matrix must be done without the knowledge of what words will be searched.

This problem may seem trivial at first but poses significant problems when scaled up to a large size (10000x10000 matrix and 1000000 words).

I've interpreted the problem to mean that the grid will always be square, so the rows and columns are of equal length in the grid. With the current implementation it is not too difficult to change the behaviour if the grid is not square.

## First Considerations

On first glance it may seem like you should convert the string to a 2D array as this is how we are presented the problem, however on further inspection when converting a string of extremely large size (such as with a 10000x10000 matrix which will give a string of length 100000000) we run into problems with how Python creates lists due to their dynamic size and how this works with the amount of memory it uses.

Further, the spec document does not outline how the row length should be defined within the `WordSearch` object, only that it should exist. I've taken it to mean that it's an attribute of the `WordSearch` object but it would be trivial to change the implementation to accept it in other ways.

## My Approaches

### First (less efficient) Approach

You can see it [here](https://github.com/matthew-jones-uk/internship-homework-2021/blob/b89084602bfec32ec6122a60c4a1d15fe508bfb6/pexhomework/word_search.py).

#### Overview

Using the initial implementation we're given I first decided to go for a Pythonic slicing approach. The way I implemented this was, when given the word to search, to iterate through the grid string's letters and check when the first letter of the word is detected. The index of our current position is known as `i`. On detection we compute the index that the end of the word should be at when the word is from left-to-right and when the word is from top-to-bottom. To do the former we simply do `i + length of word`. To do the latter is a bit more complex - we do `i + ((length of word - 1) * the row length) + 1`. Notice in both cases we get the index after the last letter of the word, this is due to how Python slicing works and how we use it later.

Now we have these two indexes we get the slices from `i:right-index` or and from the slice `i:bottom-index:row-length`. These slices yield the letters from index i (inclusive) to the right index (exclusive) and the index i (inclusive) to the bottom index (exclusive) with a step of the row length, meaning we skip `n` indexes before taking the letter at our next index. We check if the letters returned from this slice on the grid equals the search word, if not we continue iterating. If it does then we continue with more checks:

- For the top-to-bottom slice we simply check if the `end index - 1` (because we've calculated the index after the final letter) is within the grid string, if it is then we return `True`, as the search word is on a column within the grid going top-to-bottom.

- For the left-to-right slice we check if the `end index - 1` is within the grid but we also check if the start index and end index are on the same row (as for a word to be left-to-right all letters need to be on the same row). We need to do this as the grid is still in the flattened form and so we need to have some idea of 2D-ness, a.k.a. the rows. For this, we simply integer divide both indexes by the row length and check if the output is the same. If all checks work, then we return `True`, as the word is in the grid.

When we have iterated to the end of the grid we return `False` as this means the search word has not been detected in the grid string.

#### Issues

I thought this method would be fast due to the speed of slicing in Python however it turns out to be quite slow at scale. I assume this due to slicing not being quite as fast as I thought and although the time-complexity is O(n) we are still iterating through every position in the grid using a for loop and running multiple checks that require some some computation in each iteration.

#### Benefits

This approach allows for easy expansion if we want to check right-to-left or bottom-to-top. It also has the space complexity of O(n). It requires no preprocessing.

### Second (faster) Approach

This is the approach that is currently used.

#### Overview

Due to the problems with the previous approach I decided to try some preprocessing to reduce the amount of computation and iteration done when the search function is called. Instead of doing the left-to-right and top-to-bottom checks together for each letter of the grid in a for loop I instead put the grid in row-major and column-major order, but in a 1D flattened form. I use a `bytearray` here but could probably use a string instead, I wasn't sure of the performance implications of concatenation of strings vs extending bytearrays when building the column-major form or how much memory a normal string would use vs a bytearray with ascii characters.

Row-major order is simply what the grid is already in when we're given, so all I do is convert it to ASCII for the bytearray. This isn't a problem as we're told the characters can only be a-z.

To convert the grid into column-major order as a 1D array we iterate through the number of columns that exist according to the row length and sequentially add each column to the bytearray. This means that within the array we'll have each column from top-to-bottom sequentially after each other, just like how the rows are. This essentially means we now need to check two grids, but in only one direction.

The preprocessing is not done when the `WordSearch` object is created as the row length is not given at this time and could change at any time. Instead, we check if the row length has changed since a search has been previously done (or if a search has been done before) and if so then run the preprocessing (but only for the column-major order as the row-major doesn't change anyway). This means that on first search this approach may be slower than the previous, however when one object is used for many different word strings (like in the given example), it is much faster.

The word search method implementation is simple due to the preprocessing. We do the above check to see if we need to run preprocessing again, then also check if the given search word is longer than the row length (this should also apply for column length as we're testing with square matrices). For both order forms we then run the Python function `find()` on the grid to get the index where a match is found. We then get the end index (`found index + length of word - 1`) and check if they are on the same "row". This is done in the same way as the previous approach, by doing integer divison on the start and end index by dividing them by the row length, checking if the output is the same. This works works for both left-to-right and top-to-bottom approaches due to the manipulation we've done of the grid in our preprocessing. If the integer divison check is false then we run `find()` from the index after the computed end of word index to check the rest of the grid, essentially starting the process again but with a now smaller grid. If it is true then we return `True` as the serach word exists in valid index positions.

If at any time the `find()` returns `-1` (no match found) then we break the loop and check the next form. If no match is found in either grid form then we return `False`.

#### Issues

To be able to do this check from right-to-left or bottom-to-top we'd have to do more preprocessing, using more space. It currently has the space complexity of O(2n) and so with (extremely) large grids we may run out of memory, but this is somewhat negated by the usage of ascii bytearrays vs a traditional list.

#### Benefits

If the words being searched do not exist in any form in the grid then the built-in `find()` function will return `-1` extremely quickly. The algorithm will therefore be extremely good at dealing with one grid, but an extremely large amount of words being checked. Even if the word exists in an invalid form in the grid then the built-in sort function is still extremely fast and the computation required to check if the position is valid is both less than the previous method and will only be called when there is a match, less than every single position in the grid.

#### Optimisations

Instead of running `find()` multiple times after an invalid match has been made we could instead use a function that returns the indexes of all matches that exist. A regex could be used here but I'm not convinced the slowness of the regex module is worth it. It would probably depend on the number of words being checked that are not in the grid in any form (i.e. when `find()` returns `-1`). We cannot use the `in` keyword as it returns no index for a match - we require this to check if the word is in a valid position and if not, if the word exists in a valid position after this.

## Testing

Testing this is not as easy as immediately obvious. You can trivially test using precrafted grids (as done with `test_search_4x4()`, `test_search_8x8()`, and `test_search_10x10()`) but this is not necessarily reflective of all possible situations.

Further, it is not practical to test with larger precrafted grids as they cannot easily be done by hand and so will require an implementation to create them - so why not simply test with the implemenation?

An autogenerating grid test implementation has a few problems that aren't immediately obvious:

- How do we know what are words?

    We can use a built-in dictionary such as the example `/usr/share/dict/words` or we can download a larger dictionary if we want to test more words. We do run into other problems with such dictionaries, namely compound words.

- Compound words

    These need to be a consideration in an implementation that autogenerates the grid and the words to search from a dictionary due to words that may exist inside another word. For example, say we're autogenerating a (small) grid and randomly pick the word "notebook" to include. We will then take a note that we've added this word into the grid and then also add it into the words to search for. However, if we're using words from a dictionary to check for false positives, i.e. words that return that they exist in the grid when they don't, then the words "note" and "book" may appear, both words that exist within the word "notebook" and would therefore return true, but we may not have necessarily taken note of this.

- Accidental words being created

    Say our autogenerating implementation simply fills all empty spaces with a word when possible, how do we know two words back to back (or side to side) won't produce another word? For example, the words "cook" and "book" placed one after another on a single row in a grid will produce the word "cookbook", a word that may exist in our dictionary and that would cause problems.

We can combat these problems by not trying to autogenerate a crossword from a dictionary for our tests - we can just generate a grid full of random letters and create "words" out of that grid. We can even take it a step further by creating random strings of letters and appending a letter we know is definitely not in the grid (which we can achieve by taking a letter out of the grid). I've implemented this sort of test with an configurable autogeneration method when given a size and two tests that use this method at different sizes. This approach is not quite as good as the above all-inclusive method of autogeneration I discussed above, but is significantly faster (and simpler) to implement.

## Benchmarks

On my laptop with an i5-8250u and Linux it takes about 4 seconds to generate and search a 1000x1000 grid with 10k words being searched, 5k of which are in the grid, 5k are not.

The 10Kx10K grid with a million words takes significantly longer and I haven't been able to run it to completion yet.

## Bonus Question

### How would we take advantage of a multicore system?

With the currently implemented preprocessing approach the most obvious way to take advantage of a multicore system is to parallelise the processing of the top-to-bottom and left-to-right grids as they essentially act as two different grids and we're simply processing them sequentially currently. However, due to this being a CPU limited workload and how Python works with its GIL it would be best to implement this with the `multiprocessing` module as this utilises separate processes, opposed to threads. For large operations this may be better but due to the overhead added by such an approach for smaller searches simply leaving it single-threaded may be optimal.

To implement this with multiprocessing we can modify `is_present()` to utilise two processes for format of grid, instead of the sequential for loop.

This will only take advantage of dual cores due to there only being two processes.
