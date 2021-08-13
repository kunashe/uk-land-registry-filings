# UK Land Registry Filings

## Dependencies

1.  Python 3.7.6
2. pdftk
3. qpdf
4. pdftotext

## Prep

1. `mkdir ow`
2. `cd ow`
3. `mkdir pages`
4. `cp land-registry.pdf pages/`
5. `qpdf --decrypt land-registry.pdf registry.pdf`
6. `pdftk registry.pdf burst`
7. `rm registry.pdf`
8. `ls -1 * .pdf > manifest.txt`
9. `loop.sh manifest.txt |prarllel -j+8 --no-notice pdftotext -layout {} {}.txt`