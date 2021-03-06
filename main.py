import streamlit as st
import data
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression


st.set_page_config(
    # page_title="PE Score Analysis App",
    # page_icon="ð§",
    layout="wide",
    # initial_sidebar_state="collapsed",
    initial_sidebar_state="expanded",
    )

names = ['å­¦å¹´','æ§å¥','èº«é·','ä½é','åº§é«','æ¡å',
'ä¸ä½èµ·ãã','é·åº§ä½åå±','åå¾©æ¨ªè·³ã³','ã·ã£ãã«ã©ã³','50ï½èµ°','ç«ã¡å¹è·³ã³','ãã³ããã¼ã«æã',
'æ¡åå¾ç¹','ä¸ä½èµ·ããå¾ç¹','é·åº§ä½åå±å¾ç¹','åå¾©æ¨ªè·³ã³å¾ç¹','ã·ã£ãã«ã©ã³å¾ç¹','50ï½èµ°å¾ç¹',
'ç«ã¡å¹è·³ã³å¾ç¹','ãã³ããã¼ã«æãå¾ç¹']

DATA_SOURCE = './data/score_0nan.csv'

@st.cache
def load_full_data():
    data = pd.read_csv(DATA_SOURCE)
    # data['date'] = pd.to_datetime(data['date'])
    # data['Size'] = data['size'].apply(lambda x: f'{x:.0f} sqm')
    # data['Price'] = data['price'].apply(lambda x: f'CHF {x:.0f}')
    return data

@st.cache 
def load_num_data():
    data = pd.read_csv(DATA_SOURCE)
    rows = ['å­¦å¹´', 'æ§å¥']
    data = data.drop(rows, axis=1)
    return data

@st.cache 
def load_filtered_data(data, genre_filter):
    # æ°å¤ã§ãã£ã«ã¿ã¼(ä½ç¹ä»¥ä¸)
    # filtered_data = data[data['num_rooms'].between(rooms_filter[0], rooms_filter[1])]
    grade_filter = []
    gender_filter = []
    for elem in genre_filter:
        grade_filter.append(str(elem[0:2]))
        gender_filter.append(str(elem[2]))

    filtered_data = data[data['å­¦å¹´'].isin(grade_filter)]
    filtered_data = filtered_data[filtered_data['æ§å¥'].isin(gender_filter)]

    return filtered_data
    


def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'vis'

    print(st.session_state.page)

    st.sidebar.markdown('## ãã¼ã¸åãæ¿ã')
    # --- pageé¸æã©ã¸ãªãã¿ã³
    page = st.sidebar.radio('ãã¼ã¸é¸æ', ('ãã¼ã¿å¯è¦å', 'ãã¼ã¿ç¢ºèª', 'ååå¸°åæ'))

    # --- pageæ¯ãåã
    if page == 'ãã¼ã¿å¯è¦å':
        st.session_state.page = 'vis'
        vis2()
    elif page == 'ãã¼ã¿ç¢ºèª':
        st.session_state.page = 'table'
        table()
    elif page == 'ååå¸°åæ':
        st.session_state.page = 'lr'
        lr()


# ---------------- ã°ã©ãã§å¯è¦å ----------------------------------
def vis():
    st.title("ä½åæ¸¬å® ãã¼ã¿")

    # score = data.get_num_data()
    # full_data = data.get_full_data()
    score = load_num_data()
    full_data = load_full_data()

    # è²åããªãã·ã§ã³
    coloring = st.radio(
        "ã°ã©ãã®è²åã",
        ('ãªã', 'å­¦å¹´', 'æ§å¥')
    )

    left, right = st.beta_columns(2)

    with left: # æ£å¸å³ã®è¡¨ç¤º 
        label = score.columns
        x_label = st.selectbox('æ¨ªè»¸ãé¸æ',label)
        y_label = st.selectbox('ç¸¦è»¸ãé¸æ',label)


        if coloring == 'å­¦å¹´':
            fig = px.scatter(
            full_data,
            x=x_label,
            y=y_label,
            color="å­¦å¹´"
            )   
        
        elif coloring == "æ§å¥":
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                color="æ§å¥",
                )
            
        else:
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                )
        st.plotly_chart(fig, use_container_width=True)

        cor = data.get_corrcoef(score, x_label, y_label)
        st.write('ç¸é¢ä¿æ°ï¼' + str(cor))

        

    with right: # ãã¹ãã°ã©ã ã®è¡¨ç¤º
        hist_val = st.selectbox('å¤æ°ãé¸æ',label)
        fig = px.histogram(score, x=hist_val)
        st.plotly_chart(fig, use_container_width=True)

    # ç®±ã²ãå³ã®è¡¨ç¤º
    df = load_full_data()
    box_val_y = st.selectbox('ç®±ã²ãå³ã«ããå¤æ°ãé¸æ',label)
    box_val_x = st.selectbox('åé¡ããå¤æ°ãé¸æ',['å­¦å¹´','æ§å¥'])
    fig = px.box(df, x=box_val_x, y=box_val_y)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ã°ã©ãã§å¯è¦åâ¡ :  åã°ã©ããé¸æãã ----------------------------------
