import streamlit as st
from pyproj import Proj, CRS, Transformer
import pandas as pd


outProj = CRS("EPSG:32640")
inProj = CRS("EPSG:4326")
transformer = Transformer.from_crs(inProj, outProj)


@st.cache(allow_output_mutation=True)
def file_upload(sheet_file):
    try:
        if sheet_file.name.endswith("csv") or sheet_file.name.endswith("txt"):

            df = pd.read_csv(sheet_file)
            return df
        elif sheet_file.name.endswith("xlsx"):
            df = pd.read_excel(sheet_file)
            return df

    except Exception as e:
        st.exception(e)


def save_df(df):
    return df.to_csv(
        index=False
    ).encode('utf-8')


st.set_page_config(
    "UTM conversion Oman",
    page_icon="🌍",
    layout="wide",

)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
            content:'Made by Khalil Al Hooti, hooti@squ.edu.om'; 
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 2px;
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.write(
    """<h1 style="color:green;">Read a sheet containing two columns x, y in
     WGS84 spherical coordinates and convert them to projected coordinated of
      Oman (UTM zone 40 North)</h1>""",
    unsafe_allow_html=True
)
sheet_file = st.file_uploader(
    "",
    type=[
        'xlsx',
        'csv',
        'txt'
    ],
    accept_multiple_files=False,
    help="""Read a sheet containing two columns x, y in
     WGS84 spherical coordinates""",
)

if sheet_file:
    df = st.session_state['df'] = file_upload(sheet_file)
    df.dropna(how='all', axis=1, inplace=True)
    df.dropna(how='all', axis=0, inplace=True)

    st.write(
        '<h1 style="color:blue;">Original sheet</h1>',
        unsafe_allow_html=True
    )
    st.dataframe(df)

    longitude = st.selectbox(
        "What is the longitude column",
        df.columns
    )

    latitude = st.selectbox(
        "what is latitude columns",
        df.columns
    )

    df['UTM-X'], df['UTM-Y'] = zip(
        *df.apply(lambda x: transformer.transform(x[latitude], x[longitude]),
                  axis=1))

    st.write(
        '<h1 style="color:blue;">Sheet contains UTM converted</h1>',
        unsafe_allow_html=True
    )

    st.dataframe(df)

    csv = save_df(
        df
    )

    st.download_button(
        label="Download data",
        data=csv,
        file_name="converted_utm.csv",
        mime='text/csv',
    )
