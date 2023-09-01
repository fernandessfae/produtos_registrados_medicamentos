import pandas as pd
import matplotlib.pyplot as plt
from numpy import arange


def verify_column_in_dataframe(data: pd.DataFrame, column_name: str) -> bool:
    dataframe_columns: list[str] = list(data.columns)
    if column_name in dataframe_columns:
        return True
    print(f'Column: {column_name} not in a dataframe')
    return False


def convert_uppercase_columns(data: pd.DataFrame, *args: str) -> pd.DataFrame:
    for column_name in args:
        if verify_column_in_dataframe(data, column_name):
            data[column_name] = data[column_name].str.upper()
    return data


def bar_graph(data: pd.DataFrame, column: str,
              qt_bar: int, title: str) -> None:
    """Function for generating bar graphs according to the column
       desired, using the count of each value in the column.

       :param data: Data to be used to generate the graph
       :datatype: pd.DataFrame
       :param column: Column name to count its values
       :tyoe column: str
       :param qt_bar: Number of bars to be displayed on the chart
       :type qt_bar: str
       :param title: Bar chart title name
       :type title: str
    """
    plt.figure(figsize=(15, 5))
    if qt_bar >= 10:
        data.value_counts(column)[:qt_bar].sort_values().plot(
            kind='barh', color=plt.cm.Set1(arange(qt_bar-1, -1, -1)))
        plt.xticks(fontsize=15, rotation=0)
        plt.xlabel('Quantidade', fontdict={'fontsize': 15})
        plt.ylabel('', fontdict={'fontsize': 15})
        plt.yticks(rotation=20, fontsize=15)
    else:
        data.value_counts(column)[:qt_bar].plot(
            kind='bar', color=plt.cm.Set2(arange(qt_bar)))
        plt.xticks(rotation=20, fontsize=15)
        plt.xlabel('', fontdict={'fontsize': 15})
        plt.ylabel('Quantidade', fontdict={'fontsize': 15})
        plt.yticks(fontsize=15)
    plt.title(title, fontdict={'fontsize': 20, 'fontweight': 'bold'})
    plt.show()
    return None


df: pd.DataFrame = pd.read_csv(
    'DADOS_ABERTOS_MEDICAMENTOS.csv',
    encoding='latin-1',
    sep=';',
    usecols=['NOME_PRODUTO', 'CATEGORIA_REGULATORIA',
             'CLASSE_TERAPEUTICA', 'EMPRESA_DETENTORA_REGISTRO',
             'SITUACAO_REGISTRO', 'PRINCIPIO_ATIVO'])

df = convert_uppercase_columns(df, 'NOME_PRODUTO',
                               'CATEGORIA_REGULATORIA', 'CLASSE_TERAPEUTICA',
                               'SITUACAO_REGISTRO', 'PRINCIPIO_ATIVO')

df['EMPRESA_DETENTORA_REGISTRO'] = df['EMPRESA_DETENTORA_REGISTRO'].str[17:]

bar_graph(df, 'NOME_PRODUTO',
          10, '10 maiores quantidade de medicamentos registrados na ANVISA')

bar_graph(df, 'CATEGORIA_REGULATORIA',
          9, 'Categorias regulatórias para registro de medicamentos na ANVISA')

bar_graph(
    df,
    'CLASSE_TERAPEUTICA',
    10,
    '10 maiores classes terapêuticas para registro de medicamentos na ANVISA')

bar_graph(
    df,
    'PRINCIPIO_ATIVO',
    10,
    '10 maiores principios ativos presentes nos medicamentos registrados na ANVISA')

bar_graph(
    df,
    'EMPRESA_DETENTORA_REGISTRO',
    10,
    '10 maiores empresas detentoras de registros de medicamentos na ANVISA')
