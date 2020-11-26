from django.db import models


class Pokemon(models.Model):
    """Покемон. """
    title = models.CharField(max_length=100, verbose_name="Название")
    title_en = models.CharField(max_length=100, blank=True, verbose_name="Английское название")
    title_jp = models.CharField(max_length=100, blank=True, verbose_name="Японское название")
    image = models.ImageField(upload_to='pokemon', null=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Краткое описание")
    previous_evolution = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                           related_name='next_evolution', verbose_name="Из кого эволюционировал")


    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Объект покемон на карте. """
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Вид покемона")
    lat = models.FloatField(null=True, blank=True, verbose_name="Широта")
    lon = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Появится в")
    disappeared_ar = models.DateTimeField(null=True, blank=True, verbose_name="Исчезнет в")
    level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
    health = models.IntegerField(null=True, blank=True, verbose_name="Здоровье")
    strength = models.IntegerField(null=True, blank=True, verbose_name="Сила")
    defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    stamina = models.IntegerField(null=True, blank=True, verbose_name="Выносливость")

    def __str__(self):
        return f'{self.pokemon} № {self.id}'




