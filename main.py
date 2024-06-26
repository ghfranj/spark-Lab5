import findspark
findspark.init('C:\SPARK')
from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from src.preprocess_data import preprocess_data
from src.MySpark import MySpark
# Initialize SparkSession
mySpark = MySpark('config.ini')
spark = mySpark.get_spark_session()
# Read the data
data_path = "E:/Downloads/en.openfoodfacts.org.products.csv/en.openfoodfacts.org.products.csv"

if __name__ == '__main__':
    df = preprocess_data(spark, data_path)

    # Train KMeans model
    kmeans = KMeans().setK(5).setSeed(1)
    model = kmeans.fit(df)

    # Make predictions
    predictions = model.transform(df)
    evaluator = ClusteringEvaluator()

    wssse = evaluator.evaluate(predictions)

    print("Within Set Sum of Squared Errors = " + str(wssse))
    # Show the result
    centers = model.clusterCenters()
    print("Cluster Centers:")
    for center in centers:
        print(center)
    # Stop SparkSession
    spark.stop()
