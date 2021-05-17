# college-football

Python package to interact with college football player statistics.

`college-football` pulls data from [Sports Reference's college football site](https://www.sports-reference.com/cfb). This package is intended for interactive use in formats like Jupyter notebooks - an example is included in the `examples` directory.

The current version of the package only works with individual statistics, not overall team information. This functionality may be added in future versions.

Please be considerate when using this package to pull data, do not overwhelm Sports Reference's servers with quick requests.

In order to use `college-football`, please run the following command:
```
pip install college-football
```

Once installed `college-football` can be invoked as follows:
```
import college_football as cfb
p = cfb.Player('Ian', 'Book', 'Notre Dame', '2017-2020')
p.get_passing_summary()
```
