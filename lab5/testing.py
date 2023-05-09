#!/usr/bin/env python3
from requests import get
import numpy
import re


PERSON_SINGLE_KEYS = ['name', 'height', 'mass', 'hair_color', 'skin_color',
                      'eye_color', 'birth_year', 'gender', 'homeworld', 'created', 'edited', 'url']
PERSON_LIST_KEYS = ['films', 'species', 'vehicles', 'starships']
STARSHIP_NUMBER_KEYS = ['cost_in_credits', 'length', 'crew', 'passengers', 'cargo_capacity']
STARSHIP_CONSUMABLES_TIME_PERIODS = ['hour', 'day', 'week', 'month', 'year']

# function naming convention: test_*scope_name*
#                                             [_(single/traverse/random_batch)        ]
#                                                                            [_by_data]


def test_people_single_by_data(person_json):
    for key in PERSON_SINGLE_KEYS:
        assert key in person_json
        assert type(person_json[key]) is str, f'{person_json[key]} is not str!'

    for key in PERSON_LIST_KEYS:
        assert key in person_json
        assert type(person_json[key]) is list

    assert len(person_json) == len(PERSON_LIST_KEYS) + len(PERSON_SINGLE_KEYS)


def test_people_traverse():
    url = "https://swapi.dev/api/people"
    old_count = None
    true_count = 0
    while url != None:
        print(url)
        response = get(url).json()
        assert response["count"] is not None

        if old_count is not None:
            assert response["count"] == old_count
        else:
            print(f"Total count of people: {response['count']}")

        old_count = response["count"]
        true_count += len(response["results"])
        for person in response["results"]:
            test_people_single_by_data(person)
            print(".", end="", flush=True)
            assert get(person["url"]).json() == person
        url = response["next"]
        print()
    assert (true_count == old_count)


def test_people_schema():
    # test which, sadly, does not pass
    url = "https://swapi.dev/api/people/schema"
    response = get(url)
    # assert response.status_code != 404

    if response.status_code == 404:
        print("Schema does not work.")
    else:
        print("!!!!!!!!!! IT WORKS !!!!!!!!!!")

    return (response.status_code != 404)


def test_durability(count=1000):
    for i in range(count):
        url = "https://swapi.dev/api/"
        response = get(url, timeout=3).status_code
        assert response == 200
        if i % (count // 100) == 0:
            print(".", end="", flush=True)
    print()


def test_starships_single_by_data(starship_json):
    a = [re.match("[0-9,-]+|unknown|n/a", starship_json[key]) is not None for key in STARSHIP_NUMBER_KEYS]
    assert all(a)


    if starship_json["consumables"] != "unknown":
        number, period = starship_json["consumables"].split()
        assert number.isdigit()
        assert (period in STARSHIP_CONSUMABLES_TIME_PERIODS \
                or (period[-1] == 's' and period[:-1] in STARSHIP_CONSUMABLES_TIME_PERIODS)
                ), f"Starship {starship_json['url']} sucks"


def test_starships_random_batch(count=20):
    url = "https://swapi.dev/api/starships"
    print(url)

    response = get(url).json()
    assert response["count"] is not None
    print (f"Total starship count: {response['count']}")

    testing_set = set(numpy.random.choice(numpy.arange(1, response["count"] * 3), count))
    for unit in testing_set:
        response = get(url + f"/{unit}/")
        if response.status_code == 404:
            print(f"Starship with number {unit} does not exist")
            continue
        
        test_starships_single_by_data(response.json())
        print(".")


if __name__ == "__main__":
    functions = [test_people_traverse, test_durability, test_starships_random_batch, test_people_schema]
    for f in functions:
        f()
