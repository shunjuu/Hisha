import logging
import re
import requests

from ayumi import Ayumi
from datetime import datetime, time
from deprecated import deprecated
try:
    from .queries import SINGLE as SINGLE_QUERY
    from .queries import PAGE as PAGE_QUERY
except:
    from queries import SINGLE as SINGLE_QUERY
    from queries import PAGE as PAGE_QUERY

ANILIST_API_URL = "https://graphql.anilist.co"
KITSU_API_URL = "https://kitsu.io/api/edge/anime?filter[text]="

DEFAULT_ID_ANI = -1
DEFAULT_ID_MAL = -1
DEFAULT_ID_KITSU = -1
DEFAULT_EPISODES = -1
DEFAULT_DURATION = -1
DEFAULT_POPULARITY = -1
DEFAULT_AVERAGE_SCORE = -1
DEFAULT_BANNER_IMAGE = ""
DEFAULT_COVER_IMAGE = ""
DEFAULT_TITLE_USER_PREFERRED = "Unknown"
DEFAULT_TITLE_NATIVE = "不明"
DEFAULT_TITLE_ENGLISH = "Unknown"
DEFAULT_TITLE_ROMAJI = "Unknown"
DEFAULT_STUDIO = "Unknown"
DEFAULT_STUDIO_URL = ""
DEFAULT_START_DATE = time(0)
DEFAULT_END_DATE = time(0)


def extended_get(val, default):
    """
    dict.get() doesn't default if the key's value is None itself.
    """
    return val if val else default


class Hisha:
    """
    Holds all the information of a show fetched by Hisha.
    """

    def __init__(self, **kwargs):
        self._id_ani: int = extended_get(kwargs.get('id_ani'), DEFAULT_ID_ANI)
        self._id_mal: int = extended_get(kwargs.get('id_mal'), DEFAULT_ID_MAL)
        self._id_kitsu: int = extended_get(kwargs.get(
            'id_kitsu'), DEFAULT_ID_KITSU)  # Deprecated
        self._episodes: int = extended_get(
            kwargs.get('episodes'), DEFAULT_EPISODES)
        self._duration: int = extended_get(
            kwargs.get('duration'), DEFAULT_DURATION)
        self._popularity: int = extended_get(
            kwargs.get('popularity'), DEFAULT_POPULARITY)
        self._average_score: int = extended_get(
            kwargs.get('average_score'), DEFAULT_AVERAGE_SCORE)
        self._banner_image: str = extended_get(
            kwargs.get('banner_image'), DEFAULT_BANNER_IMAGE)
        self._cover_image: str = extended_get(
            kwargs.get('cover_image'), DEFAULT_COVER_IMAGE)
        self._title_user_preferred: str = extended_get(kwargs.get(
            'title_user_preferred'), DEFAULT_TITLE_USER_PREFERRED)
        self._title_native: str = extended_get(
            kwargs.get('title_native'), DEFAULT_TITLE_NATIVE)
        self._title_english: str = extended_get(
            kwargs.get('title_english'), DEFAULT_TITLE_ENGLISH)
        self._title_romaji: str = extended_get(
            kwargs.get('title_romaji'), DEFAULT_TITLE_ROMAJI)
        self._studio: str = extended_get(kwargs.get('studio'), DEFAULT_STUDIO)
        self._studio_url: str = extended_get(
            kwargs.get('studio_url'), DEFAULT_STUDIO_URL)
        self._start_date: datetime = extended_get(
            kwargs.get('start_date'), DEFAULT_START_DATE)
        self._end_date: datetime = extended_get(
            kwargs.get('end_date'), DEFAULT_END_DATE)

    @property
    def id(self) -> int:
        return self._id_ani

    @property
    def id_ani(self) -> int:
        return self._id_ani

    @property
    def id_anilist(self) -> int:
        return self._id_ani

    @property
    def id_mal(self) -> int:
        return self._id_mal

    @property
    def id_myanimelist(self) -> int:
        return self._id_mal

    @property
    def id_kitsu(self) -> int:
        return self._id_kitsu

    @property
    def episodes(self) -> int:
        return self._episodes

    @property
    def duration(self) -> int:
        return self._duration

    @property
    def popularity(self) -> int:
        return self._popularity

    @property
    def average_score(self) -> int:
        return self._average_score

    @property
    def banner_image(self) -> str:
        return self._banner_image

    @property
    def cover_image(self) -> str:
        return self._cover_image

    @property
    def title(self) -> str:
        return self._title_user_preferred

    @property
    def title_user_preferred(self) -> str:
        return self._title_user_preferred

    @property
    def title_native(self) -> str:
        return self._title_native

    @property
    def title_english(self) -> str:
        return self._title_english

    @property
    def title_romaji(self) -> str:
        return self._title_romaji

    @property
    def studio(self) -> str:
        return self._studio

    @property
    def studio_url(self) -> str:
        return self._studio_url

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date


