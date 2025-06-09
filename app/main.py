import asyncio
from pathlib import Path
import streamlit as st
from modules.scraper import parse_event_page, get_next_event, update_database
from modules.database import Database

# Paths
BASE_DIR = Path(__file__).parent

db = Database()


@st.cache_data(ttl=60 * 60)
def get_event_data():
    """
    Get the data for the next UFC event.

    Returns:
        tuple: The URL of the next UFC event and the data for the event
    """
    event_url = get_next_event()
    event_data = parse_event_page(event_url=event_url)
    return event_url, event_data


RECENT_EVENT_URL, UFC_EVENT_DATA = get_event_data()


async def update_database(event: dict):
    db_event = {
        'url': event['url'],  # Note: changed from event_url to url
        'fights': list()
    }
    await db.insert_event(db_event)


async def check_and_update_db():
    event = await db.get_event(RECENT_EVENT_URL)
    if not event:
        await update_database(UFC_EVENT_DATA)

# Run the async function
asyncio.run(check_and_update_db())

CARDS = {
    'MAIN': {
        'data': UFC_EVENT_DATA.get('main').get('data'),
        'time': UFC_EVENT_DATA.get('main').get('time')
    },
    'PRELIMS': {
        'data': UFC_EVENT_DATA.get('prelims').get('data'),
        'time': UFC_EVENT_DATA.get('prelims').get('time')
    },
    'EARLY PRELIMS': {
        'data': UFC_EVENT_DATA.get('early_prelims').get('data'),
        'time': UFC_EVENT_DATA.get('early_prelims').get('time')
    }
}


def main():
    select_box_values = [card for card, data in CARDS.items() if data.get('data') is not None]
    select_box = st.selectbox("SELECT A CARD", select_box_values)
    st.write(CARDS[select_box]['time'])
    key_range = len(CARDS[select_box]['data'])

    # Fight Card
    for key in range(key_range):
        if CARDS[select_box]['data'][key]['is_live']:
            st.error('LIVE NOW', icon='🔴')
        row1 = st.columns(2, border=True)
        row2 = st.columns(3)
        col1, col2 = row1

        red_name = CARDS[select_box]['data'][key]['red_fighter']['name']
        red_rank = CARDS[select_box]['data'][key]['red_fighter']['rank']
        red_nickname = CARDS[select_box]['data'][key]['red_fighter']['nickname']
        blue_name = CARDS[select_box]['data'][key]['blue_fighter']['name']
        blue_rank = CARDS[select_box]['data'][key]['blue_fighter']['rank']
        blue_nickname = CARDS[select_box]['data'][key]['blue_fighter']['nickname']
        category = CARDS[select_box]['data'][key]['class']
        rc = CARDS[select_box]['data'][key]['red_fighter']['country']
        bc = CARDS[select_box]['data'][key]['blue_fighter']['country']
        ro = CARDS[select_box]['data'][key]['red_fighter']['odds']
        bo = CARDS[select_box]['data'][key]['blue_fighter']['odds']
        rw = CARDS[select_box]['data'][key]['red_fighter']['w']
        rl = CARDS[select_box]['data'][key]['red_fighter']['l']
        rn = CARDS[select_box]['data'][key]['red_fighter']['nc']
        bw = CARDS[select_box]['data'][key]['blue_fighter']['w']
        bl = CARDS[select_box]['data'][key]['blue_fighter']['l']
        bn = CARDS[select_box]['data'][key]['blue_fighter']['nc']
        rf = CARDS[select_box]['data'][key]['red_fighter']['flag']
        bf = CARDS[select_box]['data'][key]['blue_fighter']['flag']

        # Red Fighter
        with col1:
            st.write(f'{red_name} [{red_rank}]')
            st.write(f'{red_nickname} ({rw}-{rl}-{rn})')
            st.write(f':small[{rc}]')
            st.write(f'Odds: {ro if ro is not None else "-"}')
            col_row = st.columns(1)
            st.session_state[f'{key}_{select_box}_red_outcome'] = col_row[0].radio('Outcome', options=['TKO', 'SUB', 'DEC'], key=f'{key}_{select_box}_red')

        # Blue Fighter
        with col2:
            st.write(f'{blue_name} [{blue_rank}]')
            st.write(f'{blue_nickname} ({bw}-{bl}-{bn})')
            st.write(f':small[{bc}]')
            st.write(f'Odds: {bo if bo is not None else "-"}')
            col_row = st.columns(3)
            st.session_state[f'{key}_{select_box}_blue_outcome'] = col_row[0].radio('Outcome', options=['TKO', 'SUB', 'DEC'], key=f'{key}_{select_box}_blue')

        # Fight Results
        row2[0].write(f'Round: {CARDS[select_box]["data"][key]["results"]["round"] if CARDS[select_box]["data"][key]["results"]["round"] is not None else "Undetermined"}')
        row2[1].write(f'Time: {CARDS[select_box]["data"][key]["results"]["time"] if CARDS[select_box]["data"][key]["results"]["time"] is not None else "Undetermined"}')
        row2[2].write(f'Method: {CARDS[select_box]["data"][key]["results"]["method"] if CARDS[select_box]["data"][key]["results"]["method"] is not None else "Undetermined"}')
        st.divider()


if __name__ == "__main__":
    main()
