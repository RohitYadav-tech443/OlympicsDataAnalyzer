import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('athlete_events_small.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

# st.dataframe(df)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    # yahan neeche jo tum naam rakhte ho usko hasmeaha file mein jo naam hai usse same rakhna hai
    year,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select year",year)
    selected_country=st.sidebar.selectbox("Select country",country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in "+ str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Total medal's overall "+ str(selected_country))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country) +"has the total medals" +str(selected_year))

    st.table(medal_tally)


if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0] -1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events= df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Nations')
        st.title(nations)

    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Nations over time")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events over time")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title("Athletes over time")
    st.plotly_chart(fig)

    st.title("No of events over time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))

    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot=x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')

    sns.heatmap(pivot,ax=ax,annot=True)
    st.pyplot(fig)

    # most successful players
    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

# Country wise analysis
if user_menu == "Country-wise Analysis":

    st.title("Country-wise Analysis")
    country_list=df['region'].unique().tolist()
    selected_country=st.selectbox("Select a country",country_list)
    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title("Medal Tally over the years for  "+selected_country)
    st.plotly_chart(fig)

    st.title(selected_country+" excels in the following events")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Most successful players by the country "+selected_country)
    top15=helper.most_successful_player_country(df,selected_country)
    st.table(top15)

if user_menu == "Athlete wise Analysis":

    st.title("Athlete wise Analysis")
    athlete_df = df.drop_duplicates(subset=['Team', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ["Overall Age", "Gold", "Silver", "Bronze"], show_hist=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    name=[]
    x=[]
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
        'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
        'Water polo', 'Hockey', 'Rowing', 'Fencing',
        'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
        'Tennis', 'Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens',
        'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]

    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport'] == sport]
        ages=temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()

        if len(ages)>1:
            x.append(ages)
            name.append(sport)

    fig=ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age with Sport(Gold Medalist) ")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height v\s Weight")
    selected_sport=st.selectbox("Select a sport",sport_list)
    temp_df= helper.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    # df.to_csv('athlete_events_small2.csv', index=False)
