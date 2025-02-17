import pandas as pd
import psycopg2
import streamlit as st 
import sqlalchemy
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#Changing backround color of a webpage
bg_color = '#000000' # This color code taken from HTML color codes 
st.markdown(f"""<style>.stApp {{background-color: {bg_color};}}</style>""",unsafe_allow_html=True)

col1, col2 = st.columns([0.9, 0.19]) 

with col1:
    st.markdown("<h1 style='font-family: Times New Roman; color: white;'>   Bird species analysis</h1>", unsafe_allow_html=True)

with col2:
    st.image(r"C:\Users\lenovo\Downloads\images (10).jpeg")


connection = psycopg2.connect(
host = "localhost",user = "postgres" , password = "begin25",database = "birds_data")
cursor = connection.cursor()
cursor.execute("select * from forest_birds_observation") 
forest = cursor.fetchall() 

forest_df=pd.DataFrame(forest)
forest_df.columns=['Admin_Unit_Code', 'Site_Name', 'Plot_Name',
       'Location_Type', 'Year', 'Date', 'Start_Time', 'End_Time', 'Observer',
       'Visit', 'Interval_Length', 'ID_Method', 'Distance', 'Flyover_Observed',
       'Sex', 'Common_Name', 'Scientific_Name', 'AcceptedTSN', 'NPSTaxonCode',
       'AOU_Code', 'PIF_Watchlist_Status', 'Regional_Stewardship_Status',
       'Temperature', 'Humidity', 'Sky', 'Wind', 'Disturbance',
       'Initial_Three_Min_Cnt']


cursor.execute("select * from grassland_birds_observation") 
grassland = cursor.fetchall() 
grassland_df=pd.DataFrame(grassland)
grassland_df.columns=['Admin_Unit_Code', 'Plot_Name', 'Location_Type',
       'Year', 'Date', 'Start_Time', 'End_Time', 'Observer', 'Visit',
       'Interval_Length', 'ID_Method', 'Distance', 'Flyover_Observed', 'Sex',
       'Common_Name', 'Scientific_Name', 'AcceptedTSN', 'TaxonCode',
       'AOU_Code', 'PIF_Watchlist_Status', 'Regional_Stewardship_Status',
       'Temperature', 'Humidity', 'Sky', 'Wind', 'Disturbance',
       'Previously_Obs', 'Initial_Three_Min_Cnt']

options=st.sidebar.radio("",['Home','Seasonal Trends','Observation Time','Location Insights','Plot-Level Analysis'
                             ,'Activity Patterns','Weather Correlation','Disturbance Effect','Distance Analysis'
                             ,'Flyover Frequency','Observer Bias','Visit Patterns','Watchlist Trends','AOU Code Patterns'])

