# This is an experimental brach, use at your own risk

There's many work to do in this branch, but these scripts used to work. 

We should clean and unify all the processes and expose a clear interface.

At the time these scripts were last used, they were able to parse data extracted from PDF files for
these competitions:

* "Gipuzkoako batel liga" results
* "Bizkaiako batel liga" results
* "Gipuzkoako traineru txapelketa" results
* "Bizkaiako traineru txapelketa" results
* "Kontxako bandera" results


## Parse "Gipuzkoako batel liga" CSV results into a Estropadak structure

Usage:

```python
python csv_to_data.py
```

## Calculating stats

```python
python calculate_stats.py <league> <year> <category>
```


## Pandas tricks

posizioak = s.calculate_posizioak_per_race('BBL', 2020, 'JG')

Create dataframe
df = pd.DataFrame(posizioak)

Calculate points:
puntuazioak = df.apply(lambda x: x.max() - x + 1, axis=1)

Calculate cumulative points:
puntuazioak.apply(np.cumsum)

Get points:
puntuazioak.apply(np.cumsum).apply(lambda x: x.max())

Sort Series descending:

puntuazioak.apply(np.cumsum).apply(lambda x: x.max()).sort_values(ascending=False)
