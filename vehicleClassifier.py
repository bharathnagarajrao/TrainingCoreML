import turicreate as turi

url = "training/"

data = turi.image_analysis.load_images(url)

data["vehicleType"] = data["path"].apply(lambda path: "Cars" if "LuxuryCars" in path else "Bus")

data.save("vehicleType.sframe")

data.explore()

dataBuffer = turi.SFrame("vehicleType.sframe")

trainingBuffers, testingBuffers = dataBuffer.random_split(0.9)

model = turi.image_classifier.create(
    trainingBuffers,
    target="vehicleType",
    model="squeezenet_v1.1",
    max_iterations=50
)

evaluations = model.evaluate(testingBuffers)
print evaluations["accuracy"]

model.save("vehicleType.model")
model.export_coreml("VehicleClassifier.mlmodel")
