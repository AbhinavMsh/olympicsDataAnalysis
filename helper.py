import numpy as np

def medal_tally(df, select_year, select_country):
    # returns dataframe with medal tally according to user filter

    # assigning medal_tally for return to work
    medal_tally = df
    # if selected year and selected country are overall
    if select_year == 'Overall' and select_country == 'Overall':
        # dropping duplicates of team events so in medal counting
        medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        # sorting by Gold
        medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
        # adding total column
        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    # select year is overall and any country selected
    elif select_year == 'Overall':
        # dropping duplicates of team events so in medal counting
        medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        # taking only the selecting country
        medal_tally = medal_tally[medal_tally['region'] == select_country][['Year','Gold', 'Silver', 'Bronze']]
        # summing each year medals
        medal_tally = medal_tally.groupby('Year').sum().reset_index()
        # adding total column
        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    elif select_country == 'Overall':
        medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        # taking only the selecting year
        # country that have not played will be removed so list gets small
        medal_tally = medal_tally[medal_tally['Year'] == select_year]
        # sorting by Gold
        medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
        # adding total column
        medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    else:
        # taking only the selecting year
        medal_tally = medal_tally[medal_tally['Year'] == select_year]
        # taking only the selecting country
        medal_tally = medal_tally[medal_tally['region'] == select_country][['Name', 'Event', 'Gold', 'Silver', 'Bronze']]

    return medal_tally.reset_index(drop=True)

def country_years_list(df):
    # Returns variables containing unique years and countries

    # extracting unique years
    years = np.sort(df['Year'].unique())
    years = list(years)
    years.insert(0, 'Overall')

    # extracting unique countries
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country
def sportsListFind(df):
    # return variable containing unique sports

    sports = np.sort(df['Sport'].unique())
    sports = list(sports)
    sports.insert(0, 'Overall')

    return sports

def partNationsOverTime(df):
    # returns dataframe of participating nation every year

    # dropping duplicate rows
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year']
    # counting and sorting value
    nations_over_time = nations_over_time.value_counts().reset_index().sort_values('Year').reset_index(drop=True)
    # renaming columns
    nations_over_time = nations_over_time.rename(columns={'Year': 'Edition', 'count': 'No of Countries'})
    return nations_over_time

def dataOverTime(df):
    # return dataframe of Events hosted every year

    # dropping duplicate rows
    eventsOverTime = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts()
    # counting and sorting value
    eventsOverTime = eventsOverTime.reset_index().sort_values('Year').reset_index(drop=True)
    # renaming columns
    eventsOverTime = eventsOverTime.rename(columns={'Year': 'Edition','count': 'Events'})
    return eventsOverTime

def athletesOverTime(df):
    # returns dataframe of participated athletes every year

    # dropping duplicate rows
    athletesOverTime = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts()
    # counting and sorting value
    athletesOverTime = athletesOverTime.reset_index().sort_values('Year').reset_index(drop=True)
    # renaming columns
    athletesOverTime = athletesOverTime.rename(columns={'Year': 'Edition','count': 'Athletes'})
    return athletesOverTime

def decoratedAthletes(df, optionSport):
    # returns dataframe of athletes with medals sorted descending

    if optionSport == 'Overall':
        # dropping duplicates
        decoratedAthletes = df.drop_duplicates()
        # extracting individual athlete and adding their medals
        decoratedAthletes = decoratedAthletes.groupby(['Name', 'region', 'Sport'])[
            ['Gold', 'Silver', 'Bronze']].sum().reset_index()
        # calculating Total col
        decoratedAthletes['Total'] = decoratedAthletes['Gold'] + decoratedAthletes['Silver'] + decoratedAthletes['Bronze']
        # sorting based on Total col
        decoratedAthletes = decoratedAthletes.sort_values('Total', ascending=False).reset_index(drop=True)
    else:
        # dropping duplicates
        decoratedAthletes = df.drop_duplicates()

        decoratedAthletes = decoratedAthletes[decoratedAthletes['Sport']== optionSport]

        decoratedAthletes = decoratedAthletes.groupby(['Name', 'region'])[
            ['Gold', 'Silver', 'Bronze']].sum().reset_index()
        # calculating Total col
        decoratedAthletes['Total'] = decoratedAthletes['Gold'] + decoratedAthletes['Silver'] + decoratedAthletes['Bronze']
        # sorting based on Total col
        decoratedAthletes = decoratedAthletes.sort_values('Total', ascending=False).reset_index(drop=True)

    return decoratedAthletes
def countryTopStats(df, optionCountry):
    # Returns variables containing statistics of the selected country
    x = df[df['region'] == optionCountry]
    sportsPart =  x['Sport'].unique().shape[0]
    eventsPart = x['Event'].unique().shape[0]
    athletesPart = x['Name'].unique().shape[0]
    medalTally = x['Gold'].sum() + x['Silver'].sum() + x['Bronze'].sum()

    return sportsPart, eventsPart, athletesPart, medalTally


def countryMedalTally(df,optionCountry):
    # returns dataframe with medal tally for every year

    medalTally = df.drop_duplicates()
    # selecting only option country
    medalTally = medalTally[medalTally['region'] == optionCountry]
    # dropping repeating medals entry for team events
    medalTally = medalTally.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # Grouping data by year and adding up medals and sorting
    medalTally = medalTally.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index().sort_values('Year')
    # Initializing Total col
    medalTally['Total'] = medalTally[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    return medalTally

def countryHeatMap(df, optionCountry):
    # dropping duplicates
    heatMapData= df.drop_duplicates()
    # extracting selected country data
    heatMapData= heatMapData[heatMapData['region'] == optionCountry]
    # dropping team events as they affect medal tally
    heatMapData= heatMapData.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # Grouping data
    heatMapData= heatMapData.groupby(['Year', 'Sport'])[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    # Adding total col
    heatMapData['Total'] = heatMapData[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    # dataframe to pivot table for Heatmap
    heatMapData = heatMapData.pivot_table(index='Sport', columns='Year', values='Total').fillna(0)

    return heatMapData

def bestAthletes(df,optionCountry):
    # dropping duplicates
    athletes = df.drop_duplicates()
    # extracting selected country data
    athletes = athletes[athletes['region'] == optionCountry]
    # Grouping data
    athletes = athletes.groupby(['Name', 'Sport'])[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    # Adding total col
    athletes['Total'] = athletes[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    # sorting values based on descending medal tally
    athletes = athletes.sort_values(by='Total', ascending=False).reset_index(drop=True)

    return athletes.head(10)

def distPlotData(df):
    athleteDf = df.drop_duplicates(subset=['Name','region'])
    x1=athleteDf['Age'].dropna()
    x2=athleteDf[athleteDf['Medal'] == 'Gold']['Age'].dropna()
    x3=athleteDf[athleteDf['Medal'] == 'Silver']['Age'].dropna()
    x4=athleteDf[athleteDf['Medal'] == 'Bronze']['Age'].dropna()

    return x1,x2,x3,x4

def scatterPlotGoldMedalist(df,optSport):

    ath = df if optSport == 'Overall' else df[df['Sport'] == optSport]
    ath['Medal'] = ath['Medal'].fillna('No Medal')
    return ath

def maleFemaleYears(df):
    men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final