import streamlit as st
import pandas as pd
import plotly.express as px
import itertools
import numpy as np
from pycaret.regression import setup, create_model, finalize_model, predict_model
from deta import Deta
deta = Deta("b02l5gt3_MFtTQuHFmWUEofyrn54FjjnWxAevcaY1")
users_db = deta.Base("fitusers")
wo_db = deta.Base("wodb")
#wo_db.put({"name": 'name', "date": 'date', "lift": 'lift', "weight": 'weight',"sets": 'sets', "time": 'time', 'sentiment': 'sentiment', 'notes': 'notes'})
st.set_page_config(layout="wide",
   page_title="CrossData 🏋️‍",
   page_icon="🏋️‍", initial_sidebar_state="collapsed")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
m = st.markdown("""
<style>
.streamlit-expander {
    position: fixed;
    bottom: 0;
    left: 0;
    width:500;
    display: flex;
    background-color: #ffffff
}

</style>""", unsafe_allow_html=True)



          



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
def main():
    st.title("CrossData 🏋️‍")

    DISPLAY, TABLES, ABOUT= st.tabs(["Workout Analytics", "Max Tables and Projections", "About"])
    
    result = wo_db.fetch().items
    result1 = users_db.fetch().items
    df = pd.DataFrame(result)
    df1 = pd.DataFrame(result1)
    name = df1['user_name'].iloc[-1]
    df = df[df['name'] == name]
    df = df[['lift','date','weight', 'sets', 'sentiment']]
    df = df.dropna()
    with st.expander("➕ Add Workout"):

        date = st.date_input("Enter Date")
        lift = st.selectbox('Select Lift',('Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts', 'Front Box Squat', 'Front Pause Squat', 'Overhead Squat', 'Push Jerk', 'Split Jerk', 'Squat Jerk', 'Hang Power Snatch', 'Hang Squat Snatch', 'Power Snatch', 'Snatch', 'Squat Snatch', 'Romainian Deadlift', 'Sumo Deadlift', 'Clean and Jerk', 'Power Clean and Jerk'))
        weight = st.text_input("Enter Weight")
        sets = st.text_input("Enter Reps")
        #time = st.text_input("Amount of Time")
        time = 5
        sentiment = st.selectbox("Select Sentiment", ("Positive", "Neutral", "Negative", "Not Sure"))
        #notes = st.text_input("Enter Notes")
        notes = 'no new notes'
        if st.button("➕"):
            wo_db.put({"name": name, "date": str(date), "lift": lift, "weight": weight,"sets": sets, "time": time, 'sentiment': sentiment, 'notes': notes})
            st.success("SUCCESSFULLY ADDED: {}".format(date))

    


    with DISPLAY:

        try:
            result = wo_db.fetch().items
            df = pd.DataFrame(result)
            df = df[df['name'] == name]
            df = df[['lift','date','weight', 'sets', 'sentiment']]
            df = df.dropna()
            df= df.loc[df['lift'].isin(['Back Squats', 'Front Squats', 'Overhead Squat', 'Split Squat', 'Clean', 'Hang Clean', 'Power Clean', 'Squat Clean', 'Bench Press', 'Push Press', 'Shoulder Press', 'Snatch Grip Push Press', 'Deadlifts', 'Front Box Squat', 'Front Pause Squat', 'Overhead Squat', 'Push Jerk', 'Split Jerk', 'Squat Jerk', 'Hang Power Snatch', 'Hang Squat Snatch', 'Power Snatch', 'Snatch', 'Squat Snatch', 'Romainian Deadlift', 'Sumo Deadlift', 'Clean and Jerk', 'Power Clean and Jerk'])]
            
                
            col1, col2 = st.columns(2)
            with col1:
                colored_header("Sentiment Analysis")
                sent_fig = px.pie(df, names='sentiment',color='sentiment', color_discrete_map={'Positive':'lightgreen',
                                     'Negative':'red',
                                     'Neutral':'lightgray',
                                     'Not Sure':'lightgray'})
                sent_fig.update_layout(width=400,height=400,showlegend=False)
                sent_fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(sent_fig, config= dict(
                    displayModeBar = False))
                
                sent_fig2 = px.scatter(df, x='date',y='sentiment',color='sentiment', color_discrete_sequence=['lightgreen','red', 'lightgray', 'lightgray'],category_orders={"sentiment": ["Positive",'Negative', 'Neutral', 'Not Sure']})
                sent_fig2.update_layout(hovermode='x unified',width=400, height=400, showlegend=False,yaxis_visible=False, yaxis_showticklabels=False,xaxis_visible=False, xaxis_showticklabels=False)
                sent_fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
                st.plotly_chart(sent_fig2, config= dict(
                    displayModeBar = False))
    
            with col2:
                colored_header("Lift Distribution")
                lift_fig = px.pie(df, names='lift')
                lift_fig.update_layout(width=400,height=400, showlegend=False)
                lift_fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(lift_fig, config= dict(
                    displayModeBar = False))
                lift_fig2 = px.scatter(df, x='date',y='lift',color='lift', symbol='lift')
                lift_fig2.update_layout(hovermode='x unified',width=400, height=400, showlegend=False,yaxis_visible=False, yaxis_showticklabels=False,xaxis_visible=False, xaxis_showticklabels=False)
                lift_fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
                st.plotly_chart(lift_fig2, config= dict(
                    displayModeBar = False))

    

        except:
            pass
        try:
            with col1:
                df['reps'] = df['sets'].astype(int)
                print('line 147')
                df['weight'] = df['weight'].astype(float)
                prog_df = df[df['reps'] < 4]
                colored_header("Progress")
                prog_fig1 = 0
                prog_df['sequence'] = prog_df.index
                prog_df["Work Out"] = prog_df.groupby("lift")['sequence'].apply(lambda x: x.groupby(x).ngroup() + 1)
                prog_fig1 = px.bar(prog_df, x="Work Out", y = 'weight',color='lift', facet_row='lift', height = 450,width=490,hover_data=["reps", "date"])
                prog_fig1.update_layout(showlegend=False,hovermode='x')
                prog_fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
                st.plotly_chart(prog_fig1, config= dict(
                        displayModeBar = False))
                #st.dataframe(df.style.highlight_max(axis=0))
            with col2:
                colored_header("Data")
                st.dataframe(df.drop(['sets'],axis=1).style.background_gradient(), height=410, width=600)
        except:
            st.info("Enter your first workout")
    with TABLES:
        try:
            d = df
            d =d[d['sets']!='sets']
            d['sets'] = d['sets'].astype(int)
            maxes = d[d['sets']==1]
            for ls in maxes['lift'].unique():
                print(ls)
                maxes1 = maxes[maxes['lift'] == ls]
                print(maxes1)
                lastsq = int(maxes1['weight'].iloc[0])
                recentsq = int(maxes1['weight'].max())
                difsq = recentsq - lastsq
                st.sidebar.metric(label=ls,value = recentsq, delta=difsq)
                
        except:
            pass

        colored_header("Percentage Table")
        maxtable = pd.DataFrame()
        maxtable['Lifts'] = df['lift'].unique()
        st.dataframe(maxtable)
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
        for lft in df['lift'].unique():
            print(lft)
            liftdf = df[df['lift'] == lft]
            print(liftdf)
            #liftdf['weight'] = liftdf['weight'].astype(float)

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
        st.dataframe(maxtable.style.background_gradient())

                
        try:
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
                    fig.update_layout(width=500,height=300,yaxis_title="1 Rep Weight Predictions", hovermode='y unified')
                    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
                    colored_header('1 Rep Max Projections: ' + lts)
                    a1, a2 = st.columns(2)
                    with a1:
                        st.plotly_chart(fig, config= dict(
                    displayModeBar = False))
                    with a2:
                        predictions = predictions.set_index('1 Rep Max Attempt')
                        predictions['past weight increase'] = predictions['past weight'].diff()
                        predictions['predicted increase per attempt'] = predictions['predictions'].diff()
                        st.text("Metrics")
                        st.error("Average Increase Per Max Attempt: " + str(round(predictions['past weight increase'].mean(),2)) + " lbs")
                        st.info("Projected Increase Next Attempt: " + str(round(predictions['predicted increase per attempt'].mean(),2)) + " lbs")
                        if predictions['predicted increase per attempt'].mean() < predictions['past weight increase'].mean():
                                                                                        st.warning("Push hard to incrase by more weight")
                        else:
                            st.success("You are projected to outpace your previous max increases")
                        #st.dataframe(predictions.drop(['weight', 'Label', 'Work Outs'], axis=1).style.background_gradient(), width=700)
        except:
            pass
    
        


    with ABOUT:
        st.subheader("CrossData 🏋️‍")
        st.text("CrossData is a simple tool to log CrossFit data")
        st.text("For questions or comments, please contact Cole Hagen @ hagencolej@gmail.com")
        


if __name__ == '__main__':
    st.sidebar.title('CrossData 🏋️‍')
    main()
