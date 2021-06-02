from typing import Any
from copy import deepcopy

class Model:

    def __init__(self, name: str, model, freq: str):
        self.name = name
        self.model = model
        self.freq = freq
        self.train = None
        self.test = None
        self.prediction = None
        self.pred_col = "prediction"
        self.y_col = "y"
        self.date_col = "ds"


    def fit(self, train_dataset):

        "Performs model training with standard settings"
        self.train = deepcopy(train_dataset)

        if self.name == "orbit":

            self.model.fit(self.train)

        elif self.name == "nprophet":
            self.model.fit(self.train, validate_each_epoch=True,
                           valid_p=0.2, freq=self.freq,
                           plot_live_loss=True, epochs=10)

    def predict(self, dataset: Any):
        "Performs prediction"

        self.test = deepcopy(dataset)

        if self.name == "orbit":
            prediction = self.model.predict(self.test)
        elif self.name == "nprophet":

            future = self.model.make_future_dataframe(self.train, periods=len(self.test))
            prediction = self.model.predict(future).rename(columns={"yhat1": self.pred_col})

        prediction = prediction[[self.date_col, self.pred_col]]

        self.prediction = prediction

        return self.prediction
