# coding=utf-8
from __future__ import unicode_literals, print_function
import unicodedata

from clldutils.dsv import reader
from clldutils.text import strip_chars

from clldutils.path import Path
from pylexibank.dataset import Metadata
from pylexibank.dataset import Dataset as BaseDataset


class Dataset(BaseDataset):
    dir = Path(__file__).parent

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
        cmap = {c['NUMBER']: c for c in self.concepts}
        lmap = {l['ID']: l for l in self.languages}
        with self.cldf as ds:
            for p in self.raw.glob('*.csv'):
                lid = p.stem.split('-')[1]
                if lid in lmap:
                    ds.add_language(
                        ID=lid,
                        Glottocode=self.glottolog.glottocode_by_iso.get(lmap[lid]['ISO']),
                        ISO639P3code=lmap[lid]['ISO'],
                        Name=lmap[lid]['NAME'])
                    for item in reader(p, dicts=True):
                        concept = cmap.get(item['BNC ID'])
                        if item['Phonetic']:
                            ds.add_concept(
                                ID=item['BNC ID'].replace('.', '-'),
                                Name=item['Gloss'],
                                Concepticon_ID=concept['CONCEPTICON_ID'] if concept else None)
                            ds.add_lexemes(
                                Language_ID=lid,
                                Parameter_ID=item['BNC ID'].replace('.', '-'),
                                Value=unicodedata.normalize('NFC', item['Phonetic']))
