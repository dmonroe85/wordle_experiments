# Wordle Experiments

This repo contains a framework for testing automated wordle strategies.

Word lists came from here:
    https://www.reddit.com/r/wordle/comments/s4tcw8/comment/hstkip2/?utm_source=share&utm_medium=web2x&context=3

To install, set up a virtualenv and activate it.  Then run
```bash
pip install -r requirements.in
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


## TODO
* CLI args to
    * change number of trials per word
    * total number of trials
    * which strategies run
    * parallelism
* Profile to find bottlenecks and make it faster
* Create more strategies