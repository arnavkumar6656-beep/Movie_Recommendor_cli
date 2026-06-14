# Movie Recommender CLI

A command-line tool that recommends similar movies based on a content-based recommendation system using **TF-IDF vectorization** and **cosine similarity**.

This project takes a content-based recommendation model (originally built and trained in a Jupyter notebook) and packages it into a usable command-line tool with fuzzy title matching and formatted output.

---

## Features

- **Get recommendations** — pass a movie title, get a ranked list of similar movies with similarity scores
- **Fuzzy matching** — typos and partial titles are automatically matched to the closest movie in the dataset
- **Search** — look up movie titles in the dataset if you're not sure of the exact name
- **Formatted output** — results displayed in a clean table using `rich`

---

## How It Works

1. Movie metadata (genres, keywords, tagline, cast, director) is combined into a single text field for each movie
2. **TF-IDF** (Term Frequency-Inverse Document Frequency) converts this text into numerical feature vectors
3. **Cosine similarity** is computed between every pair of movies, producing a similarity matrix
4. The trained model (movie titles + similarity matrix) is saved using `pickle`
5. The CLI loads this precomputed data and looks up similar movies instantly — no retraining needed at runtime

---

## Installation

```bash
git clone https://github.com/arnavkumar6656-beep/movie-recommender-cli.git
cd movie-recommender-cli
pip install typer rich pandas scikit-learn
```

> **Note:** This repo uses [Git LFS](https://git-lfs.github.com) to store `similarity.pkl` (~176MB). Make sure Git LFS is installed before cloning:
> ```bash
> git lfs install
> ```

---

## Usage

### Get recommendations

```bash
python recommendor.py recommend "Inception"
```

```
Movies similar to 'Inception'
┏━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ # ┃ Title                 ┃ Similarity ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 1 │ Interstellar          │   42.18%   │
│ 2 │ The Prestige          │   38.50%   │
│ ...                                     │
└───┴───────────────────────┴────────────┘
```

Specify how many results to return (default is 5):

```bash
python recommendor.py recommend "Inception" --count 10
```

Fuzzy matching handles typos automatically:

```bash
python recommendor.py recommend "Inceptio"
# → Did you mean 'Inception'? Showing results for that.
```

### Search for a movie title

```bash
python recommendor.py search "spider"
```

```
Possible matches for 'spider':
  • Spider-Man
  • Spider-Man 2
  • Spider-Man 3
  • The Amazing Spider-Man
```

---

## Project Structure

```
movie-recommender-cli/
├── recommendor.py    ← CLI entry point — recommend and search commands
├── movies.pkl        ← Pickled dataframe: movie index + title
├── similarity.pkl    ← Precomputed cosine similarity matrix (tracked via Git LFS)
└── README.md
```

---

## Tech Stack

| Component | Library |
|---|---|
| CLI framework | [`typer`](https://typer.tiangolo.com/) |
| Terminal output | [`rich`](https://github.com/Textualize/rich) |
| Data handling | `pandas` |
| Vectorization & similarity | `scikit-learn` |
| Fuzzy matching | `difflib` (built-in) |
| Model persistence | `pickle` (built-in) |

---

## Future Improvements

- [ ] Regenerate `.pkl` files from `movies.csv` via a setup script instead of committing large binaries
- [ ] Add poster/overview display for recommended movies
- [ ] Export recommendations to a file (CSV/JSON)
- [ ] Package as an installable CLI command (`pip install .`) so it can be run as `recommend "Inception"` from anywhere
