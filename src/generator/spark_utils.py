try:
    from pyspark.sql import SparkSession
except Exception:
    SparkSession = None


def get_spark(app_name: str = "SyntheticDataGen"):
    if SparkSession is None:
        return None
    return SparkSession.builder.appName(app_name).getOrCreate()
