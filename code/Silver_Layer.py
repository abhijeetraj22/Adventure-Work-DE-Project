# Databricks notebook source
from pyspark.sql.functions import * 
from pyspark.sql.types import *
from pyspark.sql.functions import to_timestamp


# COMMAND ----------

# MAGIC %md
# MAGIC # Silver Layers Script

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Access using App

# COMMAND ----------



spark.conf.set("fs.azure.account.auth.type.datastorageproject22.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.datastorageproject22.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.datastorageproject22.dfs.core.windows.net", "d95b3862-c14f-459a-b273-83ad618b41a4")
spark.conf.set("fs.azure.account.oauth2.client.secret.datastorageproject22.dfs.core.windows.net", "smZ8Q~o.lQ9tt7eTPbjbbFxuF1J9ON_sC8xe8cKZ")
spark.conf.set("fs.azure.account.oauth2.client.endpoint.datastorageproject22.dfs.core.windows.net", "https://login.microsoftonline.com/22b63c14-a46a-4143-89f4-29b7af2583b4/oauth2/token")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Loading

# COMMAND ----------

# MAGIC %md
# MAGIC #### Reading Data

# COMMAND ----------

df_cal = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Calendar")
df_cus = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Customers")
df_procat = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Product_Categories")
df_pro = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Products")
df_ret = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Returns")
df_sales = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Sales*")
df_ter = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Territories")
df_subcat = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/Product_Subcategories")
                                                            

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformations

# COMMAND ----------

# MAGIC %md
# MAGIC #### Calender

# COMMAND ----------

df_cal.display()

# COMMAND ----------

df_cal = df.withColumn('Month',month(col('Date'))).withColumn('Year',year(col('Date')))
df_cal.display()

# COMMAND ----------

df_cal.write.format('parquet').mode('append').option("path","abfss://silver@datastorageproject22.dfs.core.windows.net/AdventureWorks_Calendar").save()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Customer

# COMMAND ----------

df_cus.display()

# COMMAND ----------

df_cus.withColumn("fullName",concat(col('Prefix'),lit(' '),col('FirstName'),lit(' '),col('LastName'))).display()

# COMMAND ----------

df_cus = df_cus.withColumn('fullName',concat_ws(' ',col('Prefix'),col('FirstName'),col('lastName')))

# COMMAND ----------

df_cus.display()

# COMMAND ----------

df_cus.write.format('parquet').mode('append').option("path","abfss://silver@datastorageproject22.dfs.core.windows.net/AdventureWorks_Customers").save()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Sub Categories

# COMMAND ----------

df_subcat.display()

# COMMAND ----------

df_subcat.write.format('parquet').mode('append').option("path","abfss://silver@datastorageproject22.dfs.core.windows.net/Product_Subcategories").save()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Product

# COMMAND ----------

df_pro.display()

# COMMAND ----------

df_pro = df_pro.withColumn('ProductSKU',split(col('ProductSKU'),'-')[0]).withColumn('ProductName',split(col('ProductName'),' ')[0])

# COMMAND ----------

df_pro.display()

# COMMAND ----------

df_pro.write.format('parquet').mode('append').option("path","abfss://silver@datastorageproject22.dfs.core.windows.net/AdventureWorks_Products").save()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Returns

# COMMAND ----------

df_ret.display()

# COMMAND ----------

df_ret.write.format('parquet').mode('append').option("path","abfss://silver@datastorageproject22.dfs.core.windows.net/AdventureWorks_Returns").save()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Territories

# COMMAND ----------

df_ter.display()

# COMMAND ----------

df_ter.write.format('parquet').mode('append').option("path","abfss://silver@datastorageproject22.dfs.core.windows.net/AdventureWorks_Territories").save()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Sales

# COMMAND ----------

df_sales.display()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Change the Date Format

# COMMAND ----------

df_sales = spark.read.format("csv").option("header", "true").load("abfss://bronze@datastorageproject22.dfs.core.windows.net/AdventureWorks_Sales*")

# COMMAND ----------

from pyspark.sql.functions import col, trim, to_date, date_format
# Clean, parse, and format StockDate
df_sales = df_sales.withColumn("StockDate_Clean",trim(col("StockDate"))).withColumn("ParsedStockDate",to_date("StockDate_Clean", "M/d/yyyy")).withColumn("StockDate",
date_format("ParsedStockDate", "yyyy-MM-dd")).drop("StockDate_Clean", "ParsedStockDate")

# Clean, parse, and format OrderDate
df_sales = df_sales.withColumn("OrderDate_Clean",trim(col("OrderDate"))).withColumn("ParsedOrderDate",to_date("OrderDate_Clean", "M/d/yyyy")).withColumn("OrderDate",
date_format("ParsedOrderDate", "yyyy-MM-dd")).drop("OrderDate_Clean", "ParsedOrderDate")

# Show the cleaned columns
df_sales.select("StockDate", "OrderDate").show(truncate=False)


# COMMAND ----------

# Convert to date format
df_sales = df_sales.withColumn('StockDate',to_timestamp('StockDate'))
df_sales.display()

# COMMAND ----------

df_sales = df_sales.withColumn('OrderNumber',regexp_replace(col('OrderNumber'),'S','T'))

# COMMAND ----------

df_sales = df_sales.withColumn('multiply',col('OrderLineItem')*col('OrderQuantity'))

# COMMAND ----------

df_sales.display()

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC #### Sales Analysis

# COMMAND ----------

df_sales.groupBy('OrderDate').agg(count('OrderNumber').alias('total_order')).display()

# COMMAND ----------

df_procat.display()

# COMMAND ----------

df_ter.display()

# COMMAND ----------

df_sales.write.format('parquet').mode('append').option("path","abfss://silver@datastorageproject22.dfs.core.windows.net/AdventureWorks_Sales").save()