if options=='Home':
    #forest birds

    fb=forest_df[['Common_Name', 'Scientific_Name']]
    fb_unique = fb.value_counts().reset_index()
    fb_unique.drop(columns='count',inplace=True)

    observers_forest = forest_df[['Observer','Common_Name']]
    observers_gl=grassland_df[['Observer','Common_Name']]
    observers_forest_count = observers_forest.Common_Name.groupby(observers_forest.Observer).nunique().reset_index(name='Observerd species')



    #grassland

    gb=grassland_df[['Common_Name', 'Scientific_Name']]
    gb_unique = gb.value_counts().reset_index()
    gb_unique.drop(columns='count',inplace=True)

    observers_gl_count = observers_gl.Common_Name.groupby(observers_gl.Observer).nunique().reset_index(name='Observerd species')

    torism_forest = forest_df[['Admin_Unit_Code','Common_Name']]
    torism_gl = grassland_df[['Admin_Unit_Code','Common_Name']]
    torism_forest_count = torism_forest.Common_Name.groupby(torism_forest.Admin_Unit_Code).nunique().reset_index(name='No.of.species')
    torism_forest_count = torism_forest_count.sort_values(by="No.of.species", ascending=False)
    torism_forest_count_fin=torism_forest_count.head(3)
    torism_gl_count = torism_gl.Common_Name.groupby(torism_gl.Admin_Unit_Code).nunique().reset_index(name='No.of.species')
    torism_gl_count = torism_gl_count.sort_values(by="No.of.species", ascending=False)
    torism_gl_count_fin=torism_gl_count.head(3)

    risk_forest=forest_df[['Location_Type','Common_Name','Visit',  'PIF_Watchlist_Status', 'Regional_Stewardship_Status']]
    risk_forest_filter=risk_forest[(risk_forest['PIF_Watchlist_Status']==True) & (risk_forest['Regional_Stewardship_Status']==True)]
    risk_forest_filter_count=risk_forest_filter.value_counts(subset=['Common_Name',	'Visit'	,'PIF_Watchlist_Status','Regional_Stewardship_Status']).reset_index()

    risk_gl=grassland_df[['Location_Type','Common_Name','Visit',  'PIF_Watchlist_Status', 'Regional_Stewardship_Status']]
    risk_gl_filter=risk_gl[(risk_gl['PIF_Watchlist_Status']==True) & (risk_gl['Regional_Stewardship_Status']==True)]
    risk_gl_filter_count=risk_gl_filter.value_counts().reset_index()
    
    risk_forest_filter_count_final=risk_forest_filter_count[['Common_Name','PIF_Watchlist_Status','Regional_Stewardship_Status']]
    risk_forest_filter_count_final1 = risk_forest_filter_count_final.value_counts().reset_index()
    risk_forest_filter_count_final1.drop(columns='count',inplace=True)
    
    risk_gl_filter_count_final=risk_gl_filter_count[['Common_Name','PIF_Watchlist_Status','Regional_Stewardship_Status']]
    risk_gl_filter_count_final1 = risk_gl_filter_count_final.value_counts().reset_index()
    risk_gl_filter_count_final1.drop(columns='count',inplace=True)
    

    forest, grassland = st.columns([0.5, 0.5]) 
    with forest:
        st.subheader('Forest species')
        st.write(fb_unique)
        st.subheader('Forest Observer')
        st.write(observers_forest_count)
        st.subheader('Suggested tourism')
        st.subheader('Forest')
        st.write(torism_forest_count_fin)
        st.subheader('Rare species - Forest')
        st.write(risk_forest_filter_count_final1)

    with grassland:
        st.subheader('Grassland species')
        st.write(gb_unique)
        st.subheader('Grassland Observer')
        st.write(observers_gl_count)
        st.subheader('Suggested tourism')
        st.subheader('Grassland')
        st.write(torism_gl_count_fin)
        st.subheader('Rare species - Grassland')
        st.write(risk_gl_filter_count_final1)
        
    

if options == 'Seasonal Trends':
    seasons_forest=forest_df[['Date','Common_Name']]
    seasons_forest['Month']=seasons_forest['Date'].dt.month
    def get_season(month):
        if month in [12, 1, 2]: return 'Winter'
        elif month in [3, 4, 5]: return 'Spring'
        elif month in [6, 7, 8]: return 'Summer'
        else: return 'Fall'
    seasons_forest['Season'] = seasons_forest['Month'].apply(get_season)
    SeasonalTrends_forest=seasons_forest.Common_Name.groupby(seasons_forest.Season).value_counts().reset_index(name="Sightings observed")
    st_forest=px.bar(SeasonalTrends_forest,x='Common_Name',y='Sightings observed',color='Season')
    st_forest.update_layout(title="Seasonal trends in forest") 
    st_forest.show()  
    st.plotly_chart(st_forest)    
    seasons_grassland=grassland_df[['Date','Common_Name']]
    seasons_grassland['Month']=seasons_grassland['Date'].dt.month
    seasons_grassland['Season'] = seasons_grassland['Month'].apply(get_season)
    SeasonalTrends_grassland=seasons_grassland.Common_Name.groupby(seasons_grassland.Season).value_counts().reset_index(name="Sightings observed")
    st_grassland=px.bar(SeasonalTrends_grassland,x='Common_Name',y='Sightings observed',color='Season')
    st_grassland.update_layout(title="Seasonal trends in grassland") 
    st_grassland.show()
    st.plotly_chart(st_grassland) 

