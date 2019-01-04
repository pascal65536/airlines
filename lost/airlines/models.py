from django.db import models


# Create your models here.
class Airlines(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    country = models.CharField(verbose_name='Страна', max_length=30)
    birthday = models.CharField(verbose_name='Дата основания', max_length=50, null=True, blank=True)
    birthday_full = models.BooleanField(verbose_name='Точная дата основания?', default=False)
    death = models.DateTimeField(verbose_name='Точная дата закрытия', null=True, blank=True)
    death_full = models.BooleanField(verbose_name='Точная дата закрытия?', default=False)
    fleet_size = models.CharField(verbose_name='Число самолётов', max_length=50)
    status = models.CharField(verbose_name='Состояние', max_length=50)
    logo = models.ImageField(verbose_name='Логотип', blank=True)
    picture = models.CharField(verbose_name='Картинка', max_length=150)
    site = models.CharField(verbose_name='Адрес сайта', max_length=50, blank=True)
    wiki = models.CharField(verbose_name='Вики-страница', max_length=150, blank=True)
    created = models.DateTimeField(verbose_name='Создано', null=True, blank=True)
    changed = models.DateTimeField(verbose_name='Изменено', null=True, blank=True)
    deleted = models.DateTimeField(verbose_name='Удалено', null=True, blank=True)

    class Meta:
        db_table = 'airlines'
        verbose_name = 'Авиакомпания'
        verbose_name_plural = 'Авиакомпании'
        ordering = ['-created']

    def __str__(self):
        return self.title

