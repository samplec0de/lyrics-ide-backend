import pytest
from httpx import AsyncClient

from app.models import WordMeaningModel
from tests.conftest import DBSession


@pytest.mark.parametrize(
    "word, expected",
    [
        pytest.param("кот", ["Самец кошки", "О похотливом, сластолюбивом мужчине"], id="cat"),
        pytest.param("телевизор", ["Аппарат для приема телевизионных передач, телевизионный приемник"], id="tv"),
        pytest.param("абвгджц", [], id="no meanings"),
    ],
)
@pytest.mark.asyncid
async def test_word_meaning(word: str, expected: list[str], db_session: DBSession, authorized_client: AsyncClient):
    words = [
        WordMeaningModel(word_meaning_id=1, word="Кот", meaning="Самец кошки", first_character="к"),
        WordMeaningModel(
            word_meaning_id=2,
            word="Кот",
            meaning="О похотливом, сластолюбивом мужчине",
            first_character="к"
        ),
        WordMeaningModel(
            word_meaning_id=3,
            word="Телевизор",
            meaning="Аппарат для приема телевизионных передач, телевизионный приемник",
            first_character="т"
        ),
    ]
    for dict_word in words:
        db_session.add(dict_word)
    await db_session.commit()

    response = await authorized_client.get(
        "/words/meaning",
        params={"word": word},
    )
    assert response.status_code == 200
    expected_response = [{"meaning": meaning, "source": "Ojegov"} for meaning in expected]
    assert response.json() == expected_response