if options == 'Observation Time':
    observation_forest=forest_df[['Date', "Start_Time", "End_Time","Common_Name"]]
    observation_forest['Date'] = observation_forest['Date'].astype(str)
    observation_forest['Start_Time'] = observation_forest['Start_Time'].astype(str)
    observation_forest['Time']= observation_forest['Date'].astype(str) + ' ' + observation_forest['Start_Time']
    observation_forest['Time'] = pd.to_datetime(observation_forest['Time'])

# Extract hour
    observation_forest['Time_of_observation'] = observation_forest['Time'].dt.hour
    observation_forest_activity = observation_forest['Time_of_observation'].value_counts().reset_index(name='Birds activity monitored')
    ot_forest=px.bar(observation_forest_activity,x='Time_of_observation',y='Birds activity monitored',color='Time_of_observation')
    ot_forest.update_layout(title='Forest birds activity')
    ot_forest.show()
    st.plotly_chart(ot_forest) 
    observation_grassland=grassland_df[['Date', "Start_Time", "End_Time","Common_Name"]]
    observation_grassland['Date'] = observation_grassland['Date'].astype(str)
    observation_grassland['Start_Time'] = observation_grassland['Start_Time'].astype(str)
    observation_grassland['Time']= observation_grassland['Date'] + ' ' + observation_grassland['Start_Time']
    observation_grassland['Time'] = pd.to_datetime(observation_grassland['Time'])

# Extract hour
    observation_grassland['Time_of_observation'] = observation_grassland['Time'].dt.hour
    observation_grassland_activity= observation_grassland['Time_of_observation'].value_counts().reset_index(name='Birds activity monitored')
    ot_grassland=px.bar(observation_grassland_activity,x='Time_of_observation',y='Birds activity monitored',color='Time_of_observation')
    ot_grassland.update_layout(title='Grassland birds activity')
    ot_grassland.show()
    st.plotly_chart(ot_grassland) 

if options == 'Location Insights':
    st.subheader("Forest vs Grassland")
    forest_loc=forest_df[['Location_Type', 'Common_Name']]
    grassland_loc=grassland_df[['Location_Type', 'Common_Name']]
    location_ins = pd.concat([forest_loc, grassland_loc], ignore_index=True)
    unique_species=location_ins.Common_Name.groupby(location_ins.Location_Type).nunique().reset_index(name="Species identified")
    location=px.bar(unique_species,x='Location_Type',y='Species identified',color='Location_Type')
    location.update_layout(title=" Biodiversity hotspots") 
    location.show()
    st.plotly_chart(location)

if options == 'Plot-Level Analysis':
    plt_forest=forest_df[['Plot_Name','Location_Type', 'Common_Name']]
    plt_analysis_forest=plt_forest.Common_Name.groupby(plt_forest.Plot_Name).nunique().reset_index(name='Species identified')
    plt_analysis_forest_ = plt_analysis_forest.sort_values(by="Species identified", ascending=False)
    plt_analysis_forest_10=plt_analysis_forest_.head(10)
    pla_forest=px.bar(plt_analysis_forest_10,x='Plot_Name',y='Species identified',color='Plot_Name')
    pla_forest.update_layout(title="Plots attract more species - Forest") 
    pla_forest.show()
    st.plotly_chart(pla_forest)
    plt_grassland=grassland_df[['Plot_Name','Location_Type','Common_Name']]
    plt_analysis_grassland=plt_grassland.Common_Name.groupby(plt_grassland.Plot_Name).nunique().reset_index(name='Species identified')
    plt_analysis_grassland_ = plt_analysis_grassland.sort_values(by="Species identified", ascending=False)
    plt_analysis_grassland_10=plt_analysis_grassland_.head(10)
    pla_grassland=px.bar(plt_analysis_grassland_10,x='Plot_Name',y='Species identified',color='Plot_Name')
    pla_grassland.update_layout(title="Plots attract more species - Grassland") 
    pla_grassland.show()
    st.plotly_chart(pla_grassland)

