PAPER = main

TEX := $(wildcard *.tex)
BIB = ref.bib

.PHONY: all split-pdf clean 

all: $(PAPER).pdf

$(PAPER).pdf: $(TEX) $(BIB)
	xelatex $(PAPER)
	bibtex $(PAPER)
	xelatex $(PAPER)
	xelatex $(PAPER)
	rm $(PAPER).aux
	rm $(PAPER).bbl
	rm $(PAPER).blg
	rm $(PAPER).log
	
split:
	python font/split-pdf.py $(PAPER)

bib:
	python font/bib-sort.py

clean:
	rm -f *.dvi $(PAPER).ps *.aux *.bbl *.blg *.log *.out *.synctex.gz $(PAPER).pdf $(PAPER)_with_ref.pdf
