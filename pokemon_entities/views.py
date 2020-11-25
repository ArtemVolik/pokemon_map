import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.all():
        if pokemon_entity.Pokemon.image:
            add_pokemon(
                folium_map, pokemon_entity.Lat, pokemon_entity.Lon,
                pokemon_entity.Pokemon.title, request.build_absolute_uri(pokemon_entity.Pokemon.image.url))

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.image.url,
                'title_ru': pokemon.title,
                })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    if requested_pokemon:
        pokemon = {
            "pokemon_id": requested_pokemon.id,
            "title_ru": requested_pokemon.title,
            "title_en": requested_pokemon.title_en,
            "title_jp": requested_pokemon.title_jp,
            "description": requested_pokemon.description,
            "img_url": requested_pokemon.image.url
        }
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    if requested_pokemon.previous_evolution:
        previous_evolution = {
            "title_ru": requested_pokemon.previous_evolution.title,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": requested_pokemon.previous_evolution.image.url
        }
        pokemon['previous_evolution'] = previous_evolution

    #Вариант1
    related_pokemons = requested_pokemon.next_evolution.all()
    if related_pokemons:
        related_pokemon = related_pokemons[0]
        next_evolution = {
                        "title_ru": related_pokemon.title,
                        "pokemon_id": related_pokemon.id,
                        "img_url": related_pokemon.image.url
                        }
        pokemon['next_evolution'] = next_evolution
    # Вариант 2
    # if Pokemon.objects.filter(previous_evolution=requested_pokemon):
    #     next_pokemon = Pokemon.objects.get(previous_evolution=requested_pokemon)
    #     next_evolution = {
    #             "title_ru": next_pokemon.title,
    #             "pokemon_id": next_pokemon.id,
    #             "img_url": next_pokemon.image.url
    #             }
    #     pokemon['next_evolution'] = next_evolution


    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(Pokemon_id=pokemon_id):
        add_pokemon(
            folium_map, pokemon_entity.Lat, pokemon_entity.Lon,
            pokemon_entity.Pokemon.title, request.build_absolute_uri(pokemon_entity.Pokemon.image.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
