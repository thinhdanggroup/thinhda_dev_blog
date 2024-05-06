from contextvars import ContextVar

# Create a new ContextVar with a name and optional default value
var: ContextVar[int] = ContextVar('var')

# Set a new value for the context variable in the current context
token1 = var.set('new value')
token2 = var.set('new value 1')

# Get the value for the context variable in the current context
print(var.get())  # Outputs: new value 1

# Reset the context variable to its previous value
var.reset(token2)

print(var.get())  # Outputs: new value
var.reset(token1)

# Now the variable has no value again, so var.get() would raise a LookupError
try:
    print(var.get())
except LookupError:
    print("Variable has no value")  # Outputs: Variable has no value