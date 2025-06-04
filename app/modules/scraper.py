import requests
import click
import random
import pprint
import pandas as pd
from bs4 import BeautifulSoup
from ufc_website_classes import (
    PAGE_ID, PAGE_CLASS, FIGHT_CARD, CATEGORY_ID, CATEGORY_CLASS,
    BROADCAST_TIME, FIGHT, FIGHT_PROPERTIES, ODDS_PROPERTIES
)


@click.command()
@click.option('--event_number', default=random.randint(290, 310), type=int, help='The number of the UFC event to parse https://www.ufc.com/event/ufc-<event_number>')
def parse_event_page(event_number: int) -> dict:
    """
    Get the data for a UFC event from the UFC website.
    """
    ufc_event_url = f'https://www.ufc.com/event/ufc-{event_number}'
    print(f'Getting data from UFC {event_number}!')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(ufc_event_url, timeout=10, headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')

    fight_categories = {
        'main': dict(),
        'prelims': dict(),
        'early_prelims': dict()
    }

    for category in fight_categories.keys():
        try:
            fight_categories[category]['html'] = soup.find(id=CATEGORY_ID[category])
        except Exception as e:
            print(f'Error parsing {category} category: {e}')

    for category, data in fight_categories.items():
        if data.get('html'):
            fights = data['html'].find_all(class_=FIGHT)
            fight_list = []
            for fight in fights:
                fight_data = {'red_fighter': dict(), 'blue_fighter': dict()}

                # Data Containers
                odds_data = fight.find(class_=ODDS_PROPERTIES['container'])
                fight_details = fight.find(class_=FIGHT_PROPERTIES['container'])
                ranks = fight_details.find(class_=FIGHT_PROPERTIES['details']['ranks']['container'])
                results = fight_details.find(class_=FIGHT_PROPERTIES['details']['results']['container'])

                #
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
                                fight_data[target_item]['country'] = odds_data.find(class_=ODDS_PROPERTIES['fighter_country'][source_item]).find(class_=ODDS_PROPERTIES['fighter_country']['item']).get_text(strip=True)
                                fighter_data = fight_details.find(class_=FIGHT_PROPERTIES['fighter_data'][source_item]['container'])
                                if fighter_data:
                                    fight_data[target_item]['profile_url'] = fighter_data.find(FIGHT_PROPERTIES['fighter_data'][source_item]['urls']['page']['tag']).get('href')
                                    fight_data[target_item]['image_url'] = fighter_data.find(FIGHT_PROPERTIES['fighter_data'][source_item]['urls']['image']['tag']).get('src')
                                    fight_data[target_item]['outcome'] = (fighter_data.find(class_=FIGHT_PROPERTIES['fighter_data'][source_item]['outcome']['item']).get_text(strip=True)
                                                            if fighter_data.find(class_=FIGHT_PROPERTIES['fighter_data'][source_item]['outcome']['item']).get_text(strip=True) != ''
                                                            else 'None')

                if ranks:
                    sorted_ranks = [rank for rank in ranks.find_all(class_=FIGHT_PROPERTIES['details']['ranks']['item'])]
                    fight_data['red_fighter']['rank'] = sorted_ranks[0].get_text(strip=True) if sorted_ranks[0].get_text(strip=True) != '' else 'Unranked'
                    fight_data['blue_fighter']['rank'] = sorted_ranks[1].get_text(strip=True) if sorted_ranks[1].get_text(strip=True) != '' else 'Unranked'

                if odds_data:
                    odds = odds_data.find(class_=ODDS_PROPERTIES['odds']).get_text(strip=True)
                    fight_data['red_fighter']['odds'] = odds.split('odds')[0] if odds.split('odds')[0] != '-' else 'None'
                    fight_data['blue_fighter']['odds'] = odds.split('odds')[1] if odds.split('odds')[1] != '-' else 'None'

                if results:
                    fight_data['results'] = {
                        'round': (results.find(class_=FIGHT_PROPERTIES['details']['results']['data']['round']).get_text(strip=True)
                                    if results.find(class_=FIGHT_PROPERTIES['details']['results']['data']['round']).get_text(strip=True) != ''
                                    else 'None'),
                        'time': (results.find(class_=FIGHT_PROPERTIES['details']['results']['data']['time']).get_text(strip=True)
                                    if results.find(class_=FIGHT_PROPERTIES['details']['results']['data']['time']).get_text(strip=True) != ''
                                    else 'None'),
                        'method': (results.find(class_=FIGHT_PROPERTIES['details']['results']['data']['method']).get_text(strip=True)
                                    if results.find(class_=FIGHT_PROPERTIES['details']['results']['data']['method']).get_text(strip=True) != ''
                                    else 'None')
                    }

                fight_list.append(fight_data)

            fight_categories[category]['data'] = fight_list

    # Print the parsed data for verification
    for category, data in fight_categories.items():
        print(f"Category: {category}")
        for fight in data.get('data', []):
            pprint.pprint(fight)
    return fight_categories

if __name__ == '__main__':
    parse_event_page()
