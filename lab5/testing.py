#!/usr/bin/env python3
from requests import get


PERSON_SINGLE_KEYS = ['name', 'height', 'mass', 'hair_color', 'skin_color',
                      'eye_color', 'birth_year', 'gender', 'homeworld', 'created', 'edited', 'url']
PERSON_LIST_KEYS = ['films', 'species', 'vehicles', 'starships']


def test_single_person_by_data(person_json):
    for key in PERSON_SINGLE_KEYS:
        assert key in person_json
        assert type(person_json[key]) is str, f'{person_json[key]} is not str!'

    for key in PERSON_LIST_KEYS:
        assert key in person_json
        assert type(person_json[key]) is list

    assert len(person_json) == len(PERSON_LIST_KEYS) + len(PERSON_SINGLE_KEYS)


def test_traverse_people():
    url = "https://swapi.dev/api/people"
    old_count = None
    true_count = 0
    while url != None:
        print(url, flush=True)
        response = get(url).json()
        assert response["count"] is not None

        if old_count is not None:
            assert response["count"] == old_count
        else:
            print(f"Total count of people: {response['count']}")

        old_count = response["count"]
        true_count += len(response["results"])
        for person in response["results"]:
            test_single_person_by_data(person)
            print(".", end="", flush=True)
            assert get(person["url"]).json() == person
        url = response["next"]
        print()
    assert (true_count == old_count)


def test_durability(count=1000):
    for i in range(count):
        url = "https://swapi.dev/api/"
        response = get(url, timeout=3).status_code
        assert response == 200
        if i % (count // 100) == 0:
            print(".", end="", flush=True)
    print()


if __name__ == "__main__":
    test_traverse_people()
    # test_durability()
    test_durability(0)
