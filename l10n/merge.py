import os
from pathlib import Path
from typing import Dict

import polib

def merge(_base: Dict[str, polib.POEntry], *dicts_to_merge: Dict[str, polib.POEntry]) -> Dict[str, polib.POEntry]:
    _base_dict = _base.copy()
    for dict_to_merge in dicts_to_merge:
        _base_dict.update(dict_to_merge)
    return _base_dict

migration_path = Path('migration')

base_po = polib.pofile(str(migration_path / 'unchanged.po'))

base_dict = {ent.msgid : ent
             for ent in base_po}

changed_redirected = {ent.msgid : ent
                    for ent in polib.pofile(str(migration_path / 'changed' / 'redirected.po')) if not ent.fuzzy}

changed_redirected_vague = {ent.msgid : ent
                    for ent in polib.pofile(str(migration_path / 'changed' / 'redirected_vague.po')) if not ent.fuzzy}

changed_real = {ent.msgid : ent
                    for ent in polib.pofile(str(migration_path / 'changed' / 'real.po')) if not ent.fuzzy}

added_redirected = {ent.msgid : ent
                    for ent in polib.pofile(str(migration_path / 'added' / 'redirected.po')) if not ent.fuzzy}

added_real = {ent.msgid : ent
                    for ent in polib.pofile(str(migration_path / 'added' / 'real.po')) if not ent.fuzzy}

merged_dict = merge(
    base_dict,
    changed_redirected, changed_redirected_vague, changed_real,
    added_redirected, added_real
)

merged_po = polib.POFile()

for _v in merged_dict.values():
    merged_po.append(_v)

#merged_po.metadata
merged_po.sort()

merged_path = migration_path / 'merged'

os.makedirs(merged_path, exist_ok=True)

merged_po.save(str(merged_path / 'merged.po'))