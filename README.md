# Machine_Learning_Engineering

Project gives an opportunity to training two models (one simple, another one more complex). Environment of working is online store. Models are being trained in order to give predictions about users sessions in online store. Next, trained models have to predict if active session of user will finished with buying event. 

## Predictions serving:

```bash
python3 microservice.py --mode <mode>
```
### mode:
* basic - usage of basic model
* complex - usage of complex model
* ab - A/B experiment with usage of both models execution

## Model training:

```bash 
python3 model_training.py
```
