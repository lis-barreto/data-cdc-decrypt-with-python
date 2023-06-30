import pytest
from cdc_decrypt.handler import parse_filename

@pytest.mark.parametrize("s3_key, expected", [
    ("folder/app_skywalker.AbbGZ31sTQ7U9AYPR6ykP28CwW.jedi/ds=2023-01-01/app_skywalker.AbbGZ31sTQ7U9AYPR6ykP28CwW.jedi+0+0000000001.json.gz",
     ("app_skywalker", "jedi", "2023-01-01", "app_skywalker.AbbGZ31sTQ7U9AYPR6ykP28CwW.jedi+0+0000000001")),
    ("folder/app_vader.AbbGZ31sTQ7U9AYPR6ykP28CwW.sith/ds=2023-02-02/app_vader.AbbGZ31sTQ7U9AYPR6ykP28CwW.sith+0+0000000002.json.gz",
     ("app_vader", "sith", "2023-02-02", "app_vader.AbbGZ31sTQ7U9AYPR6ykP28CwW.sith+0+0000000002")),
    ("folder/app_yoda.AbbGZ31sTQ7U9AYPR6ykP28CwW.jedi/ds=2023-03-03/app_yoda.AbbGZ31sTQ7U9AYPR6ykP28CwW.jedi+0+0000000003.json.gz",
     ("app_yoda", "jedi", "2023-03-03", "app_yoda.AbbGZ31sTQ7U9AYPR6ykP28CwW.jedi+0+0000000003")),
    ("folder/app_ren.AbbGZ31sTQ7U9AYPR6ykP28CwW.sith/ds=2023-04-04/app_ren.AbbGZ31sTQ7U9AYPR6ykP28CwW.sith+0+0000000004.json.gz",
     ("app_ren", "sith", "2023-04-04", "app_ren.AbbGZ31sTQ7U9AYPR6ykP28CwW.sith+0+0000000004")),
    ("folder/app_leia.AbbGZ31sTQ7U9AYPR6ykP28CwW.rebel/ds=2023-05-05/app_leia.AbbGZ31sTQ7U9AYPR6ykP28CwW.rebel+0+0000000005.json.gz",
     ("app_leia", "rebel", "2023-05-05", "app_leia.AbbGZ31sTQ7U9AYPR6ykP28CwW.rebel+0+0000000005"))
])
def test_parse_filename(s3_key, expected):
    application, table, ds, filename = parse_filename(s3_key)
    assert (application, table, ds, filename) == expected
