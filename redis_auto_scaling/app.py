from tasks import add

results = []
for i in range(1, 500):
    result = add.apply_async((i, i), queue="high_priority")
    results.append(result)

print("Waiting for results")

for result in results:
    print(result.get())
