# -*- coding:utf-8 -*-
from . import get
from . import process


def search(keyword, **kwargs):
    kwargs.setdefault('convey', False)
    page = get.page(keyword)
    return process.page(page)
