import pandas as pa
import numpy as na
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D

def add_WERs(strExcelFilename, sheetno, WER_a, WER_b, WER_k):
    
    # Excelファイルから指定されたシートのデータを読み込み、WER列を追加する関数。
    
    # :param strExcelFilename: Excelファイルのパス

# # 引数Example
# WER_a = 1
# WER_b = -9
# WER_k = -10
# sheetno = 0

    try:
        dfExcel = pa.read_excel(
            strExcelFilename,
            sheet_name=sheetno,
            header=0
        )
    except ValueError as e:
        print(f"Excel sheet open error: {e}")
        return None

    # 1行目（iloc[0]）の値がNaNでない列を選択：ヘッダ行は数えないというちょっと許しがたい仕様
    # 元のオブジェクトからのビューかオブジェクトのコピーかわからないから明示しないとだめらしい。ひどくない？
    # つまりデフォルトの挙動はなくて文脈でポインタか実体かが決まってるってこと？そうらしい。癖つよ。
    dfTrimmed = dfExcel.loc[:, dfExcel.iloc[0].notna()].copy()

    target_columns = dfTrimmed.columns[dfTrimmed.iloc[0] == "Sim"]

    for column in target_columns:
        # add WER column
        dfTrimmed.loc[2:, f"{column}_ER"] = dfTrimmed.loc[2:, column].astype(float).apply(
            lambda x: ( WER_a + WER_b * ( ( na.exp( WER_k * x / 100 ) - 1 ) / WER_k ) ) * 100  # as x is percentile yield
        )

        # add Error upper column
        dfTrimmed.loc[2:, f"{column}_EU"] = (
            dfTrimmed.loc[2:, column].astype(float) * ( 1 + dfTrimmed.loc[2:, f"{column}_ER"].astype(float) / 100 )
        )
        
        # add Error lower column
        dfTrimmed.loc[2:, f"{column}_EL"] = (
            dfTrimmed.loc[2:, column].astype(float) * ( 1 - dfTrimmed.loc[2:, f"{column}_ER"].astype(float) / 100 )
        )

    # #   Ys, Yeを含む列の取得

    # simulation_columns = dfTrimmed.columns[dfTrimmed.iloc[0] == "Sim"]
    # experiment_columns = dfTrimmed.columns[dfTrimmed.iloc[0] == "Exp"]

    # #   Exp, Sim各列についてループ

    # for column_Ye, column_Ys in zip(experiment_columns, simulation_columns):

    #     #   3行目にラベルをつける
    #     dfTrimmed.at[1, column_Ys] = "Ys, %"
    #     dfTrimmed.at[1, column_Ye] = "Ye, %"
    #     dfTrimmed.at[1, f"{column_Ys}_ER"] = "Erel, %"
    #     dfTrimmed.at[1, f"{column_Ye}_Eabs"] = "Eabs, %"
    #     dfTrimmed.at[1, f"{column_Ye}_WFIn"] = "WFI(n)"

    #     #   各行の値についてループ
    #     for i in range(2, len(dfTrimmed)):

    #         #   値がNaNでない場合、Exp列の値をSim列の値と比較して、WFIを計算する

    #         if not na.isnan(dfTrimmed.at[i, column_Ye]):
    #             #   Eabs, WFI(n)の計算

    #             dfTrimmed.at[i, f"{column_Ye}_Eabs"] = abs(
    #                 dfTrimmed.at[i, column_Ye] - dfTrimmed.at[i, column_Ys]
    #             ) / dfTrimmed.at[i, column_Ys] * 100

    #             dfTrimmed.at[i, f"{column_Ye}_WFIn"] = (
    #                 dfTrimmed.at[i, f"{column_Ye}_Eabs"] / dfTrimmed.at[i, f"{column_Ys}_ER"] 
    #             ) 
    
    return dfTrimmed


