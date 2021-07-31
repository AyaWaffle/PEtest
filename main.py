import streamlit as st
import data
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression


st.set_page_config(
    # page_title="PE Score Analysis App",
    # page_icon="🧊",
    layout="wide",
    # initial_sidebar_state="collapsed",
    initial_sidebar_state="expanded",
    )

names = ['学年','性別','身長','体重','座高','握力',
'上体起こし','長座体前屈','反復横跳び','シャトルラン','50ｍ走','立ち幅跳び','ハンドボール投げ',
'握力得点','上体起こし得点','長座体前屈得点','反復横跳び得点','シャトルラン得点','50ｍ走得点',
'立ち幅跳び得点','ハンドボール投げ得点']

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
    rows = ['学年', '性別']
    data = data.drop(rows, axis=1)
    return data

@st.cache 
def load_filtered_data(data, genre_filter):
    # 数値でフィルター(何点以上)
    # filtered_data = data[data['num_rooms'].between(rooms_filter[0], rooms_filter[1])]
    grade_filter = []
    gender_filter = []
    for elem in genre_filter:
        grade_filter.append(str(elem[0:2]))
        gender_filter.append(str(elem[2]))

    filtered_data = data[data['学年'].isin(grade_filter)]
    filtered_data = filtered_data[filtered_data['性別'].isin(gender_filter)]

    return filtered_data
    


def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'vis'

    print(st.session_state.page)

    st.sidebar.markdown('## ページ切り替え')
    # --- page選択ラジオボタン
    page = st.sidebar.radio('ページ選択', ('データ可視化', 'データ確認', '単回帰分析'))

    # --- page振り分け
    if page == 'データ可視化':
        st.session_state.page = 'vis'
        vis2()
    elif page == 'データ確認':
        st.session_state.page = 'table'
        table()
    elif page == '単回帰分析':
        st.session_state.page = 'lr'
        lr()


# ---------------- グラフで可視化 ----------------------------------
def vis():
    st.title("体力測定 データ")

    # score = data.get_num_data()
    # full_data = data.get_full_data()
    score = load_num_data()
    full_data = load_full_data()

    # 色分けオプション
    coloring = st.radio(
        "グラフの色分け",
        ('なし', '学年', '性別')
    )

    left, right = st.beta_columns(2)

    with left: # 散布図の表示 
        label = score.columns
        x_label = st.selectbox('横軸を選択',label)
        y_label = st.selectbox('縦軸を選択',label)


        if coloring == '学年':
            fig = px.scatter(
            full_data,
            x=x_label,
            y=y_label,
            color="学年"
            )   
        
        elif coloring == "性別":
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                color="性別",
                )
            
        else:
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                )
        st.plotly_chart(fig, use_container_width=True)

        cor = data.get_corrcoef(score, x_label, y_label)
        st.write('相関係数：' + str(cor))

        

    with right: # ヒストグラムの表示
        hist_val = st.selectbox('変数を選択',label)
        fig = px.histogram(score, x=hist_val)
        st.plotly_chart(fig, use_container_width=True)

    # 箱ひげ図の表示
    df = load_full_data()
    box_val_y = st.selectbox('箱ひげ図にする変数を選択',label)
    box_val_x = st.selectbox('分類する変数を選択',['学年','性別'])
    fig = px.box(df, x=box_val_x, y=box_val_y)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- グラフで可視化② :  各グラフを選択する ----------------------------------
def vis2():
    st.title("体力測定 データ")

    score = load_num_data()
    full_data = load_full_data()
    label = score.columns

    st.sidebar.markdown('## いろんなグラフを試してみよう')

    # sidebar でグラフを選択
    graph = st.sidebar.radio(
        'グラフの種類',
        ('散布図', 'ヒストグラム', '箱ひげ図')
    )

    if  graph  == '散布図':
        left, right = st.beta_columns(2)

        with left: # 散布図の表示 
            x_label = st.selectbox('横軸を選択',label)
            y_label = st.selectbox('縦軸を選択',label)

        with right:
            # 色分けオプション
            coloring = st.radio(
                "グラフの色分け",
                ('なし', '学年', '性別')
            )

        if coloring == '学年':
            fig = px.scatter(
            full_data,
            x=x_label,
            y=y_label,
            color="学年"
            )   
        
        elif coloring == "性別":
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                color="性別",
                )
            
        else:
            fig = px.scatter(
                full_data,
                x=x_label,
                y=y_label,
                )
        st.plotly_chart(fig, use_container_width=True)

        cor = data.get_corrcoef(score, x_label, y_label)
        st.write('相関係数：' + str(cor))

    # ヒストグラム
    elif graph == "ヒストグラム":
        hist_val = st.selectbox('変数を選択',label)
        fig = px.histogram(score, x=hist_val)
        st.plotly_chart(fig, use_container_width=True)
    
    # 箱ひげ図
    elif graph == '箱ひげ図':
        box_val_y = st.selectbox('箱ひげ図にする変数を選択',label)

        left, right = st.beta_columns(2)
        with left: # 散布図の表示 
            fig = px.box(full_data, x='学年', y=box_val_y, )
            st.plotly_chart(fig, use_container_width=True)
        with right:
            fig = px.box(full_data, x='性別', y=box_val_y)
            st.plotly_chart(fig, use_container_width=True)
        


