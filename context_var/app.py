from contextvars import ContextVar

## Create a new ContextVar with a name and optional default value
var: ContextVar[int] = ContextVar('var', default=42)

## Set a new value for the context variable in the current context
token = var.set('new value')
token = var.set('new value 1')

## Get the value for the context variable in the current context
print(var.get())  # Outputs: new value

## Reset the context variable to its previous value
var.reset(token)

## Now the variable has no value again, so var.get() would raise a LookupError
try:
    print(var.get())
except LookupError:
    print("Variable has no value")  # Outputs: Variable has no value
