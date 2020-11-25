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
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Вид покемона")
    Lat = models.FloatField(null=True, blank=True, verbose_name="Широта")
    Lon = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    Appeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Появится в")
    Disappeared_ar = models.DateTimeField(null=True, blank=True, verbose_name="Исчезнет в")
    Level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
    Health = models.IntegerField(null=True, blank=True, verbose_name="Здоровье")
    Strength = models.IntegerField(null=True, blank=True, verbose_name="Сила")
    Defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    Stamina = models.IntegerField(null=True, blank=True, verbose_name="Выносливость")

    def __str__(self):
        return f'{self.Pokemon} № {self.id}'




