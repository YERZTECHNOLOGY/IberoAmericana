import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

data = {
    'Estacion Origen': [
        'EstacionA', 'EstacionB', 'EstacionC', 'EstacionD', 'EstacionE',
        'EstacionA', 'EstacionB', 'EstacionC', 'EstacionD', 'EstacionE',
        'EstacionF', 'EstacionG', 'EstacionH', 'EstacionA', 'EstacionB',
        'EstacionC', 'EstacionD', 'EstacionE', 'EstacionF', 'EstacionG'
    ],
    'Estacion Destino': [
        'EstacionB', 'EstacionC', 'EstacionD', 'EstacionE', 'EstacionF',
        'EstacionC', 'EstacionD', 'EstacionE', 'EstacionF', 'EstacionG',
        'EstacionA', 'EstacionB', 'EstacionC', 'EstacionD', 'EstacionE',
        'EstacionF', 'EstacionG', 'EstacionA', 'EstacionB', 'EstacionC'
    ],
    'Tiempo Recorrido': [
        10, 15, 20, 10, 5,
        14, 22, 17, 9, 13,
        11, 16, 18, 12, 20,
        8, 19, 15, 7, 6
    ],
    'Tiempo Estimado': [
        12, 18, 25, 15, 8,
        16, 24, 20, 12, 15,
        13, 17, 21, 14, 22,
        10, 20, 16, 9, 7
    ],
    'Costo': [
        5, 8, 12, 6, 3,
        7, 13, 10, 4, 6,
        5, 9, 11, 6, 10,
        4, 11, 7, 3, 2
    ]
}

df = pd.DataFrame(data)

df_encoded = pd.get_dummies(df, columns=['Estacion Origen', 'Estacion Destino'])

X = df_encoded.drop('Costo', axis=1)
y = df_encoded['Costo']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("Error Cuadrático Medio (MSE):", mse)

plt.scatter(y_test, y_pred)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel('Costo Real')
plt.ylabel('Costo Predicho')
plt.title('Comparación de Costos Reales vs Predichos')
plt.grid(True)
plt.show()