def _check_equality(name1, name2) -> bool:
    Ayumi.debug("Regex comparing: {} | {}".format(name1, name2))
    try:
        # Anilist sometimes has weird leading/trailing spaces
        re_str1 = re.sub(r'[^\w]', '', name1)
        Ayumi.debug("Name 1 without puncutation: {}".format(re_str1))
        re_str2 = re.sub(r'[^\w]', '', name2)
        Ayumi.debug("Name 2 without puncutation: {}".format(re_str2))

        if re_str1 == re_str2:
            Ayumi.debug("Both show names are matching, returning True.")
            return True
        else:
            Ayumi.debug("Show names do not match, returning False.")
            return False
    except:
        Ayumi.debug("Error occured while matching show names, returning False.")
        return False


def _clean_title(title):
    """
    Removes potentially problematic characters.
    """
    try:
        clean_str = title.replace('"', '')
        Ayumi.debug("Cleaned {} to {}.".format(title, clean_str))
        return clean_str
    except:
        Ayumi.debug(
            "Cleaner wasn't provided a valid title ({}), returning None.".format(title))
        return None


def _query_request(query, search, status) -> dict:
    """
    Makes requests to Anlist, returns response in JSON.

    Query: One of the Queries objects.
    Search: Name of show to search for.
    Status: Status of the show to search for.
    """
    try:
        Ayumi.debug("Making request to {}, searching for {} under status {}".format(
            ANILIST_API_URL, search, status
        ))
        ani_res = requests.post(
            ANILIST_API_URL,
            json={
                'query': query,
                'variables': {
                    'search': search,
                    'status': status
                }
            },
            timeout=10
        )

        if ani_res.status_code != 200:
            Ayumi.warning("Anilist returned unaccepted HTTP code {} upon request.".format(
                ani_res.status_code), color=Ayumi.LRED)
            raise Exception()

        # Get request response as JSON object.
        try:
            ani_json = ani_res.json()
            return ani_json['data']
        except:
            Ayumi.warning("Anilist returned a non-JSON response.",
                          color=Ayumi.LRED)
            raise Exception()

    except requests.exceptions.Timeout:
        Ayumi.warning("Request to Anilist timed out.", color=Ayumi.LRED)
        raise Exception()
    except requests.exceptions.ConnectionError:
        Ayumi.warning(
            "Unable to contact Anilist, maybe it's down?", color=Ayumi.LRED)
        raise Exception()


def _single_search(search, status):
    """
    Searches for a show using the single query.
    Params:
        search - show to search for
        status - status to filter under.

    Returns: Show data if it's found, or None.
    """
    try:
        info = _query_request(SINGLE_QUERY, search, status)
    except:
        Ayumi.debug(
            "No data provided for {} in {}, returning None.".format(search, status))
        return None

    # Check if any of the titles match
    Ayumi.debug("Checking for matches in media titles...")
    for title in info['Media']['title'].values():
        if _check_equality(search, title):
            Ayumi.debug("Matched {} to {}, returning.".format(search, title))
            return info['Media']
        else:
            Ayumi.debug("Did not match {} to {}.".format(search, title))

    # Check if any of the synonyms match
    Ayumi.debug("Checking for matches in media synonyms...")
    for title in info['Media']['synonyms']:
        if _check_equality(search, title):
            Ayumi.debug("Matched {} to {}, returning.".format(search, title))
            return info['Media']
        else:
            Ayumi.debug("Did not match {} to {}.".format(search, title))

    # No matches, return None
    Ayumi.debug(
        "Didn't find any matches for {} in {}, returning None.".format(search, status))
    return None


def _page_search(search, status):
    """
    Searches for a show using the page query.
    Params:
        search - show to search for
        status - status to filter under.

    Returns: Show data if it's found, or None.
    """
    try:
        info = _query_request(PAGE_QUERY, search, status)['Page']['media']
    except:
        Ayumi.debug(
            "No data provided for {} in {}, returning None.".format(search, status))
        return None

    for show in info:
        # Check if any of the titles match
        Ayumi.debug("Checking for matches in media titles...")
        for title in show['title'].values():
            if _check_equality(search, title):
                Ayumi.debug(
                    "Matched {} to {}, returning.".format(search, title))
                return show
            else:
                Ayumi.debug("Did not match {} to {}.".format(search, title))

        # Check if any of the synonyms match
        Ayumi.debug("Checking for matches in media synonyms...")
        for title in show['synonyms']:
            if _check_equality(search, title):
                Ayumi.debug(
                    "Matched {} to {}, returning.".format(search, title))
                return show
            else:
                Ayumi.debug("Did not match {} to {}.".format(search, title))

    # No matches, return None
    Ayumi.debug(
        "Didn't find any matches for {} in {}, returning None.".format(search, status))
    return None


