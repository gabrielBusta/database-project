import os
import sys
import requests
from utilities import uprint, load_json, write_json

def main():
    countries = load_json('./countries.json')

    time_zones = extract_unique_time_zones(countries)

    languages = extract_unique_languages(countries)

    TimeZone_objects = create_TimeZone_objects(time_zones)

    Language_objects = create_Language_objects(languages)

    # write new TimeZone objects into our database
    for TimeZone_object in TimeZone_objects:
        TimeZone_object.save()

    # write new Language objects into our database
    for Language_object in Language_objects:
        Language_object.save()

    # the Language and TimeZone objects must be present
    # in the database before we create the Country objects
    Country_objects = create_Country_objects(countries)

    for Country_object in Country_objects:
        Country_object.save()


def create_Country_objects(contries):
    Country_objects = []

    for country in contries:
        name = country['name']
        alpha2Code = country['alpha2Code']
        region = country['region']
        subregion = country['subregion']
        population = country['population']

        Country_object = models.Country.objects.create(name=name,
                                                       alpha2Code=alpha2Code,
                                                       region=region,
                                                       subregion=subregion,
                                                       population=population)

        for timezone in country['timezones']:
            TimeZone_object = models.TimeZone.objects.get(UTC_offset=timezone)
            Country_object.timezones.add(TimeZone_object)

        for language in country['languages']:
            Language_object = models.Language.objects.get(ISO_639_1_code=language)
            Country_object.languages.add(Language_object)

        Country_objects.append(Country_object)

    return Country_objects


def create_Language_objects(languages):
    Language_objects = []

    for language in languages:
        Language_object = models.Language.objects.create(ISO_639_1_code=language)
        Language_objects.append(Language_object)

    return Language_objects


def create_TimeZone_objects(time_zones):
    TimeZone_objects = []

    for time_zone in time_zones:
        TimeZone_object = models.TimeZone.objects.create(UTC_offset=time_zone)
        TimeZone_objects.append(TimeZone_object)

    return TimeZone_objects


def extract_unique_time_zones(countries):
    time_zones = []

    for country in countries:
        for time_zone in country['timezones']:
            if time_zone not in time_zones:
                time_zones.append(time_zone)

    return time_zones


def extract_unique_languages(countries):
    languages = []

    for country in countries:
        for language in country['languages']:
            if language not in languages:
                languages.append(language)

    return languages


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    import django
    django.setup()
    from app import models

    if len(sys.argv) == 2:
        if sys.argv[1] == 'fetch':
            response = requests.get('https://restcountries.eu/rest/v1/all')
            write_json(response.json(), './countries.json')

    main()