def vis2():
    st.title("ä½åæ¸¬å® ãã¼ã¿")

    score = load_num_data()
    full_data = load_full_data()
    label = score.columns

    st.sidebar.markdown('## ããããªã°ã©ããè©¦ãã¦ã¿ãã')

    # sidebar ã§ã°ã©ããé¸æ
    graph = st.sidebar.radio(
        'ã°ã©ãã®ç¨®é¡',
        ('æ£å¸å³', 'ãã¹ãã°ã©ã ', 'ç®±ã²ãå³')
    )

    if  graph  == 'æ£å¸å³':
        left, right = st.beta_columns(2)

        with left: # æ£å¸å³ã®è¡¨ç¤º 
            x_label = st.selectbox('æ¨ªè»¸ãé¸æ',label)
            y_label = st.selectbox('ç¸¦è»¸ãé¸æ',label)

        with right:
            # è²åããªãã·ã§ã³
            coloring = st.radio(
                "ã°ã©ãã®è²åã",
                ('ãªã', 'å­¦å¹´', 'æ§å¥')
            )

        if coloring == 'å­¦å¹´':
            fig = px.scatter(
            full_data,
            x=x_label,
            y=y_label,
            color="å­¦å¹´"
            )   
        
        elif coloring == "æ§å¥":
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                color="æ§å¥",
                )
            
        else:
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                )
        st.plotly_chart(fig, use_container_width=True)

        cor = data.get_corrcoef(score, x_label, y_label)
        st.write('ç¸é¢ä¿æ°ï¼' + str(cor))

    # ãã¹ãã°ã©ã 
    elif graph == "ãã¹ãã°ã©ã ":
        hist_val = st.selectbox('å¤æ°ãé¸æ',label)
        fig = px.histogram(score, x=hist_val)
        st.plotly_chart(fig, use_container_width=True)
    
    # ç®±ã²ãå³
    elif graph == 'ç®±ã²ãå³':
        box_val_y = st.selectbox('ç®±ã²ãå³ã«ããå¤æ°ãé¸æ',label)

        left, right = st.beta_columns(2)
        with left: # æ£å¸å³ã®è¡¨ç¤º 
            fig = px.box(full_data, x='å­¦å¹´', y=box_val_y, )
            st.plotly_chart(fig, use_container_width=True)
        with right:
            fig = px.box(full_data, x='æ§å¥', y=box_val_y)
            st.plotly_chart(fig, use_container_width=True)
        


# ---------------- ãã¼ã¿è¡¨ç¤º ----------------------------------
def sub_table():
    if not 'table_df' in st.session_state:
        st.session_state.table_df = load_full_data()


    # data_load_state = st.text('Loading data...')
    # data = load_data() ã§ã¼ãåãè¾¼ã
    # data_load_state.text("")
    tmp = st.session_state.table_df
    st.title('ãã¼ã¿ã®çµ±è¨æå ±ãç¢ºèªããã')
    st.dataframe(tmp.style.highlight_max(axis=0))

    # ãµã¤ããã¼
    st.sidebar.write('å±æ§ãã¨ã«è¡¨ç¤ºãã')
    genre = st.sidebar.multiselect(
        'ï¼æ°ã«ãªãå±æ§ãé¸æããã',
        ['é«1å¥³å­', 'é«2å¥³å­', 'é«3å¥³å­', 'é«1ç·å­', 'é«2ç·å­', 'é«3ç·å­']
    )

    st.session_state.table_df = data.pick_up_df(tmp, genre)

