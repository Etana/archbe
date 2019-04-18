# archbe
search.arch.be image downloader
## usage

```sh
archbe.py [scale factor] <URL with picture ID>
```

for example:

```sh
archbe.py https://search.arch.be/fr/rechercher-des-archives/resultats/inventaris/rabscan/eadid/BE-A0523_712045_712433_FRE/inventarisnr/I712045712433390/level/file/scan-index/121/foto/523_6000_000_00053_000_0_0240
```

will create image `523_6000_000_00053_000_0_0240.jpg` in current directory

if the output is redirected, file is written on stdout, so:

```sh
archbe.py 8 523_6000_000_00053_000_0_0240 > image.jpg
```

will save image scaled to 1/8 in `image.jpg` file

## parameters

- `[scale factor]`: by which factor the image is scaled down (by default `2`, can be `1`, `2`, `4`, `8`, `16`, `32`)
