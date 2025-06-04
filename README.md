# Fight Goblin
## About
Fight Goblin is a UFC fight companion app that allows friends to get ongoing UFC fight cards and make predictions on the outcome of the matches.

## MVP
- User creation
- Fighter database
- Leaderboard
- Users can make fight predictions (TKO, Submission, Decision)
- Users can see fighter stats

## Requirements
- A good Kaggle dataset for UFC fighter stats
- An API/scrape containing fight card data
- Local DB management that leverages a home network (running on my Mac?)
- Simple UX that allows users to see various cards and make predictions on a fight (TKO, Decision, Submission)
- Leaderboard
- Only want to leverage Python with some HTML and CSS
- Streamlit for the MVP
- Flask for the Final Product, levaraging Rich and Textual

## How It Works
It's a pretty simple app web app with very few bells and whistles.

### Splash/Login Page.
Shows a splash image and then proceeds with login if previously logged in, bringing user to Main page.
If no log in is detected, allows users to create an account or login; all logins are associated with their device id; I would prefer if they didn't have to provide any signup information beyond what they'd like their username to be.

### Main Page
Once a user is logged in they can see a list of upcoming UFC events.

### Event Page
Upon selecting a UFC event they are presented with collapsible sections for each fight card; the fight cards will be Main, Prelims and Early-Prelims.
Each card will show the name of the fighters, their fight recrods