@deprecated(version='0.1', reason="Should move to another module.")
def _kitsu_basic_search(title):
    """Quick Kitsu implementation"""
    title_lower = title.lower()
    request_url = requests.utils.requote_uri(KITSU_API_URL + title_lower)
    Ayumi.debug("Created Kitsu request URL: {}".format(request_url))

    try:
        kitsu_res = requests.get(request_url, timeout=10)

        try:
            kitsu_json = kitsu_res.json()
            return kitsu_json
        except:
            Ayumi.warning(
                "Kitsu did not return a valid JSON response.", color=Ayumi.RED)
            raise Exception()
    except requests.exceptions.Timeout:
        Ayumi.warning("Kitsu request timed out.", color=Ayumi.LRED)
        raise Exception()
    except requests.exceptions.ConnectionError:
        Ayumi.warning(
            "Unable to contact Kitsu, maybe it's down?", color=Ayumi.LRED)
        raise Exception()


@deprecated(version='0.1', reason="Should move to another module.")
def _get_kitsu_id(title):
    """Gets Kitsu's ID for a show." Returns -1 if not found."""
    try:
        kitsu_id = _kitsu_basic_search(title)['data'][0]['id']
        return int(kitsu_id)
    except:
        Ayumi.debug("Error occured when fetching Kitsu ID, returning -1.")
        return -1


def _get_main_studio_info(studios):
    """
    Goes through the studio edges and returns the main (studio name, siteurl)

    Params:
        studios - The studios body from the Anilist GraphQL json response

    Returns: A tuple (studio name: str, site url: str), or None if not found
    """
    try:
        edges = studios['edges']
        for edge in edges:
            Ayumi.debug("Checking edge {}".format(edge['node']['name']))
            if edge['isMain']:
                Ayumi.debug("Found main studio edge, returning tuple")
                node = edge['node']
                return (node['name'], node['siteUrl'])
        # If a main studio isn't found, return None
        Ayumi.debug("Didn't find any main studio edge, returning None")
        return (None, None)
    except Exception as e:
        Ayumi.warning(
            "Didn't find any main studio edge due to error, returning None")
        Ayumi.warning(e)
        return (None, None)


def _create_hisha_object(show, title):
    if show is None:
        return Hisha(
            title_user_preferred=_clean_title(title),
            title_native=_clean_title(title),
            title_english=_clean_title(title),
            title_romaji=_clean_title(title)
        )
    else:
        studio, studio_url = _get_main_studio_info(show['studios'])

        start_date = show['startDate']
        if start_date['year'] and start_date['month'] and start_date['day']:
            start_date_dt = datetime(
                year=start_date['year'], month=start_date['month'], day=start_date['day'])
        else:
            start_date_dt = None

        end_date = show['endDate']
        if end_date['year'] and end_date['month'] and end_date['day']:
            end_date_dt = datetime(
                year=end_date['year'], month=end_date['month'], day=end_date['day'])
        else:
            end_date_dt = None

        return Hisha(
            id_ani=show['id'],
            id_mal=show['idMal'],
            id_kitsu=_get_kitsu_id(title),
            episodes=show['episodes'],
            duration=show['duration'],
            popularity=show['popularity'],
            average_score=show['averageScore'],
            banner_image=show['bannerImage'],
            cover_image=show['coverImage']['large'],
            title_user_preferred=_clean_title(show['title']['userPreferred']),
            title_native=_clean_title(show['title']['native']),
            title_english=_clean_title(show['title']['english']),
            title_romaji=_clean_title(show['title']['romaji']),
            studio=studio,
            studio_url=studio_url,
            start_date=start_date_dt,
            end_date=end_date_dt,
        )


def search(show):
    airing = _single_search(show, "RELEASING")
    if airing:
        Ayumi.info("Found show {} in RELEASING, returning Hisha object.".format(
            show), color=Ayumi.LCYAN)
        return _create_hisha_object(airing, show)

    finished = _page_search(show, "FINISHED")
    if finished:
        Ayumi.info("Found show {} in FINISHED, returning Hisha object.".format(
            show), color=Ayumi.LCYAN)
        return _create_hisha_object(finished, show)

    not_yet_released = _single_search(show, "NOT_YET_RELEASED")
    if not_yet_released:
        Ayumi.info("Found show {} in NOT_YET_RELEASED, returning Hisha object.".format(
            show), color=Ayumi.LCYAN)
        return _create_hisha_object(not_yet_released, show)

    # None of them found a show, so create a dummy Hisha object.
    Ayumi.info("Creating dummy Hisha object for {} with default values.".format(
        show), color=Ayumi.LCYAN)
    return _create_hisha_object(None, show)