if options == 'Activity Patterns':
    ap_forest=forest_df[['Interval_Length', 'ID_Method']]
    ap_gl=grassland_df[['Interval_Length', 'ID_Method']]
    activity_forest = ap_forest['ID_Method'].value_counts().reset_index(name='observed_count')
    activity_grassland = ap_gl['ID_Method'].value_counts().reset_index(name='observed_count')
    forest_birds_acitivity=px.bar(activity_forest,x='ID_Method',y='observed_count',color='ID_Method')
    forest_birds_acitivity.update_layout(title="Common activity in Forest") 
    forest_birds_acitivity.show()
    st.plotly_chart(forest_birds_acitivity)
    grassland_birds_activity_=px.bar(activity_grassland,x='ID_Method',y='observed_count',color='ID_Method')
    grassland_birds_activity_.update_layout(title="Common activity in Grassland ") 
    grassland_birds_activity_.show()
    st.plotly_chart(grassland_birds_activity_)

if options == 'Weather Correlation':
    Weather_forest =forest_df[['Temperature','Humidity','Sky', 'Wind', 'Disturbance','Distance']]
    Weather_forest_grouped= Weather_forest.groupby(['Temperature','Humidity', 'Sky','Wind'])['Distance'].value_counts().rename('Observed').reset_index()
    weather_distance_correlation_forest=px.scatter(Weather_forest_grouped,x='Temperature',y='Observed' ,hover_data=['Distance','Sky','Wind','Humidity'],color='Sky')
    weather_distance_correlation_forest.update_layout(title='Forest weather analysis')
    weather_distance_correlation_forest.show()
    Weather_gl =grassland_df[['Temperature','Humidity','Sky', 'Wind', 'Disturbance','Distance']]
    grouped_gl= Weather_gl.groupby(['Temperature','Humidity', 'Sky','Wind'])['Distance'].value_counts().rename('Observed').reset_index()
    weather_distance_correlation_grassland=px.scatter(grouped_gl,x='Temperature',y='Observed' ,hover_data=['Distance','Sky','Wind','Humidity'],color='Sky')
    weather_distance_correlation_grassland.update_layout(title='Grassland weather analysis')
    weather_distance_correlation_grassland.show()
    st.plotly_chart(weather_distance_correlation_forest)
    st.plotly_chart(weather_distance_correlation_grassland)

if options == 'Disturbance Effect':
    Weather_forest =forest_df[['Temperature','Humidity','Sky', 'Wind', 'Disturbance','Distance']]
    forest_de= Weather_forest.groupby(['Temperature','Humidity', 'Sky','Wind'])['Disturbance'].value_counts().rename('Observed counts').reset_index()
    dist_forest=px.scatter(forest_de,x='Temperature',y='Humidity' ,hover_data=['Disturbance','Sky','Wind','Observed counts'],color='Disturbance',size='Observed counts')
    dist_forest.update_layout(title='Disturbance Effect in forest')
    dist_forest.show()
    Weather_gl =grassland_df[['Temperature','Humidity','Sky', 'Wind', 'Disturbance','Distance']]
    grassland_de= Weather_gl.groupby(['Temperature','Humidity', 'Sky','Wind'])['Disturbance'].value_counts().rename('Observed counts').reset_index()
    dist_grassland=px.scatter(grassland_de,x='Temperature',y='Humidity' ,hover_data=['Disturbance','Sky','Wind','Observed counts'],color='Disturbance',size="Observed counts")
    dist_grassland.update_layout(title='Disturbance Effect in Grassland')
    dist_grassland.show()
    st.plotly_chart(dist_forest)
    st.plotly_chart(dist_grassland)
    
