# Desigualdades de Markov, Chebyshev y Chernoff

Proyecto de la materia **Probabilidad** de la Maestría en Ciencia de Datos. El objetivo es estudiar desigualdades probabilísticas que permiten acotar eventos extremos sin calcular necesariamente toda la distribución.

El desarrollo combina demostraciones matemáticas con experimentos reproducibles en Python para comparar probabilidades exactas y cotas superiores.

## Objetivos

- Demostrar la desigualdad de Markov.
- Deducir la desigualdad de Chebyshev a partir de Markov.
- Obtener la cota de Chernoff mediante funciones generadoras de momentos.
- Calcular las funciones generadoras de momentos de las distribuciones Poisson y exponencial.
- Comparar las probabilidades exactas con las cotas de Markov, Chebyshev y Chernoff.
- Analizar cuándo cada cota resulta informativa.

## Distribuciones estudiadas

### Poisson

Para una variable aleatoria

$$
X\sim\operatorname{Poisson}(\lambda),
$$

se utilizan

$$
\mathbb E[X]=\lambda,
\qquad
\operatorname{Var}(X)=\lambda,
$$

y la función generadora de momentos

$$
M_X(\theta)=\exp\{\lambda(e^\theta-1)\}.
$$

Como Poisson es una distribución discreta, los eventos de cola se calculan para umbrales enteros. En SciPy,

```python
poisson.sf(k - 1, mu=lam)
```

representa $\mathbb P(X\ge k)$.

### Exponencial

Se emplea la parametrización por **tasa**:

$$
Y\sim\operatorname{Exp}(\lambda),
$$

con

$$
\mathbb E[Y]=\frac{1}{\lambda},
\qquad
\operatorname{Var}(Y)=\frac{1}{\lambda^2},
$$

y

$$
M_Y(\theta)=\frac{\lambda}{\lambda-\theta},
\qquad \theta<\lambda.
$$

SciPy parametriza la exponencial mediante la escala, por lo que debe utilizarse `scale=1/lam`.

## Estructura del proyecto

```text
Desigualdades/
├── funciones/
│   ├── __init__.py
│   ├── cotas.py
│   └── visualizacion.py
├── notebooks/
│   └── desigualdades.ipynb
├── figures/
│   ├── comparacion_poisson.svg
│   └── comparacion_exponencial.svg
├── presentacion/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── Desigualdade.png
├── instrucciones.png
├── requirements.txt
└── README.md
```

- `notebooks/desigualdades.ipynb`: demostraciones, experimentos, tablas, gráficas y conclusiones.
- `funciones/cotas.py`: implementación de las cotas y construcción de tablas comparativas.
- `funciones/visualizacion.py`: gráfica de probabilidades exactas y cotas.
- `figures/`: imágenes PNG y SVG exportadas automáticamente por el notebook.
- `presentacion/`: presentación web con navegación mediante botones o teclado.
- `requirements.txt`: dependencias y versiones instaladas en el ambiente de desarrollo.
- `presentacion/`: materiales para la exposición del proyecto.

## Requisitos

- Python 3.11 o posterior.
- NumPy.
- SciPy.
- pandas.
- Matplotlib.
- seaborn.
- JupyterLab.
- ipykernel.

## Instalación

Desde PowerShell, en la raíz del proyecto, crear un ambiente virtual:

```powershell
python -m venv .venv
```

Activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, habilitarla solamente durante la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Actualizar las herramientas de instalación e instalar las dependencias principales:

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install numpy scipy pandas matplotlib seaborn jupyterlab ipykernel
```

También es posible reproducir las versiones registradas en el proyecto:

```powershell
python -m pip install -r requirements.txt
```

Registrar el ambiente como kernel de Jupyter:

```powershell
python -m ipykernel install --user --name desigualdades --display-name "Python (Desigualdades)"
```

## Ejecución

Con el ambiente virtual activo, iniciar JupyterLab:

```powershell
jupyter lab
```

Abrir `notebooks/desigualdades.ipynb` y seleccionar el kernel **Python (Desigualdades)**. Después, ejecutar todas las celdas en orden.

Al ejecutar las celdas de visualización se crean las figuras utilizadas por la presentación. Para exponer el proyecto, abrir `presentacion/index.html` en un navegador. Las flechas izquierda y derecha cambian de diapositiva y la tecla `F` activa la pantalla completa.

Para comprobar las dependencias desde la terminal:

```powershell
python -c "import numpy, scipy, pandas, matplotlib, seaborn; print('Dependencias correctas')"
```

## Metodología computacional

Para cada distribución se seleccionan parámetros $\lambda$ y umbrales superiores a la esperanza. El notebook calcula:

1. La probabilidad de cola exacta.
2. La cota de Markov.
3. La cota obtenida mediante Chebyshev.
4. La cota optimizada de Chernoff.

Los resultados se presentan en tablas y gráficas con escala vertical logarítmica. Las fórmulas originales se conservan en las tablas. Para las gráficas se utiliza

$$
\min(1,\text{cota}),
$$

porque una cota mayor que uno es matemáticamente válida, pero no aporta información adicional sobre una probabilidad.

## Resultados esperados

- Markov es la desigualdad más general y normalmente produce la cota más holgada.
- Chebyshev incorpora la varianza, aunque puede ser poco informativa cerca de la media.
- Chernoff utiliza la función generadora de momentos y suele describir mejor el decaimiento de las colas.
- Todas las cotas calculadas deben ser mayores o iguales que la probabilidad exacta correspondiente.

El notebook incluye una comprobación automática de esta última propiedad.

## Referencias

- Ross, S. M. (2014). *A First Course in Probability* (9th ed.). Pearson.
- Mitzenmacher, M., & Upfal, E. (2017). *Probability and Computing* (2nd ed.). Cambridge University Press.
- SciPy Community. Documentación de [`scipy.stats.poisson`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html) y [`scipy.stats.expon`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html).
