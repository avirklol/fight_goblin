import requests
import click
import random
import pprint
from bs4 import BeautifulSoup
from app.modules.web_classes.ufc_event_classes import CATEGORY_ID, BROADCAST_TIME, EVENT_CLASS, FIGHT, FIGHT_PROPERTIES, ODDS_PROPERTIES
from app.modules.database import db


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}


def get_next_event() -> str:
    """
    Get the next UFC event from the UFC website.

    """
    ufc_event_page = 'https://www.ufc.com/events'
    response = requests.get(ufc_event_page, timeout=10, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    url = soup.find_all(class_=EVENT_CLASS['container'])[0].find(class_=EVENT_CLASS['url']['container']).find(EVENT_CLASS['url']['tag']).get('href')
    next_event = f'https://www.ufc.com{url}'
    click.echo(click.style(f"Next event URL: {next_event}", fg='green'))
    return next_event


def get_fighter_info(fighter_url: str) -> dict:
    """
    Get the information for a UFC fighter from the UFC website.
    """
    response = requests.get(fighter_url, timeout=10, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    hero_container = soup.find(class_='hero-profile')
    win_loss = hero_container.find(class_='hero-profile__division-body').get_text(strip=True).strip(' (W-L-D)').split('-')
    data = {
        'nickname': hero_container.find(class_='hero-profile__nickname').get_text(strip=True).strip('"') if hero_container.find(class_='hero-profile__nickname') else None,
        'w': win_loss[0],
        'l': win_loss[1],
        'nc': win_loss[2]
    }
    return data


# @click.command()
# @click.option('--event_number', default=random.randint(290, 310), type=int, help='The number of the UFC event to parse https://www.ufc.com/event/ufc-<event_number> ()')
# @click.option('--event_url', default=None, type=str, help='The URL of the UFC event to parse (optional)')
def parse_event_page(event_number: int = None, event_url: str = None, dev_mode: bool = False) -> dict:
    """
    Get the data for a UFC event from the UFC website.

    Args:
        event_number (int): The number of the UFC event to parse https://www.ufc.com/event/ufc-<event_number> (option 1)
        event_url (str): The URL of the UFC event to parse (option 2)

    Returns:
        dict: The data for the parsed UFC event
    """
    if not event_number and not event_url:
        event_number = random.randint(290, 310)
        click.echo(click.style("Please provide either an event number or a URL", fg='red'))
        click.echo(click.style(f"Returning a random event number ({event_number})", fg='green'))

    ufc_event_url = event_url if event_url else f'https://www.ufc.com/event/ufc-{event_number}'

    response = requests.get(ufc_event_url, timeout=10, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    event = {
        'main': dict(),
        'prelims': dict(),
        'early_prelims': dict(),
    }

    for card, data in event.items():
        try:
            card_html = soup.find(id=CATEGORY_ID[card])
            if dev_mode:
                data['html'] = card_html
            data['time'] = card_html.find(class_=BROADCAST_TIME).get_text(strip=True)
            click.echo(click.style(f"Card: {event[card]}", fg='green'))
        except Exception as e:
            print(f'Error parsing {card} card: {e}')

        if card_html:
            fights = card_html.find_all(class_=FIGHT)
            fight_list = []
            for fight in fights:
                fight_data = {'red_fighter': dict(),
                              'blue_fighter': dict(),
                              'results': {'round': 'None', 'time': 'None', 'method': 'None'}
                            }

                # Data Containers
                odds_data = fight.find(class_=ODDS_PROPERTIES['container'])
                fight_details = fight.find(class_=FIGHT_PROPERTIES['container'])
                ranks = fight_details.find(class_=FIGHT_PROPERTIES['details']['ranks']['container'])
                results = fight_details.find(class_=FIGHT_PROPERTIES['details']['results']['container'])

                # Scrape Fight Details
                if fight_details:
                    is_live = fight_details.find(class_=FIGHT_PROPERTIES['details']['is_live'])
                    if is_live:
                        is_live_classes = is_live.get('class', [])
                        fight_data['is_live'] = 'hidden' not in is_live_classes

                    fight_data['class'] = fight_details.find(class_=FIGHT_PROPERTIES['details']['class']['item']).get_text(strip=True)

                    fight_data['award'] = fight_details.find(class_=FIGHT_PROPERTIES['details']['award']).get_text(strip=True)
                    if len(fight_data['award']) == 0:
                        fight_data['award'] = None

                    for source_item in FIGHT_PROPERTIES['fighter_data'].keys():
                        for target_item, target_data in fight_data.items():
                            if source_item in target_item:
                                fighter_name = fight_details.find(class_=FIGHT_PROPERTIES['details']['fighters'][source_item]['container'])
                                if fighter_name:
                                    full_name = fighter_name.find(class_=FIGHT_PROPERTIES['details']['fighters'][source_item]['gn'])
                                    if full_name:
                                        given_name = fighter_name.find(class_=FIGHT_PROPERTIES['details']['fighters'][source_item]['gn']).get_text(strip=True)
                                        family_name = fighter_name.find(class_=FIGHT_PROPERTIES['details']['fighters'][source_item]['fn']).get_text(strip=True)
                                        fight_data[target_item]['name'] = f'{given_name} {family_name}'
                                    else:
                                        fight_data[target_item]['name'] = fighter_name.get_text(strip=True)
                                fight_data[target_item]['country'] = odds_data.find(class_=ODDS_PROPERTIES['fighter_country'][source_item]).find(class_=ODDS_PROPERTIES['fighter_country']['item']).get_text(strip=True) if odds_data.find(class_=ODDS_PROPERTIES['fighter_country'][source_item]).find(class_=ODDS_PROPERTIES['fighter_country']['item']) else 'Unlisted'
                                fight_data[target_item]['flag'] = odds_data.find(class_=ODDS_PROPERTIES['fighter_country'][source_item]).find('img').get('src') if odds_data.find(class_=ODDS_PROPERTIES['fighter_country'][source_item]).find('img') else None
                                fighter_data = fight_details.find(class_=FIGHT_PROPERTIES['fighter_data'][source_item]['container'])
                                if fighter_data:
                                    profile_url = fighter_data.find(FIGHT_PROPERTIES['fighter_data'][source_item]['urls']['page']['tag']).get('href')
                                    if profile_url:
                                        fighter_info = get_fighter_info(profile_url)
                                        fight_data[target_item]['nickname'] = fighter_info['nickname']
                                        fight_data[target_item]['w'] = fighter_info['w']
                                        fight_data[target_item]['l'] = fighter_info['l']
                                        fight_data[target_item]['nc'] = fighter_info['nc']
                                        fight_data[target_item]['profile_url'] = profile_url
                                    fight_data[target_item]['image_url'] = fighter_data.find(FIGHT_PROPERTIES['fighter_data'][source_item]['urls']['image']['tag']).get('src')
                                    fight_data[target_item]['outcome'] = (fighter_data.find(class_=FIGHT_PROPERTIES['fighter_data'][source_item]['outcome']['item']).get_text(strip=True)
                                                            if fighter_data.find(class_=FIGHT_PROPERTIES['fighter_data'][source_item]['outcome']['item']).get_text(strip=True) != ''
                                                            else None)

                if ranks:
                    sorted_ranks = [rank for rank in ranks.find_all(class_=FIGHT_PROPERTIES['details']['ranks']['item'])]
                    fight_data['red_fighter']['rank'] = sorted_ranks[0].get_text(strip=True) if sorted_ranks[0].get_text(strip=True) != '' else 'Unranked'
                    fight_data['blue_fighter']['rank'] = sorted_ranks[1].get_text(strip=True) if sorted_ranks[1].get_text(strip=True) != '' else 'Unranked'

                if odds_data:
                    odds = odds_data.find(class_=ODDS_PROPERTIES['odds']).get_text(strip=True)
                    fight_data['red_fighter']['odds'] = odds.split('odds')[0] if odds.split('odds')[0] != '-' else None
                    fight_data['blue_fighter']['odds'] = odds.split('odds')[1] if odds.split('odds')[1] != '-' else None

                if results:
                    for item, data in fight_data['results'].items():
                        data = results.find(class_=FIGHT_PROPERTIES['details']['results']['data'][item]).get_text(strip=True)
                        if data != '':
                            fight_data['results'][item] = data
                        else:
                            fight_data['results'][item] = None

                fight_data['user_predictions'] = list()

                fight_list.append(fight_data)

            if len(fight_list) > 0:
                event[card]['data'] = fight_list

    event['url'] = ufc_event_url

    # Print the parsed data for verification and remove empty card data.
    for card, data in event.items():
        if 'url' not in card:
            if data.get('data') is not None:
                click.echo(click.style(f"Card: {card}", fg='green'))
                click.echo(click.style(f"Time: {data.get('time')}", fg='green'))
            for fight in data.get('data', []):
                pprint.pprint(fight)
                print('=' * 100)
        else:
            click.echo(click.style(f"Event URL: {event[card]}", fg='green'))
    return event


async def update_database(event: dict):
    db_event = {
        'url': event['event_url'],
        'fights': list()
    }

    await db.insert_event(db_event)

    for card, data in event.items():
        if 'url' not in card:
            for fight in data.get('data', []):
                await db.insert_fight(fight)

if __name__ == '__main__':
    get_next_event()
    parse_event_page()
