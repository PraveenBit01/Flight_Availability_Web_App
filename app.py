import streamlit as st
from dbhelper import DB
import pandas as pd
import plotly.graph_objects as go

db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox('Menu',['Select One','Check Flights','Analytics'])

if user_option == 'Check Flights' :
    st.title('Check Flights')

    col1,col2 = st.columns(2)
    city = db.fetch_city_names()

    with col1 :
        source = st.selectbox('Source',sorted(city))

    with col2 :
        destination = st.selectbox('Destination',sorted(city))
    
    if st.button('Search') :
        result = db.fetch_all_cities(source,destination)
        if len(result) == 0 :
            st.write('Sorry , There is no flights Right Now')
        else :
            df = pd.DataFrame(result, columns=['Airline','Route','Dep_Time','Duration','Price'])
            st.dataframe(df)

elif user_option == 'Analytics' :

    airline,frequency = db.fetch_airline_frequency()
    city,frequency1 = db.busy_airport()
    dates, frequency2 = db.daily_frequency()  

    # Create charts
    # Pie Chart
    pie_fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value",
        )
    )
    pie_fig.update_layout(
        title="Airline Frequency Distribution",
        template='plotly_white',
        height=600,  
        width=800    
    )

    # Bar Chart
    bar_fig = go.Figure(
        go.Bar(
            x=city,
            y=frequency1,
            hoverinfo="x+y",
            textposition="auto",
            marker=dict(color='#1f77b4')
        )
    )
    bar_fig.update_layout(
        title="Airline Frequency by City",
        xaxis_title="City",
        yaxis_title="Frequency",
        template='plotly_white'
    )

    # Line Chart
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(
        x=dates,
        y=frequency2,
        mode='lines+markers',
        line=dict(color='firebrick', width=2),
        marker=dict(size=8),
        name='Frequency'
    ))
    line_fig.update_layout(
        title="Frequency over Time",
        xaxis_title="Date",
        yaxis_title="Frequency",
        template='plotly_white',
        xaxis=dict(type='date')
    )

    # Display charts in a dashboard layout
    st.header("Analytics Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pie Chart")
        st.plotly_chart(pie_fig)
    
    with col2:
        st.subheader("Bar Chart")
        st.plotly_chart(bar_fig)

    st.subheader("Line Chart")
    st.plotly_chart(line_fig)

else :
    # Project description
    st.title('About the Project')
    st.write("""
    This project is aimed at providing insights into flight data analytics. Whether you're planning your next trip or
    interested in exploring trends in airline industry, our analytics dashboard has got you covered. Here's what you can
    do with our app:

    - **Check Flights**: Search for available flights between different cities.
    - **Analytics**: Explore various analytics charts such as Airline Frequency Distribution, Airline Frequency by City,
      and Frequency over Time to gain insights into flight patterns and trends.

    Get ready to embark on a journey of discovery with our Flight Analytics app!
    """)