# ---------------- データ表示 ----------------------------------
def sub_table():
    if not 'table_df' in st.session_state:
        st.session_state.table_df = load_full_data()


    # data_load_state = st.text('Loading data...')
    # data = load_data() でーた取り込む
    # data_load_state.text("")
    tmp = st.session_state.table_df
    st.title('データの統計情報を確認しよう')
    st.dataframe(tmp.style.highlight_max(axis=0))

    # サイドバー
    st.sidebar.write('属性ごとに表示する')
    genre = st.sidebar.multiselect(
        '＊気になる属性を選択しよう',
        ['高1女子', '高2女子', '高3女子', '高1男子', '高2男子', '高3男子']
    )

    st.session_state.table_df = data.pick_up_df(tmp, genre)

def table():
    st.title('データの統計情報を確認しよう')
    
    data_load_state = st.text('Loading data...')
    data = load_full_data()
    data_load_state.text("")

    st.subheader('Choose filters')

    genre_options = ['高1女子', '高2女子', '高3女子', '高1男子', '高2男子', '高3男子']
    genre_filter = st.multiselect('Genre',genre_options, default=['高1女子', '高2女子', '高3女子', '高1男子', '高2男子', '高3男子'])

    filtered_data = load_filtered_data(data, genre_filter)
    st.dataframe(filtered_data.style.highlight_max(axis=0))
    avg = filtered_data['立ち幅跳び'].mean()
    med = filtered_data['立ち幅跳び'].median()
    mn = filtered_data['立ち幅跳び'].min()
    mx = filtered_data['立ち幅跳び'].max()

    st.markdown("### 「立ち幅跳び」 統計情報")
    st.markdown(f"- 平均値 {avg:.0f}")
    st.markdown(f"- 中央値 {med:.0f}")
    st.markdown(f"- 最小値 {mn:.0f}")
    st.markdown(f"- 最大値 {mx:.0f}")


# ---------------- 単回帰分析 ----------------------------------
def  lr():
    st.title('単回帰分析を使って予測してみよう！')

    df = load_num_data()
    label = df.columns

    # 変数を取得してから、単回帰したい
    with st.form('get_lr_data'):
        y_label = st.selectbox('予測したい変数(目的変数)', label)
        x_label = st.selectbox('予測に使いたい変数(説明変数)', label)
        
        
        y = df[[y_label]]
        X = df[[x_label]]
        submitted = st.form_submit_button("分析スタート")
        
        if not 'vis_check' in st.session_state:
            st.session_state.vis_check = False
        
        if submitted:
            # モデルの構築
            model_lr = LinearRegression()
            model_lr.fit(X, y)

            # 結果の出力
            # st.write('モデル関数の回帰変数 w1: %.3f' %model_lr.coef_)
            # st.write('モデル関数の切片 w2: %.3f' %model_lr.intercept_)
            st.write('y= %.3fx + %.3f' % (model_lr.coef_ , model_lr.intercept_))
            st.write('決定係数 R^2： ', model_lr.score(X, y))

            # グラフ表示するか否か
            vis_check = st.checkbox("グラフで確認する", value=False)
            # checkつけた後にもういちどsubmit押す必要あり
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
            # hover_name=df['学年'].values) 
        # fig = px.scatter(
        #     x=df[x_label].values, y=df[y_label].values,
        #     labels={'x':x_label, 'y':y_label},
        #     trendline='ols')
        st.plotly_chart(fig, use_container_width=True)
       
# menu = st.sidebar.selectbox(
#     '何をする？',
#     ['ここから選ぼう','散布図を表示']
# )

# 風船とぶ、
# st.balloons()

# 待たせられる
# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')


main()