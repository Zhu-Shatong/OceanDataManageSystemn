import streamlit as st
import sys
from my_rsa import *
import xarray as xr
import os
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import io


def generate_plot(ds, date):
    fig, ax = plt.subplots(figsize=[20, 10])
    ds.SSH.plot(ax=ax)
    ax.set_title(f"Sea Surface Height on {date.strftime('%Y-%m-%d')}")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def main():
    # 宽屏显示
    st.set_page_config(layout="wide")

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("ECCO Sea Surface Height Visualization")

    # 获取URL中的查询参数
    query_params = st.query_params
    encrypted_message = query_params.get('encrypted_message', [None])

    if encrypted_message:
        try:
            # 将空格改为加号
            encrypted_message = encrypted_message.replace(" ", "+")
            year = int(decrypt_message(encrypted_message))
        except Exception as e:
            st.error(f"Error decrypting message: {e}")
            return
    else:
        st.error("No encrypted message provided in the URL.")
        return

    # 使用滑动条获取月份和日期
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    date = st.slider("Select Date", start_date, end_date, start_date)

    # 构建文件路径
    file_path = os.path.join("D:\\Desktop\\ECCO\\ECCO_V4r4_PODAAC\\ECCO_L4_SSH_05DEG_DAILY_V4R4",
                             f"SEA_SURFACE_HEIGHT_day_mean_{date.strftime('%Y-%m-%d')}_ECCO_V4r4_latlon_0p50deg.nc")

    if os.path.exists(file_path):
        # 使用xarray打开并可视化文件内容
        try:
            ds = xr.open_dataset(file_path)
            st.write(f"Visualizing data for {date.strftime('%Y-%m-%d')}")
            plot_area = st.empty()
            with plot_area:
                ds.SSH.plot(figsize=[20, 10])
                st.pyplot()
        except Exception as e:
            st.error(f"Error visualizing data: {e}")
    else:
        st.error(f"File for {date.strftime('%Y-%m-%d')} does not exist.")


if __name__ == "__main__":
    main()
