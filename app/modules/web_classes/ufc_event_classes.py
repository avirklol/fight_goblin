"""
UFC Event Classes
--------------------------------
Classes for the UFC event parent and children pages.

ENDPOINTS:
- https://www.ufc.com/events
- https://www.ufc.com/event/ufc-<event_number>
- https://www.ufc.com/event/ufc-fight-night-<month-DD-YYYY>
"""

# UFC EVENT

EVENT_CLASS = {
    'container': 'l-listing__item',
    'url': {
        'container': 'c-card-event--result__logo',
        'tag': 'a'  # Get href
    }
}

FIGHT_CARD = 'fight-card'  # Get class

# CARD

CATEGORY_ID = {
    'main': 'main-card',  # Get id
    'prelims': 'prelims-card',  # Get id
    'early_prelims': 'early-prelims'  # Get id
}

CATEGORY_CLASS = {
    'main': 'main-card',  # Get class
    'prelims': 'fight-card-prelims',  # Get class
    'early_prelims': 'fight-card-prelims-early'  # Get class
}

BROADCAST_TIME = 'c-event-fight-card-broadcaster__time'  # Get text

# FIGHT

FIGHT = 'l-listing__item'

FIGHT_PROPERTIES = {
    'container': 'c-listing-fight__content-row',
    'details': {
        'container': 'c-listing-fight__details',
        'is_live': 'c-listing-fight__banner--live',  # Get text
        'class': {
            'container': 'c-listing-fight__class',
            'item': 'c-listing-fight__class-text',  # Get text
        },
        'ranks': {
            'container': 'c-listing-fight__class',
            'item': 'c-listing-fight__corner-rank',  # Get ranks twice
        },
        'award': 'c-listing-fight__awards',  # Get text
        'fighters': {
            'container': 'c-listing-fight__names-row',
            'red': {
                'container': 'c-listing-fight__corner-name--red',
                'gn': 'c-listing-fight__corner-given-name',  # Get text
                'fn': 'c-listing-fight__corner-family-name'  # Get text
            },
            'blue': {
                'container': 'c-listing-fight__corner-name--blue',
                'gn': 'c-listing-fight__corner-given-name',  # Get text
                'fn': 'c-listing-fight__corner-family-name'  # Get text
            }
        },
        'results': {
            'container': 'js-listing-fight__results',
            'data': {
                'container': 'c-listing-fight__result',
                'round': 'c-listing-fight__result-text round',  # Get text
                'time': 'c-listing-fight__result-text time',  # Get text
                'method': 'c-listing-fight__result-text method'  # Get text
            }
        },
    },
    'fighter_data': {
        'red': {
            'container': 'c-listing-fight__corner--red',
            'urls': {
                'container': 'c-listing-fight__corner-image--red',
                'page': {
                    'tag': 'a',  # Target <a> tag
                },
                'image': {
                    'container': 'layout__region',  # Target layout__region class nested in <a> tag
                    'tag': 'img'  # Get src attribute from <img> tag
                }
            },
            'outcome': {
                'container': 'c-listing-fight__corner-body--red',
                'item': 'c-listing-fight__outcome-wrapper'  # Get text, if any
            }
        },
        'blue': {
            'container': 'c-listing-fight__corner--blue',
            'urls': {
                'container': 'c-listing-fight__corner-image--blue',
                'page': {
                    'tag': 'a',  # Target <a> tag
                },
                'image': {
                    'container': 'layout__region',  # Target layout__region class nested in <a> tag
                    'tag': 'img'  # Get src attribute from <img> tag
                }
            },
            'outcome': {
                'container': 'c-listing-fight__corner-body--blue',
                'item': 'c-listing-fight__outcome-wrapper'  # Get tex, if any
            }
        }
    }
}

ODDS_PROPERTIES = {
    'container': 'c-listing-fight__odds-row',
    'fighter_country': {
        'red': 'c-listing-fight__country--red',
        'blue': 'c-listing-fight__country--blue',
        'item': 'c-listing-fight__country-text'  # Get text
    },
    'odds': 'c-listing-fight__odds-wrapper'  # Get text
}
