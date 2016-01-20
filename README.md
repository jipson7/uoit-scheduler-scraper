###Usage

```
cd scraper

```

Edit run.sh and change the env to whatever database you want to export to.

The script wont overwrite data. It will add semesters together if run on different ones consecutivley.

If the same semester is queried on the same database. It will replace all instance of the original scrape with the new one

Example usage

```
./run.sh 201601

```
To get the 2016 Winter semester

```
./run.sh 201605

```

To get the 2016 summer semester

```
./run.sh 201509

```

To get the 2015 Fall semester, etc.
