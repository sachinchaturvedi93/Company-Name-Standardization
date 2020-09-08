import streamlit as st
import pandas as pd 
import numpy as np
import base64
from copyright import CopyRight

data = st.file_uploader("Upload a Dataset", type=["csv","txt"])


def main():

    def download_file(df):
        """
        Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(
            csv.encode()
        ).decode()  # some strings <-> bytes conversions necessary here
        return f'<a href="data:file/csv;base64,{b64}" download="copyright.csv">Download csv file</a>'

    if data is not None:
        df = pd.read_csv(data, encoding ='latin')
        st.dataframe(df.head())

        if(st.button("Copyright Names")):
            df2 = CopyRight(df)
            st.dataframe(df2)
            st.markdown(download_file(df2), unsafe_allow_html = True)        

if __name__=='__main__':
    main()
