# coding=utf-8
from __future__ import unicode_literals, print_function
import unicodedata

import attr
from clldutils.dsv import reader
from clldutils.text import strip_chars

from clldutils.path import Path
from pylexibank.dataset import Metadata
from pylexibank.dataset import Dataset as BaseDataset, Concept as BaseConcept


@attr.s
class Concept(BaseConcept):
    French = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'blenchbenuecongo'
    concept_class = Concept

    def clean_form(self, row, form):
        return strip_chars('-_().', BaseDataset.clean_form(self, row, form) or '').strip()

    def split_forms(self, row, value):
        res = []
        for form in BaseDataset.split_forms(self, row, value):
            if form:
                for variant in form.split('~'):
                    variant = variant.strip()
                    if variant:
                        res.append(variant)
                        break  # only add the first of several variants
        return res

    def cmd_install(self, **kw):
        with self.cldf as ds:
            ds.add_concepts(id_factory=lambda d: d.number.replace('.', '-'))
            lmap = ds.add_languages()
            for p in self.raw.glob('*.csv'):
                lid = p.stem.split('-')[1]
                if lid in lmap:
                    for item in reader(p, dicts=True):
                        if item['Phonetic']:
                            ds.add_lexemes(
                                Language_ID=lid,
                                Parameter_ID=item['BNC ID'].replace('.', '-'),
                                Value=unicodedata.normalize('NFC', item['Phonetic']))