def draw_WERcharts(
    dfTrimmed, 
    var_marker_size, 
    var_font_size, 
    var_chart_size_inches_width, 
    flagShowLegend, 
    sim_startcolour, 
    exp_startcolour
):
    
    # Error handling.
    if dfTrimmed is None or dfTrimmed.empty:
        print("Invalid DataFrame provided.")
        return None

    # basic settings

    plt.rcParams['font.family'] = 'Calibri'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    chart_colors = ['limegreen', 'orange', 'darkslateblue', 'magenta', 
                    'forestgreen', 'indianred', 'royalblue', 'purple',
                    'lawngreen', 'crimson', 'dodgerblue', 'deeppink']

    #   プロットのオブジェクトを取得して基本設定
    #   白銀比でプロットを作成

    fig, ax = plt.subplots()
    fig.set_dpi(400)        #default 100dpi
    fig.set_size_inches(1.414*var_chart_size_inches_width,var_chart_size_inches_width)

    #   Time系列の取得

    time_column = dfTrimmed.columns[dfTrimmed.iloc[0].astype(str).str.match(r"^[tT]ime\s*")]

    #このままだとTime系列の型がobjectになってるのでfloatに変換する必要がある
    #   シミュレーションデータ+WERの描画
    #   ソートしようと思ったがあえてしない。ユーザに左から並べさせる。

    simulation_columns = dfTrimmed.columns[dfTrimmed.iloc[0] == "Sim"]
    experiment_columns = dfTrimmed.columns[dfTrimmed.iloc[0] == "Exp"]

    dfDraw = dfTrimmed.drop(index=[0,1])  # drop header rows
    dfDraw[f"{time_column[0]}"] = dfDraw[f"{time_column[0]}"].astype(float)  # convert time column to float


    #   シミュレーションデータの描画

    color_index = sim_startcolour % len(chart_colors)  # ensure color index is within bounds

    for column in simulation_columns:
        dfDraw[f"{column}"] = dfDraw[f"{column}"].astype(float)  # convert simulation column to float
        
        ax.fill_between(                                    #塗りつぶし
                    #time_column,
                    dfDraw[f"{time_column[0]}"],            #X
                    dfDraw[f"{column}_EU"],                 #Y1
                    dfDraw[f"{column}_EL"],                 #Y2
                    color=chart_colors[color_index],
                    alpha=0.2,
                    edgecolor="none"
        )

        dfDraw.plot( ax=ax,
                    x=f"{time_column[0]}",
                    y=f"{column}",
                    grid=True,
                    color=chart_colors[color_index],
                    style="-",
                    alpha=0.7
        )

        color_index += 1
        color_index %= len(chart_colors)  # ensure color index is within bounds

    #   実験データの描画

    color_index = exp_startcolour % len(chart_colors)  # ensure color index is within bounds
    custom_lines = []  # for legend

    for column in experiment_columns:
        dfDraw[f"{column}"] = dfDraw[f"{column}"].astype(float)  # convert experiment column to float
        
        dfDraw.plot( ax=ax,
                    x=f"{time_column[0]}",
                    y=f"{column}",
                    grid=True,
                    color=chart_colors[color_index],
                    marker="o",
                    markersize=var_marker_size,
                    linestyle='None',
                    alpha=1.0
        )

        #   凡例の設定：まったく新しいLine2Dオブジェクトのセットを作ることで好きなように凡例内を変える
        
        custom_lines=custom_lines + [
            Line2D([0], [0], color=chart_colors[color_index], marker='o', markersize=var_marker_size, linestyle='-', label=r"$"+column+r"$")
        ]

        color_index += 1
        color_index %= len(chart_colors)

    #   凡例の表示

    legend=ax.legend(handles=custom_lines, loc='best', ncol=1, fontsize=var_font_size-1)
    f = legend.get_frame()
    f.set_alpha(1)

    ax.get_legend().set_visible(flagShowLegend)
        
    #   目盛線の設定

    for i in ax.spines.values():
        i.set_color('dimgrey')

    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')

    ax.tick_params(axis='both',which='both', colors='gainsboro', labelsize=var_font_size-1)
    ax.grid(color='gainsboro', linestyle='-', linewidth=0.5)


    for l in ax.get_xticklabels():
        l.set_color('dimgrey')

    for l in ax.get_yticklabels():
        l.set_color('dimgrey')

    #  軸の設定

    ax.set_xlabel(r"Time, min", loc='right', color='dimgrey', fontsize=var_font_size, labelpad=2)       #r""はraw literal、エスケープ抑止
    ax.set_ylabel(r"Yield, %", loc="top", color='dimgrey', fontsize=var_font_size, labelpad=2)

    ax.set_xlim(left=0)
    ax.set_ylim((0,105))

    return fig, ax


def calc_WFI(dfTrimmed, WER_a, WER_b, WER_k):
    # Returns a Dataframe object with WFI values.
    # Input a Dataframe processed by add_WERs function.
    # add_WERsにまとめてもいいのだが。

    if dfTrimmed is None or dfTrimmed.empty:
        print("Invalid DataFrame provided.")
        return None
    
    #   Ys, Yeを含む列の取得

    simulation_columns = dfTrimmed.columns[dfTrimmed.iloc[0] == "Sim"]
    experiment_columns = dfTrimmed.columns[dfTrimmed.iloc[0] == "Exp"]

    #   Exp, Sim各列についてループ

    for column_Ye, column_Ys in zip(experiment_columns, simulation_columns):

        #   3行目にラベルをつける
        dfTrimmed.at[1, column_Ys] = "Ys, %"
        dfTrimmed.at[1, column_Ye] = "Ye, %"
        dfTrimmed.at[1, f"{column_Ys}_ER"] = "Erel, %"
        dfTrimmed.at[1, f"{column_Ye}_Eabs"] = "Eabs, %"
        dfTrimmed.at[1, f"{column_Ye}_WFIn"] = "WFI(n)"

        #   各行の値についてループ
        for i in range(2, len(dfTrimmed)):

            #   値がNaNでない場合、Exp列の値をSim列の値と比較して、WFIを計算する

            if not na.isnan(dfTrimmed.at[i, column_Ye]):
                #   Eabs, WFI(n)の計算

                dfTrimmed.at[i, f"{column_Ye}_Eabs"] = abs(
                    dfTrimmed.at[i, column_Ye] - dfTrimmed.at[i, column_Ys]
                ) / dfTrimmed.at[i, column_Ys] * 100

                dfTrimmed.at[i, f"{column_Ye}_WFIn"] = (
                    dfTrimmed.at[i, f"{column_Ye}_Eabs"] / dfTrimmed.at[i, f"{column_Ys}_ER"] 
                ) 

    return dfTrimmed


