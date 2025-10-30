# financial-institution-campaign-analysis

## Data preparation

### Step1: Download data

This project requires the dataset that comes with the book.

**Where to get it:**
- Book: 「スッキリわかるPythonによる機械学習入門」（須藤秋良著、株式会社フレアリンク監修）
- Sample data: https://sukkiri.jp/books/sukkiri_ml2

**Download instructions:**
```bash
# After downloading from the official website
unzip sukkiriwakaru_ml_data.zip
```

### Step2: Data placement

Place the downloaded CSV file in the `data/` directory.
```bash
# Create data directory
mkdir -p data
```

**Expected Directory Structure:**
```
your-project/
├── data/
│   ├── Bank.csv          # Bank customer data
├── models/               # 学習済みモデル保存先
├── notebooks/            # Jupyter Notebook
├── src/
│   ├── train.py
│   └── predict.py
├── requirements.txt
└── README.md
```

### Step3: Data validation

Check that the data is correctly aligned：

```bash
python scripts/verify_data.py
```

**Output example:**
```
データ検証中...
✓ data/iris.csv: 150行, 5列
✓ data/housing.csv: 506行, 14列
✓ data/titanic.csv: 891行, 12列

すべてのデータファイルが正常です！
```

### Troubleshooting

**Q: I get an error that the data file was not found**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/iris.csv'
```

A: Please check below：
1. The `data/` directory exists
2. The CSV file name is correct (including capitalization)
3. The current directory is the project root

**Q: The data seems to be different**

A: Data may vary depending on the edition of the book.
   This project is compatible with the 2nd edition data.

