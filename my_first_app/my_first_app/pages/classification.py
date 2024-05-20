import pandas
import numpy
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper
from bokeh.plotting import figure
from bokeh.transform import transform
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from typing import List

from dara.core import Variable, py_component, DerivedVariable
from dara.components import Bokeh, Card, Stack, Text, Card, Slider
from dara.components.plotting.palettes import SequentialDark8

from my_first_app.definitions import data, features, target_names

X_train, X_test, y_train, y_test = train_test_split(
    data[features], data['species'], test_size=0.33, random_state=1
)
tree = DecisionTreeClassifier(max_depth=3, random_state=1)
tree.fit(X_train, y_train)
predictions = tree.predict(X_test)

@py_component
def confusion_matrix_plot(predictions: numpy.array):
    df = pandas.DataFrame(confusion_matrix(y_test, predictions), index=target_names, columns=target_names)
    df.index.name = 'Actual'
    df.columns.name = 'Prediction'
    df = df.stack().rename('value').reset_index()

    mapper = LinearColorMapper(
        palette=SequentialDark8, low=df.value.min(), high=df.value.max()
    )
    p = figure(
        title='Confusion Matrix',
        sizing_mode='stretch_both',
        toolbar_location=None,
        x_axis_label='Predicted',
        y_axis_label='Actual',
        x_axis_location="above",
        x_range=target_names,
        y_range=target_names[::-1]
    )
    p.rect(
        x='Actual',
        y='Prediction',
        width=1,
        height=1,
        source=df,
        line_color=None,
        fill_color=transform('value', mapper),
    )

    color_bar = ColorBar(
        color_mapper=mapper,
        location=(0, 0),
        label_standoff=10,
        ticker=BasicTicker(desired_num_ticks=3),
    )
    p.add_layout(color_bar, 'right')

    return Bokeh(p)

def calculate_predictions(n: List[int]):
    tree = DecisionTreeClassifier(max_depth=n[0], random_state=1)
    tree.fit(X_train, y_train)
    predictions = tree.predict(X_test)
    return predictions

max_depth_var = Variable([5])
predictions_var = DerivedVariable(
    calculate_predictions,
    variables=[max_depth_var]
)

def classification_page():
    return Card(
        Stack(
            Text('Max Depth:', width='15%'),
            Slider(domain=[1, 5], value=max_depth_var, step=1, ticks=list(range(1,6))),
            direction='horizontal',
            hug=True,
        ),
        confusion_matrix_plot(predictions_var),
        title='Classification Results'
    )