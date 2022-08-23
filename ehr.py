import streamlit as st
import pandas as pd
import plotly.express as px
import itertools
import numpy as np
from pycaret.regression import setup, create_model, finalize_model, predict_model
from ehr_db import create_table, add_data, view_all_data, view_all_data_names, get_name, edit_name_data, delete_data
sign_in = ''
st.set_page_config(layout="wide",
   page_title="CrossData 🏋️‍",
   page_icon="chart_with_upwards_trend", initial_sidebar_state="collapsed")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


HEADER_COLOR_CYCLE = itertools.cycle(
    [
        "#00c0f2",  # light-blue-70",
        "#ffbd45",  # "orange-70",
        "#00d4b1",  # "blue-green-70",
        "#1c83e1",  # "blue-70",
        "#803df5",  # "violet-70",
        "#ff4b4b",  # "red-70",
        "#21c354",  # "green-70",
        "#faca2b",  # "yellow-80",
    ]
)
    
def colored_header(label, description=None, color=None):
    """Shows a header with a colored underline and an optional description."""
    st.write("")
    if color is None:
        color = next(HEADER_COLOR_CYCLE)
    st.subheader(label)
    st.write(
        f'<hr style="background-color: {color}; margin-top: 0; margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)
def predict_future(data):
    data = data[data['reps'] ==1]
    data['Work Outs'] = np.arange(1,len(data)+1)
    data = data[['Work Outs', 'weight']] 
    data1 = data.append(data)
    data1 = data.append(data)
    data1 = data.append(data)
    s = setup(data = data1, silent=True,fold=2, target = 'weight', fold_strategy = 'timeseries', data_split_shuffle = False,numeric_features = ['Work Outs'])
    lar = create_model('lar')
    final = finalize_model(lar)
    future_df = pd.DataFrame({'Work Outs':[data['Work Outs'].iloc[-1] + 1, data['Work Outs'].iloc[-1] + 2, data['Work Outs'].iloc[-1] + 3,data['Work Outs'].iloc[-1] + 4, data['Work Outs'].iloc[-1] + 5]})
    future_df = data.append(future_df)
    predict_future = predict_model(final, data=future_df)
    return predict_future             
def main(name):

    st.title("CrossData 🏋️‍")
    ADD, DISPLAY, TABLES, ABOUT= st.tabs(["Add Workout", "Workout Analytics", "Max Tables and Projections", "About"])

    create_table()
    with ADD:
        st.info("Welcome " + name + " hope you rocked your workout")
        with st.expander("Add"):

                date = st.date_input("Enter Date")
                lift = st.selectbox('Select Lift',('','Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts', 'Front Box Squat', 'Front Pause Squat', 'Overhead Squat', 'Push Jerk', 'Split Jerk', 'Squat Jerk', 'Hang Power Snatch', 'Hang Squat Snatch', 'Power Snatch', 'Snatch', 'Squat Snatch', 'Romainian Deadlift', 'Sumo Deadlift', 'Clean and Jerk', 'Power Clean and Jerk'))
                weight = st.text_input("Enter Weight")
                sets = st.text_input("Enter Reps")
                time = st.text_input("Amount of Time")
                sentiment = st.selectbox("Select Sentiment", ("", "Positive", "Neutral", "Negative"))
                notes = st.text_input("Enter Notes")

                if st.button("ADD DETAILS"):
                        add_data(name, date, lift, weight, sets,time, sentiment, notes)
                        st.success("SUCCESSFULLY ADDED: {}".format(date))


    with DISPLAY:
        result = view_all_data()
        df = pd.DataFrame(result, columns=['name', 'date', 'lift', 'weight', 'sets','time', 'sentiment', 'notes'])
        df = df[df['name'] == name]


        try:
            result = view_all_data()
            df = pd.DataFrame(result, columns=['name', 'date', 'lift', 'weight', 'sets','time', 'sentiment', 'notes'])
            df = df[df['name'] == name]
            ch1, ch2 = st.columns(2)
            with ch1:
                colored_header("Sentiment Analysis")
            with ch2:
                colored_header("Lift Distribution")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                
                sent_fig = px.pie(df, names='sentiment',color='sentiment', color_discrete_map={'Positive':'lightgreen',
                                     'Negative':'red',
                                     'Neutral':'lightgray',
                                     '':'lightgray'})
                sent_fig.update_layout(width=400,height=400,showlegend=False)
                sent_fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(sent_fig, config= dict(
                    displayModeBar = False))
            with col2:
                sent_fig2 = px.scatter(df, x='date',y='sentiment',color='sentiment', color_discrete_sequence=['lightgreen','red', 'lightgray'],category_orders={"sentiment": ["Positive",'Negative', 'Neutral']})
                sent_fig2.update_layout(hovermode='x unified',width=200, height=400, showlegend=False,yaxis_visible=False, yaxis_showticklabels=False,xaxis_visible=False, xaxis_showticklabels=False)
                sent_fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
                st.plotly_chart(sent_fig2, config= dict(
                    displayModeBar = False))
    
            with col3:
                
                lift_fig = px.pie(df, names='lift')
                lift_fig.update_layout(width=400,height=400, showlegend=False)
                lift_fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(lift_fig, config= dict(
                    displayModeBar = False))
            with col4:
                lift_fig2 = px.scatter(df, x='date',y='lift',color='lift', symbol='lift')
                lift_fig2.update_layout(hovermode='x unified',width=200, height=400, showlegend=False,yaxis_visible=False, yaxis_showticklabels=False,xaxis_visible=False, xaxis_showticklabels=False)
                lift_fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
                st.plotly_chart(lift_fig2, config= dict(
                    displayModeBar = False))

    
            df['reps'] = df['sets'].astype(int)
            df['weight'] = df['weight'].astype(float)
            prog_df = df[df['reps'] < 4]
            colored_header("Progress")
            prog_fig = px.histogram(prog_df, x="date", y = 'weight',color='lift', facet_row='lift',barmode='group', width=1100,height=600,hover_data=["reps"])
            prog_fig.update_layout(showlegend=False,hovermode='x unified')
            prog_fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
            st.plotly_chart(prog_fig, config= dict(
                    displayModeBar = False))
        except:
            st.error("Enter your first workout!")
    with TABLES:
        colored_header("Recent 1 Rep Max Data")
        c1, c2, c3 = st.columns(3)
        maxes = df[df['sets']=='1']
        try:
            maxesq = maxes[maxes['lift'] == "Back Squats"]
            lastsq = int(maxesq['weight'].iloc[0])
            recentsq = int(maxesq['weight'].max())
            difsq = recentsq - lastsq
            with c1:
                st.metric(label="Back Squat",value = recentsq, delta=difsq)
                
        except:
            with c1:
                st.metric(label='Back Squat', value = 0, delta=0)
                
        try:
            maxb = maxes[maxes['lift'] == "Bench Press"]
            lastbp = int(maxb['weight'].iloc[0])
            recentbp = maxb['weight'].astype(int).max()
            difbp = recentbp - lastbp
            with c2:
                st.metric(label="Bench Press",value = recentbp, delta=difbp)
                
        except:
            with c2:
               st.metric(label='Bench Press', value=0, delta=0)
         
        try:
            maxd = maxes[maxes['lift'] == "Deadlifts"]   
            lastdl = int(maxd['weight'].iloc[0])
            recentdl = maxd['weight'].astype(int).max()
            difdl = recentdl - lastdl
            with c3:
                st.metric(label="Dead Lift",value = recentdl, delta=difdl)
                
        except:
            with c3:
                st.metric(label="Dead lift", value = 0, delta = 0)
        try:
            colored_header("Percentage Table")
            maxtable = pd.DataFrame()
            maxtable['Lifts'] = df['lift'].unique()
            namedf = df[df['name']==name]
            ind = 0
            maxtable['100%'] = 'na'
            maxtable['95%'] = 'na'
            maxtable['90%'] = 'na'
            maxtable['85%'] = 'na'
            maxtable['80%'] = 'na'
            maxtable['75%'] = 'na'
            maxtable['70%'] = 'na'
            maxtable['65%'] = 'na'
            maxtable['60%'] = 'na'
            maxtable['55%'] = 'na'
            maxtable['50%'] = 'na'
            maxtable['45%'] = 'na'
            maxtable['40%'] = 'na'
            maxtable['35%'] = 'na'
            maxtable['30%'] = 'na'
            maxtable['25%'] = 'na'
            maxtable['20%'] = 'na'
            maxtable['15%'] = 'na'
            maxtable['10%'] = 'na'
            maxtable['5%'] = 'na'
            for lft in namedf['lift'].unique():
                #maxtable['Lifts'].iloc[0] = str(lft)
                print(lft)
                liftdf = namedf[namedf['lift'] == lft]
                liftdf['weight'] = liftdf['weight'].astype(float)
                for i in range(len(maxtable)):
                    
                    maxlft = liftdf['weight'].max()
                    maxtable['100%'].iloc[ind] = maxlft
                    maxtable['95%'].iloc[ind] = round(maxlft * 0.95, 2)
                    maxtable['90%'].iloc[ind] = round(maxlft * 0.90, 2)
                    maxtable['85%'].iloc[ind] = round(maxlft * 0.85,2)
                    maxtable['80%'].iloc[ind] = round(maxlft * 0.80,2)
                    maxtable['75%'].iloc[ind] = round(maxlft * 0.75,2)
                    maxtable['70%'].iloc[ind] = round(maxlft * 0.70,2)
                    maxtable['65%'].iloc[ind] = round(maxlft * 0.65,2)
                    maxtable['60%'].iloc[ind] = round(maxlft * 0.60,2)
                    maxtable['55%'].iloc[ind] = round(maxlft * 0.55,2)
                    maxtable['50%'].iloc[ind] = round(maxlft * 0.50,2)
                    maxtable['45%'].iloc[ind] = round(maxlft * 0.45,2)
                    maxtable['40%'].iloc[ind] = round(maxlft * 0.40,2)
                    maxtable['35%'].iloc[ind] = round(maxlft * 0.35,2)
                    maxtable['30%'].iloc[ind] = round(maxlft * 0.30,2)
                    maxtable['25%'].iloc[ind] = round(maxlft * 0.25,2)
                    maxtable['20%'].iloc[ind] = round(maxlft * 0.20,2)
                    maxtable['15%'].iloc[ind] = round(maxlft * 0.15,2)
                    maxtable['10%'].iloc[ind] = round(maxlft * 0.10,2)
                    maxtable['5%'].iloc[ind]= round(maxlft * 0.05,2)
                ind = ind + 1
            st.dataframe(maxtable)


        except:
            pass
                
        try:
            st.sidebar.dataframe(df)
            for lts in df['lift'].unique():
                d1 = df[df['lift'] == lts]
                if len(d1[d1['reps']==1]) > 3:
                    predictions = predict_future(data=d1)
                    predictions['predictions'] = predictions['Label']
                    predictions['past weight'] = predictions['weight']
                    predictions['1 Rep Max Attempt'] = predictions['Work Outs']
                    fig = px.line(predictions, x='1 Rep Max Attempt', y=['predictions', 'past weight'], markers=True)
                    # add a vertical rectange for test-set separation
                    fig.add_vrect(x0=predictions['Work Outs'].iloc[-5], x1=predictions['Work Outs'].iloc[-1], fillcolor="grey", opacity=0.25, line_width=0)
                    fig.update_layout(width=1100,yaxis_title="1 Rep Weight Predictions", hovermode='y unified')
                    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
                    colored_header('1 Rep Max Projections: ' + lts)
                    st.plotly_chart(fig, config= dict(
                    displayModeBar = False))
        except:
            pass
    
        


    with ABOUT:
        st.subheader("CrossData 🏋️‍")
        st.text("CrossData is a simple tool to log CrossFit data")
        st.text("For questions or comments, please contact Cole Hagen @ hagencolej@gmail.com")

if __name__ == '__main__':
    st.sidebar.title('CrossData 🏋️‍')
    placeholder = st.empty()
    with st.sidebar.empty():
        sign_in = st.sidebar.text_input("User Name")
        password =st.sidebar.text_input("Password")
    if password == 'ella':
        main(name=sign_in)

