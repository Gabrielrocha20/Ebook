import os
import string
from pickletools import optimize
from random import SystemRandom

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image
from utils import utils


class Categoria(models.Model):
    categoria = models.CharField(max_length=40)
    def __str__(self):
        return f'{self.categoria}'

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/',
                               blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(
        default=0, verbose_name='Preço Promo')
    url_produto = models.CharField(max_length=1000, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def get_preco_formatado(self):
        return utils.formata_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return utils.formata_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preço Promocional'

    @staticmethod
    def resize_image(img, new_with=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_with:
            img_pil.close()
            return
        new_height = round((new_with * original_height) / original_width)
        new_img = img_pil.resize((new_with, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                    SystemRandom().choices(
                        string.ascii_letters + string.digits,
                        k=5,
                    )
                )
            self.slug = slugify(f'{self.nome}-{rand_letters}')
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return f'{self.nome}'


# Create your models here.