if options == 'Distance Analysis':
    ditance_data_forest=forest_df[['Distance', 'Common_Name']]
    daf_count=ditance_data_forest.Common_Name.groupby(ditance_data_forest.Distance).size().reset_index(name='Observed counts')
    distance_analysis_forest=px.bar(daf_count,x='Distance',y='Observed counts',color='Distance')
    distance_analysis_forest.update_layout(title="Distance Analysis of forest birds") 
    distance_analysis_forest.show()
    daf_group=ditance_data_forest.Distance.groupby(ditance_data_forest.Common_Name).value_counts().reset_index(name="Observed counts")
    distance_analysis_species=px.bar(daf_group,x='Common_Name',y='Observed counts',color='Distance')
    distance_analysis_species.update_layout(title="Distance Analysis of forest bird species") 
    distance_analysis_species.show()
    st.plotly_chart(distance_analysis_forest)
    st.plotly_chart(distance_analysis_species)
    distance_data_gl=grassland_df[['Distance', 'Common_Name']]
    daf_gl=distance_data_gl.Common_Name.groupby(distance_data_gl.Distance).size().rename('observed count').reset_index()
    distance_analysis_gl=px.bar(daf_gl,x='Distance',y='observed count',color='Distance')
    distance_analysis_gl.update_layout(title="Distance Analysis of grassland birds") 
    distance_analysis_gl.show()
    daf_gl_species=distance_data_gl.Distance.groupby(distance_data_gl.Common_Name).value_counts().reset_index(name='Observed count')
    distance_analysis_gl_species=px.bar(daf_gl_species,x='Common_Name',y='Observed count',color='Distance')
    distance_analysis_gl_species.update_layout(title="Distance Analysis of grassland bird species") 
    distance_analysis_gl_species.show() 
    st.plotly_chart(distance_analysis_gl)
    st.plotly_chart(distance_analysis_gl_species)

if options == 'Flyover Frequency':
    Flyover_forest =forest_df[['Common_Name', 'Flyover_Observed']]
    Flyover_forest_group=Flyover_forest.Flyover_Observed.groupby(Flyover_forest.Common_Name).value_counts().reset_index(name='observed_count')
    Flyover_freq_forest=px.bar(Flyover_forest_group,x='Common_Name',y='observed_count',color='Flyover_Observed')
    Flyover_freq_forest.update_layout(title="Flyover_Observed forest") 
    Flyover_freq_forest.show()
    Flyover_gl=grassland_df[['Common_Name', 'Flyover_Observed']]
    Flyover_gl_group=Flyover_gl.Flyover_Observed.groupby(Flyover_gl.Common_Name).value_counts().reset_index(name='observed_count')
    Flyover_group_gl=px.bar(Flyover_gl_group,x='Common_Name',y='observed_count',color='Flyover_Observed')
    Flyover_group_gl.update_layout(title="Flyover_Observed grassland") 
    Flyover_group_gl.show()
    st.plotly_chart(Flyover_freq_forest)
    st.plotly_chart(Flyover_group_gl)

if options == "Observer Bias":
    observers_forest =forest_df[['Observer','Scientific_Name']]
    observer_groupd_forest=observers_forest.Scientific_Name.groupby(observers_forest.Observer).nunique().reset_index(name='Total_observed_species')
    observer_count_forest=px.bar(observer_groupd_forest,x='Observer',y='Total_observed_species',color='Observer')
    observer_count_forest.update_layout(title="Observers forest") 
    observer_count_forest.show()
    observer_gl =grassland_df[['Observer','Scientific_Name']]
    observer_grouped_gl=observer_gl.Scientific_Name.groupby(observer_gl.Observer).nunique().reset_index(name='Total_observed_species')
    observer_count_gl=px.bar(observer_grouped_gl,x='Observer',y='Total_observed_species',color='Observer')
    observer_count_gl.update_layout(title="Observers Grassland") 
    observer_count_gl.show()
    st.plotly_chart(observer_count_forest)
    st.plotly_chart(observer_count_gl)

