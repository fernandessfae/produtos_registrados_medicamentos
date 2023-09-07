import pandas as pd
import matplotlib.pyplot as plt
from numpy import arange


def verify_column_in_dataframe(data: pd.DataFrame, column_name: str) -> bool:
    dataframe_columns: list[str] = list(data.columns)
    if column_name in dataframe_columns:
        return True
    print(f'Column: {column_name} not in a dataframe')
    return False


def convert_uppercase_columns(data: pd.DataFrame, column: str) -> pd.DataFrame:
    if verify_column_in_dataframe(data, column):
        data[column] = data[column].str.upper()
        return data


def replace_column_rows_with_nan_values(
        data: pd.DataFrame, value_replace: str, *args: str) -> pd.DataFrame:
    for column_name in args:
        df = convert_uppercase_columns(data, column_name)
        df.fillna(value_replace, axis=1, inplace=True)
    return data


def replace_column_values_by_numbers_values(
        data: pd.DataFrame, *args: str) -> pd.DataFrame:
    for column_name in args:
        if verify_column_in_dataframe(data, column_name):
            column_values_list: list[str] = data[column_name].unique().tolist()
            column_key_value_dict: dict[str, int] = {}
            for i in range(len(column_values_list)):
                column_key_value_dict[column_values_list[i]] = i
            # print(column_key_value_dict)
            data.replace({column_name: column_key_value_dict}, inplace=True)
    return data


if __name__ == '__main__':
    df: pd.DataFrame = pd.read_csv(
        'DADOS_ABERTOS_MEDICAMENTOS.csv',
        encoding='latin-1',
        sep=';',
        usecols=['CATEGORIA_REGULATORIA', 'CLASSE_TERAPEUTICA',
                 'PRINCIPIO_ATIVO'])

    print(df.shape)  # 30725 rows
    print(df.isna().sum())
    print()

    df.dropna(how='any', subset='CATEGORIA_REGULATORIA', inplace=True)
    df = replace_column_rows_with_nan_values(
        df, 'DESCONHECIDO', 'CLASSE_TERAPEUTICA', 'PRINCIPIO_ATIVO')

    print(df.shape)
    print(df.isna().sum())
    print()

    """
    plt.figure(figsize=(15, 5))
    df.value_counts('CATEGORIA_REGULATORIA')[:9].plot(
        kind='bar', color=plt.cm.Set2(arange(9)))
    plt.xticks(rotation=20, fontsize=15)
    plt.xlabel('', fontdict={'fontsize': 15})
    plt.ylabel('Quantidade', fontdict={'fontsize': 15})
    plt.yticks(fontsize=15)
    plt.title('Registros das categorias regulatórias pós processamento',
              fontdict={'fontsize': 20, 'fontweight': 'bold'})
    plt.show()
    """

    df = replace_column_values_by_numbers_values(
        df, 'CATEGORIA_REGULATORIA', 'CLASSE_TERAPEUTICA', 'PRINCIPIO_ATIVO')

    print(df.head())
