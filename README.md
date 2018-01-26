`noisy` runs linters on noise protocols

This is super hacky pre-alpha code. Don't expect anything nice.

### Instructions:

```
pip install git+https://github.com/katrielalex/noisy
noisy .../path/to/foo.noise
```

The parser is kind of a mess. Here's a valid example, note the newline at the end of the file.

```
Noise_NN():
   -> e
   <- e, ee

```