if options == 'Visit Patterns' :
    forest_vp=forest_df[['Common_Name', 'Visit']]
    visit_counts_forest = forest_vp.groupby('Visit').size().reset_index(name='Total_Observations')
    visit_counts_forest = px.bar(visit_counts_forest, x='Visit', y='Total_Observations', title="Forest Visit patterns ",color='Visit')
    visit_counts_forest.show()
    species_diversity_forest = forest_vp.groupby('Visit')['Common_Name'].nunique().reset_index(name='Unique_Species')
    species_diversity_visit = px.bar(species_diversity_forest, x='Visit', y='Unique_Species', title="Forest Visit patterns by Species",color='Visit')
    species_diversity_visit.show()
    st.plotly_chart(visit_counts_forest)
    st.plotly_chart(species_diversity_visit) 
    vp_gl=grassland_df[['Common_Name', 'Visit']]
    visit_counts_gl = vp_gl.groupby('Visit').size().reset_index(name='Total_Observations')
    visit_counts_gl = px.bar(visit_counts_gl, x='Visit', y='Total_Observations',  title="Grassland Visit patterns",color='Visit')
    visit_counts_gl.show()
    species_diversity_gl = vp_gl.groupby('Visit')['Common_Name'].nunique().reset_index(name='Unique_Species')
    species_diversity_gl = px.bar(species_diversity_gl, x='Visit', y='Unique_Species', title="Grassland Visit patterns by Species",color='Visit')
    species_diversity_gl.show()
    st.plotly_chart(visit_counts_gl)
    st.plotly_chart(species_diversity_gl)

if options == 'Watchlist Trends':
    risk_forest=forest_df[['Location_Type','Common_Name','Visit',  'PIF_Watchlist_Status', 'Regional_Stewardship_Status']]
    risk_forest_filter=risk_forest[(risk_forest['PIF_Watchlist_Status']==True) & (risk_forest['Regional_Stewardship_Status']==True)]
    risk_forest_filter_count=risk_forest_filter.value_counts(subset=['Common_Name',	'Visit'	,'PIF_Watchlist_Status','Regional_Stewardship_Status']).reset_index()
    watchlist_forest = px.sunburst(risk_forest_filter_count,path=['Visit','Common_Name'],values='count',title="Forest birds watchlist")
    watchlist_forest.show()
    risk_gl=grassland_df[['Location_Type','Common_Name','Visit',  'PIF_Watchlist_Status', 'Regional_Stewardship_Status']]
    risk_gl_filter=risk_gl[(risk_gl['PIF_Watchlist_Status']==True) & (risk_gl['Regional_Stewardship_Status']==True)]
    risk_gl_filter_count=risk_gl_filter.value_counts().reset_index()
    watchlist_gl = px.sunburst(risk_gl_filter_count,path=['Visit','Common_Name'],values='count',title="Grassland birds watchlist")
    watchlist_gl.show()
    st.plotly_chart(watchlist_forest)
    st.plotly_chart(watchlist_gl)

if options == 'AOU Code Patterns':
    aou_forest=forest_df[['Common_Name', 'AOU_Code','Regional_Stewardship_Status' ]]
    aou_forest_group=aou_forest.groupby('AOU_Code')[["Common_Name","Regional_Stewardship_Status"]].value_counts().reset_index()
    aou_forest_filter=aou_forest_group[aou_forest_group['Regional_Stewardship_Status']==True]
    forest_aou=px.bar(aou_forest_filter,x='AOU_Code',y='count',color='Common_Name')
    forest_aou.update_layout(title="Forest conservation priorities") 
    forest_aou.show()
    aou_gl=grassland_df[['Common_Name', 'AOU_Code','Regional_Stewardship_Status' ]]
    aou_count_gl=aou_gl.groupby('AOU_Code')[["Common_Name","Regional_Stewardship_Status"]].value_counts(ascending=True).reset_index()
    aou_gl_filter=aou_count_gl[aou_count_gl['Regional_Stewardship_Status']==True]
    grassland_aou=px.bar(aou_gl_filter,x='AOU_Code',y='count',color='Common_Name')
    grassland_aou.update_layout(title="Grassland conservation priorities") 
    grassland_aou.show()
    st.plotly_chart(forest_aou)
    st.plotly_chart(grassland_aou)