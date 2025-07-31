import streamlit as st
import pandas as pd
import plotly.express as px
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.set_page_config(layout="wide")

# importing datasets
df = pd.read_csv('dataset/athlete_events.csv')
region_df = pd.read_csv('dataset/noc_regions.csv')
# preprocessing the datasets
df = preprocessor.preprocessor(df,region_df)
# initializing sidebar
st.sidebar.title('Olympics Analysis')
# radio button
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    # Extracting country and year data
    years, country = helper.country_years_list(df)
    # dropdown for selecting year
    select_year = st.sidebar.selectbox('Select Year', years)
    # dropdown for selecting country
    select_country = st.sidebar.selectbox('Select Country', country)

    # extracting medal tally data as per user filter
    medal_tally = helper.medal_tally(df, select_year, select_country )
    if select_year == 'Overall' and select_country == 'Overall':
        st.header('Medal Tally')
    elif select_year == 'Overall':
        st.header(select_country + ' Medal Tally')
    elif select_country == 'Overall':
        st.header(str(select_year) + ' Medal Tally')
    else:
        st.header(str(select_year) + ' ' + select_country + ' Medal Tally')
    # displaying medal tally
    st.dataframe(medal_tally)

elif user_menu == 'Overall Analysis':
    # extracting top statistics
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    # displaying top statistics
    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    # extracting data of participating nations over time and representing by line plot
    nationsOverTime = helper.partNationsOverTime(df)
    fig = px.line(nationsOverTime, x='Edition', y='No of Countries')
    st.title('Participating Nations Over the Years')
    st.plotly_chart(fig)

    # extracting data of events over time and representing by line plot
    eventsOverTime = helper.dataOverTime(df)
    fig = px.line(eventsOverTime, x='Edition', y='Events')
    st.title('Events Over the Years')
    st.plotly_chart(fig)

    # extracting data of participating athletes over time and representing by line plot
    athletesOverTime = helper.athletesOverTime(df)
    fig = px.line(athletesOverTime, x='Edition', y='Athletes')
    st.title('Athletes Over the Years')
    st.plotly_chart(fig)

    # decorated athletes
    sportsList = helper.sportsListFind(df)
    st.title('Decorated Athletes')
    optionSport = st.selectbox('Select Sport',sportsList)
    # extracting top athletes
    decoratedAthletes = helper.decoratedAthletes(df,optionSport)
    # displaying in dataframe
    st.dataframe(decoratedAthletes, hide_index=True)


elif user_menu == 'Country-wise Analysis':
    # Title
    st.title('Country-wise Analysis')
    # Extracting country list and removing overall
    years, country = country_years_list(df)
    country.remove('Overall')
    # Country dropdown menu
    optionCountry = st.sidebar.selectbox('Select Country', country)

    # Country top stats
    sportsPart, eventsPart, athletesPart, medalCnt = helper.countryTopStats(df, optionCountry)
    st.title('Top Statistics')
    col1, col2, col3= st.columns(3)
    with col1:
        st.header('Sports Played')
        st.title(sportsPart)
    with col2:
            st.header('Events Played')
            st.title(eventsPart)
    with col3:
            st.header('Athlete Played')
            st.title(athletesPart)

    # medal tally of selected country represented by line plot
    medalTally = helper.countryMedalTally(df, optionCountry)
    medalTallyFig = px.line(medalTally, x='Year', y='Total', title=f"Total Medals won: {medalCnt}")

    st.title(optionCountry + ' Medal Tally over the Years')
    st.plotly_chart(medalTallyFig)

    # heatmap comparing medals and sport
    heatMapData = helper.countryHeatMap(df, optionCountry)
    st.title(f'{optionCountry} Heatmap Over the Years ')
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(heatMapData, annot=True)
    st.pyplot(fig)

    # most successful athletes
    bestAthletesList = helper.bestAthletes(df,optionCountry)
    st.title(f'Top 10 athletes from {optionCountry}')
    st.dataframe(bestAthletesList, hide_index=True)

elif user_menu == 'Athlete-wise Analysis':
    # Title
    st.title('Athlete-wise Analysis')
    x1,x2,x3,x4 = helper.distPlotData(df)
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist','Silver Medalist' , 'Bronze Medalist'], show_hist=False, show_rug=False)
    st.header('Distribution of Age')
    st.plotly_chart(fig)


    st.header('Scatter plot of height & wright vs Gold Medalist')
    sportslst = helper.sportsListFind(df)
    optionSport = st.selectbox('Select Sport',sportslst)
    scatterPlotData = helper.scatterPlotGoldMedalist(df, optionSport)
    fig, ax = plt.subplots()

    sns.scatterplot(data=scatterPlotData, x='Weight', y='Height', hue='Medal', alpha=0.8, ax=ax)
    st.pyplot(fig)

    st.header('Male vs Female participants over the years')
    final = helper.maleFemaleYears(df)
    fig = px.line(final,x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)



