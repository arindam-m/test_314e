from django.db import models


class VisualData(models.Model):

    class LevelEnum(models.IntegerChoices):
        ZERO = 0, 'Root (Home Page)'
        ONE = 1, 'First'
        TWO = 2, 'Second'
        THREE = 3, 'Third'
        FOUR = 4, 'Fourth'

    url = models.CharField(max_length=256)
    level = models.IntegerField(default=LevelEnum.ZERO,
                                choices=LevelEnum.choices)
    num_of_urls = models.IntegerField()
    data_frequency = models.JSONField()

    def __str__(self):
        return "A VisualData object has been created"
