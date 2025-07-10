# 🌐 Adventure Works - Azure Data Engineering Project

An end-to-end data engineering solution built on Azure, implementing the Medallion Architecture and demonstrating a complete pipeline from data ingestion to business intelligence.

> GitHub Repo: [Adventure-Work-DE-Project](https://github.com/abhijeetraj22/Adventure-Work-DE-Project)

---

## 📸 Architecture Overview
<p align="center">
  <img src="https://github.com/username/repo/blob/main/image.png?raw=true" width="300"/>
</p>

<p align="center">
  <img src="Data/Architech.png" alt="Azure Pipeline Architecture" width="600"/>
  <br>
  <b>Figure:</b> Azure Pipeline Architecture
</p>


This architecture follows the **Bronze → Silver → Gold** model and consists of:

1. **Data Source**: Public GitHub repository hosting CSV data (Sales, Customers, Products)
2. **Data Ingestion**: Azure Data Factory (ADF) pulls data using the HTTP connector
3. **Raw Data Store**: Bronze layer in Azure Data Lake Gen2
4. **Transformation**: Azure Databricks (PySpark) performs cleaning and enrichment
5. **Serving**: Transformed Gold data served via Azure Synapse Analytics
6. **Reporting**: Power BI dashboards consuming Synapse views

---

## ⚙️ Tech Stack Used

| Layer            | Azure Service          | Purpose                                     |
|------------------|------------------------|---------------------------------------------|
| Data Ingestion   | **Azure Data Factory** | Ingest CSV files from GitHub (HTTP Source) |
| Raw Storage      | **ADLS Gen2 - Bronze** | Store unprocessed/raw data                  |
| Transformation   | **Azure Databricks**   | Clean, enrich, and join datasets using Spark |
| Processed Storage| **ADLS Gen2 - Silver/Gold** | Hold clean & modeled datasets           |
| Serving Layer    | **Azure Synapse**      | Queryable analytics layer (external tables) |
| Reporting        | **Power BI**           | Dashboards for insights                     |

---

## 📁 Repository Structure

```bash
Adventure-Work-DE-Project/
│
├── README.md                      # This file
│
├───Code/
│   ├───Bronze/                    # ADF configurations for raw layer
│   │   ├───pipeline/              # Pipelines: DynamicGitToRow.json, GitToRow.json
│   │   ├───dataset/               # ADF datasets for source/sink/param
│   │   ├───linkedService/         # ADF linked services: HTTP, ADLS
│   │   ├───factory/               # Factory definition JSON
│   │   ├───Microsoft.DataFactory/ # Template and parameter JSONs for ARM deployment
│   │   └── demo.txt, git.json, publish_config.json
│
│   ├───Silver/                    # Databricks notebooks and templates
│   │   ├── Silver_Layer.ipynb     # Main transformation notebook
│   │   ├── silver_layer_refer.ipynb, Silver_Layer.py
│   │   └───Demo-RG_aw-azure-databrick-project/ # ARM template for Databricks
│
│   ├───Gold/                      # Synapse configurations
│   │   ├───sqlscript/             # SQL scripts: CreateSchema, CreateView, ExternalCredential
│   │   ├───linkedService/         # Synapse default linked services
│   │   ├───integrationRuntime/    # IR setup
│   │   ├───credential/            # Synapse credential config
│   │   └── Demo.txt, publish_config.json
│
├───Data/                          # Raw CSV files from AdventureWorks dataset
│   ├── AdventureWorks_Sales_2015.csv
│   ├── AdventureWorks_Customers.csv
│   ├── AdventureWorks_Products.csv
│   ├── AdventureWorks_Returns.csv
│   ├── AdventureWorks_Territories.csv
│   └── etc...
```
---

## 🛠️ Step-by-Step Pipeline Flow

### 🔹 Step 1: Data Source
- Source: Public GitHub repo with AdventureWorks CSVs (Sales, Returns, Products, Customers)
- Files include: `Sales2015.csv`, `Sales2016.csv`, `Returns.csv`, `Products.csv`

### 🔹 Step 2: Data Ingestion via ADF
- Use **HTTP connector** in ADF
- Parameterized **dynamic pipeline** with Lookup + ForEach
- Data stored in **Bronze layer** of ADLS

### 🔹 Step 3: Transformation via Databricks
- Read raw data from Bronze
- Apply:
  - Null removal
  - Data type conversions
  - Joins with dimension tables
- Write clean data to **Silver**
- Write modeled facts/dims to **Gold**

### 🔹 Step 4: Serving Layer (Synapse)
- Create **external tables** on Gold data
- Enable BI connectivity using **SQL queries**

### 🔹 Step 5: Reporting with Power BI
- Connect to Synapse
- Build interactive dashboards using cleaned & aggregated data

---
## Connect with me! 🌐

[<img target="_blank" src="https://img.icons8.com/bubbles/100/000000/linkedin.png" title="LinkedIn">](https://www.linkedin.com/in/rajabhijeet22/)       [<img target="_blank" src="https://img.icons8.com/bubbles/100/000000/github.png" title="Github">](https://github.com/abhijeetraj22)     [<img target="_blank" src="https://img.icons8.com/bubbles/100/000000/instagram-new.png" title="Instagram">](https://www.instagram.com/abhijeet_raj_/?hl=en) [<img target="_blank" src="https://img.icons8.com/bubbles/100/000000/twitter-circled.png" title="Twitter">](https://twitter.com/abhijeet_raj_/)


