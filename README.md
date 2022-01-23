# Wordle Experiments

This repo contains a framework for testing automated wordle strategies.  It was
developed and tested using Python3.10.

Word lists came from here:
    https://www.reddit.com/r/wordle/comments/s4tcw8/comment/hstkip2/?utm_source=share&utm_medium=web2x&context=3

To install, set up a virtualenv and activate it.  Then run
```bash
pip install -r requirements.lock
```

To run tests:
```bash
pytest tests/
```

You can also simulate all current strategies from `main.py`.  Note that this
runs in parallel with `joblib` and is set up to use all of your cores:
```bash
python main.py
```

To analyze a strategy's performance, start Jupyter Notebook.
```bash
jupyter notebook
```

This should open in your browser.  Navigate to `Analyze.ipynb` and run all
cells.  The last cell is a histogram showing a distribution of the number of
guesses each strategy took to find the answer.

## Implementing new strategies
Create your new strategies inside of `./wordle/strategies/`.  A strategy is a
subclass of the `wordle.strategies.strategy.Strategy` class.  You need to
implement two methods:
* `make_guess` - This is how your strategy chooses the next word
* `incorporate_feedback` - This is how your strategy updates its state based on
    the most recent guess and feedback from when it was compared to the answer.

## Feedback
When you make a guess in Wordle, the app compares your guess to the hidden word
and displays a status for each character using colors in the UI.  This is a
statistical simulator so we use letter encodings instead.

The feedback statuses are encoded in the `wordle.types.feedback` module.

Statuses:
* `CORRECT` (code `C`, a.k.a. Green) - This character is correct, and in the
    correct position.
* `WRONG_POSITION` (code `P`, a.k.a. Yellow) - The character appears in the
    hidden word, but it is in the wrong position
* `WRONG` (code `X`, a.k.a. Gray) - This character does not appear in the
    hidden word.

One thing to note about `WRONG_POSITION`: if the letters in the guess exceed
the hidden word a `WRONG_POSITION` will be marked as `WRONG`.  Here are some
examples:

```
Hidden word is "ABBEY"
     You guess "KEEPS"
   Feedback is "XPXXX"
```

```
Hidden word is "ELATE"
     You guess "EERIE"
   Feedback is "CXXXC"
```


Source: https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/ 

## TODO
* Create more strategies
* Logging