def table():
    st.title('ãã¼ã¿ã®çµ±è¨æå ±ãç¢ºèªããã')
    
    data_load_state = st.text('Loading data...')
    data = load_full_data()
    data_load_state.text("")

    st.subheader('Choose filters')

    genre_options = ['é«1å¥³å­', 'é«2å¥³å­', 'é«3å¥³å­', 'é«1ç·å­', 'é«2ç·å­', 'é«3ç·å­']
    genre_filter = st.multiselect('Genre',genre_options, default=['é«1å¥³å­', 'é«2å¥³å­', 'é«3å¥³å­', 'é«1ç·å­', 'é«2ç·å­', 'é«3ç·å­'])

    filtered_data = load_filtered_data(data, genre_filter)
    st.dataframe(filtered_data.style.highlight_max(axis=0))
    avg = filtered_data['ç«ã¡å¹è·³ã³'].mean()
    med = filtered_data['ç«ã¡å¹è·³ã³'].median()
    mn = filtered_data['ç«ã¡å¹è·³ã³'].min()
    mx = filtered_data['ç«ã¡å¹è·³ã³'].max()

    st.markdown("### ãç«ã¡å¹è·³ã³ã çµ±è¨æå ±")
    st.markdown(f"- å¹³åå¤ {avg:.0f}")
    st.markdown(f"- ä¸­å¤®å¤ {med:.0f}")
    st.markdown(f"- æå°å¤ {mn:.0f}")
    st.markdown(f"- æå¤§å¤ {mx:.0f}")


# ---------------- ååå¸°åæ ----------------------------------
def  lr():
    st.title('ååå¸°åæãä½¿ã£ã¦äºæ¸¬ãã¦ã¿ããï¼')

    df = load_num_data()
    label = df.columns

    # å¤æ°ãåå¾ãã¦ãããååå¸°ããã
    with st.form('get_lr_data'):
        y_label = st.selectbox('äºæ¸¬ãããå¤æ°(ç®çå¤æ°)', label)
        x_label = st.selectbox('äºæ¸¬ã«ä½¿ãããå¤æ°(èª¬æå¤æ°)', label)
        
        
        y = df[[y_label]]
        X = df[[x_label]]
        submitted = st.form_submit_button("åæã¹ã¿ã¼ã")
        
        if not 'vis_check' in st.session_state:
            st.session_state.vis_check = False
        
        if submitted:
            # ã¢ãã«ã®æ§ç¯
            model_lr = LinearRegression()
            model_lr.fit(X, y)

            # çµæã®åºå
            # st.write('ã¢ãã«é¢æ°ã®åå¸°å¤æ° w1: %.3f' %model_lr.coef_)
            # st.write('ã¢ãã«é¢æ°ã®åç w2: %.3f' %model_lr.intercept_)
            st.write('y= %.3fx + %.3f' % (model_lr.coef_ , model_lr.intercept_))
            st.write('æ±ºå®ä¿æ° R^2ï¼ ', model_lr.score(X, y))

            # ã°ã©ãè¡¨ç¤ºãããå¦ã
            vis_check = st.checkbox("ã°ã©ãã§ç¢ºèªãã", value=False)
            # checkã¤ããå¾ã«ãããã¡ã©submitæ¼ãå¿è¦ãã
            if vis_check:
                # st.write('Checked')
                st.session_state.vis_check = True

    # st.session_state
    if st.session_state.vis_check:
        fig = px.scatter(
            x=df[x_label].values, y=df[y_label].values,
            labels={'x':x_label, 'y':y_label},
             trendline='ols',
             trendline_color_override='red')
            # hover_name=df['å­¦å¹´'].values) 
        # fig = px.scatter(
        #     x=df[x_label].values, y=df[y_label].values,
        #     labels={'x':x_label, 'y':y_label},
        #     trendline='ols')
        st.plotly_chart(fig, use_container_width=True)
       
# menu = st.sidebar.selectbox(
#     'ä½ãããï¼',
#     ['ããããé¸ã¼ã','æ£å¸å³ãè¡¨ç¤º']
# )

# é¢¨è¹ã¨ã¶ã
# st.balloons()

# å¾ããããã
# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')


main()