from src.belly import Belly

def before_scenario(context, scenario):
    context.belly = Belly()
