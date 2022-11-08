import json

from PIL import Image
from rich.console import RenderableType
from rich.text import Text
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import ListItem, ListView, Static

NUM_POKEMON = 151
POKEMON_DIR = "data/pokemon_pics"


class PokeItem(ListItem):
    def __init__(self, pokemon_name: str = "", pokemon_id: int = 0):
        self.pokemon_id = pokemon_id
        self.pokemon_name = pokemon_name
        super().__init__()

    # def render(self) -> RenderableType:
    #     return f"{self.pokemon_id} {self.pokemon_name}"

    def compose(self) -> ComposeResult:
        yield Static(f"{self.pokemon_id} {self.pokemon_name}")


class PokemonImage(Static):
    pokemon_id = reactive(1)

    def __init__(self, pokemon_id: int) -> None:
        super().__init__()
        self.pokemon_id = pokemon_id

    def watch_pokemon_id(self, id):
        print(id)

    def render(self) -> RenderableType:
        path = f"{POKEMON_DIR}/{self.pokemon_id}.png"
        with Image.open(path) as img:
            height, width = img.height, img.width
            rgba_img = img.convert("RGBA")
            img_text = []
            for y in range(height):
                this_row = []
                for x in range(width):
                    r, g, b, a = rgba_img.getpixel((x, y))
                    this_row.append(("  ", f"on rgb({r},{g},{b})" if a > 0 else ""))
                    should_newline = x % width == 0
                    if should_newline:
                        this_row.append(("\n", ""))

                if not all(t[1] == "" for t in this_row[:-1]):
                    img_text += this_row

            return Text.assemble(*img_text)


#
# class Image(Widget):
#     def render(self) -> RenderableType:
#         from rich_pixels import Pixels
#         return Pixels.from_image_path("data/rick.png")


class Pokedex(App):
    def compose(self) -> ComposeResult:
        with open("data/pokemon_data.json") as f:
            self.poke_info = json.loads(f.read())
        info = self.poke_info
        yield ListView(
            *[PokeItem(pokemon_name=pokemon["name"], pokemon_id=int(pokemon["id"])) for pokemon in info][
             :NUM_POKEMON],
            id="side-list"
        )

        yield PokemonImage(pokemon_id=1)

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        self._select_pokemon(event.item.pokemon_id)

    def on_list_view_selected(self, event: ListView.Selected):
        self._select_pokemon(event.item.pokemon_id)

    def _select_pokemon(self, id: int) -> None:
        self.query_one(PokemonImage).pokemon_id = id


app = Pokedex(css_path="pokeprint.css")
if __name__ == '__main__':
    app.run()

# mapping = {"1": Segment(" ", "on ")}
#
# \u2341223344
#
#
#
#
