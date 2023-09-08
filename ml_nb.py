import pandas as pd
from pre_processamento import replace_column_rows_with_nan_values
from pre_processamento import replace_column_values_by_numbers_values
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from yellowbrick.classifier import ConfusionMatrix

df: pd.DataFrame = pd.read_csv(
    'DADOS_ABERTOS_MEDICAMENTOS.csv',
    encoding='latin-1',
    sep=';',
    usecols=['CATEGORIA_REGULATORIA', 'CLASSE_TERAPEUTICA',
             'PRINCIPIO_ATIVO'])

df.dropna(how='any', subset='CATEGORIA_REGULATORIA', inplace=True)
df = replace_column_rows_with_nan_values(
    df, 'DESCONHECIDO', 'CLASSE_TERAPEUTICA', 'PRINCIPIO_ATIVO')
df = replace_column_values_by_numbers_values(
    df, 'CATEGORIA_REGULATORIA', 'CLASSE_TERAPEUTICA', 'PRINCIPIO_ATIVO')

forecasters = df.iloc[:, 1:3].values
class_ = df.iloc[:, 0].values

# Holdout (Train_test_split)
forecasters_training, forecasters_test, class_training, class_test = \
    train_test_split(forecasters, class_, test_size=0.25, random_state=0)

classifier = GaussianNB()
classifier.fit(forecasters_training, class_training)
forecasts = classifier.predict(forecasters_test)

model_precision: float = round(accuracy_score(class_test, forecasts), 2)
confusion_matrix_ = confusion_matrix(class_test, forecasts)

# print(classifier.classes_)
# print(classifier.class_count_)
# print(classifier.class_prior_)

confusion_matrix_image = ConfusionMatrix(
    classifier, encoder={0: 'SIMILAR', 1: 'FITOTERÁPICO',
                         2: 'NOVO', 3: 'BIOLÓGICO',
                         4: 'ESPECÍFICO', 5: 'GENÉRICO',
                         6: 'DINAMIZADO', 7: 'RADIOFÁRMACO',
                         8: 'PRODUTO DE T'})
confusion_matrix_image.fit(forecasters_training, class_training)
confusion_matrix_image.score(forecasters_test, class_test)
confusion_matrix_image.show()

print(classification_report(
    class_test,
    forecasts,
    target_names=['SIMILAR', 'FITOTERÁPICO', 'NOVO', 'BIOLÓGICO', 'ESPECÍFICO',
                  'GENÉRICO', 'DINAMIZADO', 'RADIOFÁRMACO', 'PRODUTO DE T']))
