# recommend.py
import typer
import pickle
import difflib
from rich import print as rprint
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

titles = movies['title'].tolist()


def find_closest_title(query: str) -> str | None:
    matches = difflib.get_close_matches(query, titles, n=1, cutoff=0.5)
    return matches[0] if matches else None


@app.command()
def recommend(movie: str, count: int = 5):
    """Recommend similar movies based on a given title."""
    matched_title = find_closest_title(movie)

    if not matched_title:
        rprint(f"[red]No movie found matching '{movie}'.[/red]")
        raise typer.Exit()

    if matched_title.lower() != movie.lower():
        rprint(f"[yellow]Did you mean '{matched_title}'? Showing results for that.[/yellow]\n")

    # Use the CSV's 'index' column, matching the notebook's logic
    movie_index = movies[movies['title'] == matched_title]['index'].values[0]
    similarity_score = list(enumerate(similarity[movie_index]))
    sorted_similar = sorted(similarity_score, key=lambda x: x[1], reverse=True)[1:count + 1]

    table = Table(title=f"Movies similar to '{matched_title}'", header_style="bold blue")
    table.add_column("#", justify="center")
    table.add_column("Title", style="bold")
    table.add_column("Similarity", justify="center")

    for rank, (idx, score) in enumerate(sorted_similar, start=1):
        title = movies[movies['index'] == idx]['title'].values[0]
        table.add_row(str(rank), title, f"{score:.2%}")

    console.print(table)


@app.command()
def search(query: str):
    """Search for a movie title in the dataset."""
    matches = difflib.get_close_matches(query, titles, n=5, cutoff=0.3)
    if not matches:
        rprint(f"[red]No matches found for '{query}'.[/red]")
        raise typer.Exit()
    rprint(f"[bold]Possible matches for '{query}':[/bold]")
    for m in matches:
        rprint(f"  • {m}")


if __name__ == "__main__":
    app()