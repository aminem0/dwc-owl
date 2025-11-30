# DwC-OWL

## Intent of the project

The project seeks to convert [Darwin Core](https://dwc.tdwg.org/list/) and recently suggested [Darwin Core DataPackage](https://www.gbif.org/composition/3Be8w9RzbjHtK2brXxTtun/introducing-the-darwin-core-data-package) terms into OWL concepts of classes and properties.

Darwin-SW has previously explored similar ideas using OWL classes. This work extends that approach by incorporating OWL restrictions and additional object properties. The goal is to interlink entities through these object properties, creating a semantically connected network of biodiversity data rather than a simple, flat RDF representation.

The goal of the project is to provide researchers with a semantically-sound ontology to annotate biodiversity datasets. The advantages of this include, but are not limited to:

1. Enhanced data discoverability
2. Proper attribution of credits to reseachers
3. Improved dataset querying, promoting data reuse
4. Easier data publication processes to biodiversity aggregators (GBIF, OBIS)
5. Direct integration into pipelines that allow the computation of biological indicators

## Ontology exploration

The easiest way to explore the ontology is to look at the `dwc-owl.html` file in the `docs/` directory for a complete listing of the terms considered in the ontology. The documentation for this ontology can be viewed on the [GitHub Pages site of this repository](https://aminem0.github.io/dwc-owl/).

Alternatively, a visual representation of the classes and their relationships through object properties can be viewed [using WebVOWL](https://service.tib.eu/webvowl/#iri=https://raw.githubusercontent.com/aminem0/dwc-owl/refs/heads/main/dwc-owl-v2.ttl).

You can also load the `dwc-owl.ttl` file into an ontology editor such as [Protégé](https://protege.stanford.edu/). The difference is that Protégé includes reasoners such as HermiT, that allow reasoning over the test individuals created at the end of the ontology.

On that note, the HermiT reasoner is used to assess and ensure the consistency of the ontology. Through DL reasoning, it ensures that the description logic is sound and correct. 

## Initial motivation

The project was also motivated by another side-project: *sparql-completer*, a completion engine for sparql files. The neovim plugin is written in Lua and is based on a series of input Lua tables. The plugin can make calls to cURL, allowing for the direct execution of the SPARQL query, rather than through another programming language.

![Screenshot illustrating the use of *sparql-completer* offering term suggestions generated from an OWL ontology constructed using Darwin Core terms.](images/nvimsnip.png)

However, at its core, *sparql-completer* is only a completion engine, and therefore does not enforce any logical or datatype constraints. In other words, a nonsensical triple such as `bb:event123 dwcdp:happenedIn bb:identification456` will not get flagged as wrong even though it completely disregards, among other things, domain and range restrictions that I had written out. The SPARQL query will evidently (and silently) fail to retrieve any data.

The data in the triplestore follows the ontology I have described in *sparql-completer*, but does not validate it.

Therefore, I wanted to have a robust and consistent way to validate the underlying semantics. This is done by combining an OWL-based ontology and a SHACL-based validation of the constructed RDF graphs.

Originally, the semantics were more consistent with my original proposal, considering `foaf:Agent` and `foaf:Document` (which has the benefit of being equivalent to `bibo:Document`), but has been reworked to be compatible with the terms proposed by the Darwin Core DataPackage publishing model.

## Applications of the ontology

The terms in this ontology are being applied to model real-world datasets at [another GitHub repository](https://github.com/aminem0/dwc-owl-rdf).
