#####################################################################################################
# BEGIN IMPORTS
#####################################################################################################

import subprocess
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD
from pylode import OntPub
from utils import createCTOP, createDP, createEDP, createEOC, createOC, createOP, createRDP, createSC, declare_disjoint

#####################################################################################################
# BEGIN ONTOLOGY DEFINITION
#####################################################################################################

# Define all namespces to be used
AC = Namespace("http://rs.tdwg.org/ac/terms/")
ADMS = Namespace("http://www.w3.org/ns/adms#")
BIBO = Namespace("http://purl.org/ontology/bibo/")
BB = Namespace("http://bioboum.ca/")
CHRONO = Namespace("http://rs.tdwg.org/chrono/terms/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
DWCEM = Namespace("http://rs.tdwg.org/dwcem/values/")
DWCDOE = Namespace("http://rs.tdwg.org/dwcdoe/values/")
DWCIRI = Namespace("http://rs.tdwg.org/dwc/iri/")
DWCDP = Namespace("http://rs.tdwg.org/dwcdp/terms/")
DWCPW = Namespace("http://rs.tdwg.org/dwcpw/values/")
ECO = Namespace("http://rs.tdwg.org/eco/terms/")
ECOIRI = Namespace("http://rs.tdwg.org/eco/iri/")
EXIF = Namespace("http://ns.adobe.com/exif/1.0/")
GBIF = Namespace("http://rs.gbif.org/terms/")
GGBN = Namespace("http://data.ggbn.org/schemas/ggbn/terms/")
MINEXT = Namespace("http://rs.tdwg.org/mineralogy/terms/")
MIQE = Namespace("http://rs.gbif.org/terms/miqe/")
MIXS = Namespace("https://w3id.org/mixs/")
TDT = Namespace("http://rs.gbif.org/vocabulary/gbif/type_designation_type/")
VANN = Namespace("http://purl.org/vocab/vann/")
XMP = Namespace("http://ns.adobe.com/xap/1.0/")

# Create an instance of a Graph object
g = Graph()

# Bind the prefixes to the previously defined namespaces
g.bind("ac", AC)
g.bind("adms", ADMS)
g.bind("bb", BB)
g.bind("bibo", BIBO)
g.bind("chrono", CHRONO)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)
g.bind("dwc", DWC)
g.bind("dwcdoe", DWCDOE)
g.bind("dwcem", DWCEM)
g.bind("dwciri", DWCIRI)
g.bind("dwcdp", DWCDP)
g.bind("dwcpw", DWCPW)
g.bind("eco", ECO)
g.bind("exif", EXIF)
g.bind("gbif", GBIF)
g.bind("ggbn", GGBN)
g.bind("minext", MINEXT)
g.bind("miqe", MIQE)
g.bind("mixs", MIXS)
g.bind("tdt", TDT)
g.bind("vann", VANN)
g.bind("xmp", XMP)


# Define ontology URI and basic definitions.
ontology_uri = URIRef("http://bioboum.ca/dwc-owl.owl")
g.add((ontology_uri, RDF["type"], OWL["Ontology"]))
g.add((ontology_uri, OWL["versionInfo"], Literal("0.0.3")))
g.add((ontology_uri, VANN["preferredNamespacePrefix"], Literal("dwcowl")))
g.add((ontology_uri, VANN["example"], URIRef("https://github.com/aminem0/dwc-owl-rdf")))
g.add((ontology_uri, DC["title"], Literal("Darwin Core OWL")))
g.add((ontology_uri, DC["description"], Literal("Darwin Core OWL is an effort to represent Darwin Core terms, along with the newly proposed Darwin Core DataPackage terms, as OWL concepts, specifically as OWL classes and properties. Darwin-SW has previously explored similar ideas using OWL classes. This work extends that approach by incorporating OWL restrictions and additional object properties. The goal is to interlink entities through these object properties, creating a semantically connected network of biodiversity data rather than a simple, flat RDF representation.", lang="en")))
g.add((ontology_uri, DCTERMS["created"], Literal("2025-04-03", datatype=XSD["date"])))

#####################################################################################################
# BEGIN OWL CLASS DEFINITIONS
#####################################################################################################

# NOTE: RECHECK terms in example.
createOC(
    name="Media",
    namespace=AC,
    graph=g,
    pref_label=Literal("Media"),
    definition=Literal("A dcmi:MediaType or other media type with other entities as subject matter.", lang="en"),
    comments=Literal("An instance of digital textual media may be better represented as a dcterms:BibliographicResource.", lang="en"),
    examples=[
        Literal("dcmi:Sound"),
        Literal("dcmi:StillImage"),
        Literal("dcmi:MovingImage"),
    ],
    # maxcard1_restrictions=[AC["captureDevice"], AC["digitizationDate"], AC["frameRate"], AC["heightFrac"], AC["widthFrac"], XMP["CreateDate"]],
    #card0_restrictions=[AC["radius"]],
    version_of_s="http://rs.tdwg.org/ac/terms/Media",
)

createOC(
    name="Agent",
    namespace=DCTERMS,
    graph=g,
    pref_label=Literal("Agent"),
    definition=Literal("A resource that acts or has the power to act.", lang="en"),
    comments=Literal("A person, group, organization, machine, software or other entity that can act. Membership in the [dcterms:Agent] class is determined by the capacity to act, even if not doing so in a specific context. To act: To participate in an event or process by contributing through behavior, operation, or an effect resulting from active participation — regardless of whether that contribution is intentional, volitional, or conscious.", lang="en"),
    examples=[
        Literal("Carl Linnaeus"),
        Literal("The Terra Nova Expedition"),
        Literal("The National Science Foundation"),
        Literal("The El Yunque National Forest ARBIMON System"),
        Literal("ChatGPT"),
    ],
    # card1_restrictions=[DWC["agentID"], DWC["agentType"]],
    maxcard1_restrictions=[DWC["preferredAgentName"]],
    version_of_s="http://purl.org/dc/terms/Agent",
)

# NOTE: Should we consider dwc:Assertion as a special case of dwc:MeasurmentOrFact?
createOC(
    name="Assertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Assertion"),
    # card0_restrictions=[DWCDP["assertedBy"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/MeasurementOrFact",
    references_s="http://rs.tdwg.org/dwc/terms/version/MeasurementOrFact-2023-09-13",
)

createOC(
    name="BibliographicResource",
    namespace=DCTERMS,
    graph=g,
    pref_label=Literal("Bibliographic Resource"),
    definition=Literal("A book, article, or other documentary resource.", lang="en"),
    version_of_s="http://purl.org/dc/terms/BibliographicResource",
)

createOC(
    name="ChronometricAge",
    namespace=CHRONO,
    graph=g,
    pref_label=Literal("Chronometric Age"),
    definition=Literal("An approximation of temporal position (in the sense conveyed by [https://www.w3.org/TR/owl-time/#time:TemporalPosition]) that is supported by evidence.", lang="en"),
    comments=Literal("The age of a [dwc:MaterialEntity] and how this age is known, whether by a dating assay, or a relative association with dated material, or legacy collection information.", lang="en"),
    examples=[
        Literal("an age range associated with a specimen derived from an AMS dating assay applied to an oyster shell in the same stratum"),
        Literal("an age range associated with a specimen derived from a ceramics analysis based on other materials found in the same stratum"),
        Literal("a maximum age associated with a specimen derived from K-Ar dating applied to a proximal volcanic tuff found stratigraphically below the specimen"),
        Literal("an age range of a specimen based on its biostratigraphic content"),
        Literal("an age of a specimen based on what is reported in legacy collections data"),
    ],
    version_of_s="http://rs.tdwg.org/chrono/terms/ChronometricAge",
    references_s="http://rs.tdwg.org/chrono/terms/version/ChronometricAge-2021-02-21",
)

# NOTE: Review integration of skos:Concept and owl:Classes.
# Here there is a defined skos:ConceptScheme
createEOC(
    name="DegreeOfEstablishment",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Degree Of Establishment", lang="en"),
    definition=Literal("Controlled value for Darwin Core terms with local name degreeOfEstablishment.", lang="en"),
    comments=Literal("For details and rationale, see [Groom et al. 2019](https://doi.org/10.3897/biss.3.38084).", lang="en"),
    one_of=[
        URIRef("http://rs.tdwg.org/dwcdoe/values/d001"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d002"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d003"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d004"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d005"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d006"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d007"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d008"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d009"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d010"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d011"),
    ],
)

# NOTE: Review integration of skos:Concept and owl:Classes.
# Here there is a defined skos:ConceptScheme
createEOC(
    name="EstablishmentMeans",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Establishment Means", lang="en"),
    definition=Literal("Controlled value for Darwin Core terms with local name establishmentMeans.", lang="en"),
    comments=Literal("For details and rationale, see [Groom et al. 2019](https://doi.org/10.3897/biss.3.38084).", lang="en"),
    one_of=[
        URIRef("http://rs.tdwg.org/dwcem/values/e001"),
        URIRef("http://rs.tdwg.org/dwcem/values/e002"),
        URIRef("http://rs.tdwg.org/dwcem/values/e003"),
        URIRef("http://rs.tdwg.org/dwcem/values/e004"),
        URIRef("http://rs.tdwg.org/dwcem/values/e005"),
        URIRef("http://rs.tdwg.org/dwcem/values/e006"),
        URIRef("http://rs.tdwg.org/dwcem/values/e007"),
    ],
)

# NOTE: Should we allow for several parent events? I mean that in the sense of OWL cardinalities.
createOC(
    name="Event",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Event"),
    definition=Literal("An action, process, or set of circumstances occurring at a [dcterms:Location] during a period of time.", lang="en"),
    examples=[
        Literal("a material collecting event"),
        Literal("a bird observation"),
        Literal("a camera trap image capture"),
        Literal("an organism occurrence"),
        Literal("a biotic survey"),
    ],
    # card1_restrictions=[DWC["eventID"]],
    # card0_restrictions=[DWCDP["happenedDuring"]],
    maxcard1_restrictions=[DWC["preferredEventName"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/Event",
    references_s="http://rs.tdwg.org/dwc/terms/version/Event-2023-09-18",
)

createOC(
    name="GeologicalContext",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Geological Context"),
    definition=Literal("A set of geological designations, such as stratigraphy, that qualifies a [dcterms:Location].", lang="en"),
    examples=[
        Literal("a particular lithostratigraphic layer"),
        Literal("a specific chronostratigraphic unit")
    ],
    card1_restrictions=[DWC["geologicalContextID"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/GeologicalContext",
    references_s="http://rs.tdwg.org/dwc/terms/version/GeologicalContext-2023-09-18",
)

createOC(
    name="Identification",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Identification"),
    definition=Literal("A classification of a resource according to a classification scheme.", lang="en"),
    comments=Literal("For biology, the assignment of a scientific name or taxon concept to a [dwc:Organism].", lang="en"),
    examples=[
        Literal("a subspecies determination of an organism"),
        Literal("a nomenclatural act designating a specimen as a holotype"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/Identification",
    references_s="http://rs.tdwg.org/dwc/terms/version/Identification-2023-09-18",
)

createOC(
    name="Location",
    namespace=DCTERMS,
    graph=g,
    pref_label=Literal("Location"),
    definition=Literal("A spatial region or named place.", lang="en"),
    examples=[
        Literal("the municipality of San Carlos de Bariloche, Río Negro, Argentina"),
        Literal("the place defined by a georeference")
    ],
    version_of_s="http://purl.org/dc/terms/Location",
)

createOC(
    name="MaterialEntity",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Material Entity"),
    definition=Literal("An entity that can be identified, exist for some period of time, and consist in whole or in part of physical matter while it exists.", lang="en"),
    comments=Literal("The term is defined at the most general level to admit descriptions of any subtype of material entity within the scope of Darwin Core. In particular, any kind of material sample, preserved specimen, fossil, or exemplar from living collections is intended to be subsumed under this term.", lang="en"),
    examples=[
        Literal("the entire contents of a trawl"),
        Literal("a subset of the contents of a trawl"),
        Literal("the body of a fish"),
        Literal("the stomach contents of a fish"),
        Literal("a rock containing fossils"),
        Literal("a fossil within a rock"),
        Literal("an herbarium sheet with its attached plant specimen"),
        Literal("a flower on a plant specimen"),
        Literal("a specific water sample"),
        Literal("an isolated molecule of DNA"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/MaterialEntity",
    references_s="http://rs.tdwg.org/dwc/terms/version/MaterialEntity-2023-09-13",
)

# WARN: Add triples to express owl:Restriction here then integrate to function
# This is done to avoid cross-class use of the term dwcdp:isDerivedFrom, which is the union of
# ac:Media and dwc:MaterialEntity.
R_isDerivedFrom = BNode()
g.add((R_isDerivedFrom, RDF["type"], OWL["Restriction"]))
g.add((R_isDerivedFrom, OWL["onProperty"], DWCDP["isDerivedFrom"]))
g.add((R_isDerivedFrom, OWL["allValuesFrom"], DWC["MaterialEntity"]))
g.add((DWC["MaterialEntity"], RDFS["subClassOf"], R_isDerivedFrom))

createOC(
    name="NucleotideAnalysis",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Nucleotide Analysis"),
    definition=Literal("A link between a [dwc:NucleotideSequence] and a [dwc:Event] and a [dwc:MaterialEntity] from which it was derived, using a specified [dwc:Protocol].", lang="en"),
    # card1_restrictions=[DWC["eventID"], DWC["molecularProtocolID"], DWC["nucleotideAnalysisID"], DWC["nucleotideSequenceID"]],
    # card01_restrictions=[DWC["materialEntityID"], DWC["readCount"], DWC["totalReadCount"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/NucleotideAnalysis",
)

createOC(
    name="NucleotideSequence",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Nucleotide Sequence"),
    definition=Literal("A digital representation of a nucleotide sequence.", lang="en"),
    card1_restrictions=[DWC["nucleotideSequenceID"], DWC["sequence"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/NucleotideSequence",
)

createOC(
    name="Occurrence",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Occurrence"),
    definition=Literal("A state of a [dwc:Organism] in a [dwc:Event].", lang="en"),
    examples=[
        Literal("a wolf pack on the shore of Kluane Lake in 1988"),
        Literal("a virus in a plant leaf in the New York Botanical Garden at 15:29 on 2014-10-23"),
        Literal("a fungus in Central Park in the summer of 1929"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/Occurrence",
    references_s="http://rs.tdwg.org/dwc/terms/version/Occurrence-2023-09-18",
)

createOC(
    name="Organism",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Organism"),
    definition=Literal("A particular organism or defined group of organisms considered to be taxonomically homogeneous.", lang="en"),
    comments=Literal("Instances of the [dwc:Organism] class are intended to facilitate linking one or more [dwc:Identification] instances to one or more [dwc:Occurrence] instances. Therefore, things that are typically assigned scientific names (such as viruses, hybrids and lichens) and aggregates whose [dwc:Occurrence]s are typically recorded (such as packs, clones, and colonies) are included in the scope of this class.", lang="en"),
    examples=[
        Literal("a specific bird"),
        Literal("a specific wolf pack"),
        Literal("a specific instance of a bacterial culture"),
    ],
    # card1_restrictions=[DWC["organismID"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/Organism",
    references_s="http://rs.tdwg.org/dwc/terms/version/Organism-2023-09-18",
)

# NOTE: Seems like a good thing to model with reification. Not many software support RDF-Star, but rdf:Statement has been around since the early days.
createOC(
    name="OrganismInteraction",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Organism Interaction"),
    definition=Literal("An interaction between two [dwc:Organism]s during a [dwc:Event].", lang="en"),
    comments=Literal("Supports only primary observed interactions, not habitualor derived taxon-level interactions. Pairwise interactions must be used to represent multi-organism interactions. When possible, typify the action rather than the state from which the action is inferred, with the actor as the subject in [dwc:Occurrence] and the acted-upon as the related [dwc:Occurrence]. Only one direction of a two-way interaction is necessary, though both are permissible as distinct [dwc:OrganismInteraction]s with distinct subject [dwc:Occurrence]s.", lang="en"),
    examples=[
        Literal("a bee visiting a flower"),
        Literal("a Mallophora ruficauda hunting an Apis mellifera in flight"),
        Literal("a viral infection in a plant"),
        Literal("a female spider mating with a male spider"),
        Literal("a lion cub nursing from its mother"),
        Literal("a mosquito sucking blood from a chimpanzee's arm"),
        Literal("a slug eating a fungus growing on a decomposing stump (2 interactions)"),
    ],
    # card1_restrictions=[DWC["organismInteractionID"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/OrganismInteraction",
)

# NOTE: Review integration of skos:Concept and owl:Classes.
# Here there is a defined skos:ConceptScheme
createEOC(
    name="Pathway",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Pathway", lang="en"),
    definition=Literal("Controlled value for Darwin Core terms with local name pathway.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    one_of=[
        URIRef("http://rs.tdwg.org/dwcpw/values/p001"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p002"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p003"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p004"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p005"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p006"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p007"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p008"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p009"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p010"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p011"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p012"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p013"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p014"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p015"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p016"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p017"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p018"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p019"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p020"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p021"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p022"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p023"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p024"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p025"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p026"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p027"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p028"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p029"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p030"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p031"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p032"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p033"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p034"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p035"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p036"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p037"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p038"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p039"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p040"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p041"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p042"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p043"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p044"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p049"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p050"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p051"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p052"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p053"),
    ],
)

# WARN: Not in original DwCDP definition, but I added it.
# NOTE: Should it be a "legal" document. Maybe consider dcterms:LicenseDocument?
createOC(
    name="Permit",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Permit"),
    definition=Literal("A document, allowing for the execution of certain activities.", lang="en"),
    examples=[
        Literal("a license to put up mist-nets to sample for bird communities"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/Permit",
)

# TEST: Consider a class to contain the controlled types of Permits
# Here the namespace is referred to as ggbn:
createEOC(
    name="permitStatus_vocabulary",
    namespace=GGBN,
    graph=g,
    pref_label=Literal("Permit Status Vocabulary"),
    definition=Literal("Vocabulary of ggbn:permitStatus.", lang="en"),
    one_of=[
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Permit_available"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Permit_not_required"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Permit_not_available"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Unknown"),
    ],
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/permitStatus_vocabulary",
)

# TEST: Consider a class to contain the controlled types of Permits
# Here the namespace is referred to as ggbn:
# Beware the Data use and the 
createEOC(
    name="permitType_vocabulary",
    namespace=GGBN,
    graph=g,
    pref_label=Literal("Permit Type Vocabulary"),
    definition=Literal("Vocabulary of ggbn:permitType term.", lang="en"),
    one_of=[
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Collecting_Permit"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Import_Permit"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Export_Permit"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Intellectual_Property_Rights"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Copyright"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Patent"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Data_use"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Phytosanitary"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Salvage"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Exemption_Permit"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Material_Transfer_Agreement"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Internationally_Recognized_Certificate_of_Compliance"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Contract"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Memorandum_of_Understanding"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Memorandum_of_Cooperation"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Veterinary_Certificate"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Human_Pathogens"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Genetically_Modified_Organism"),
        URIRef("http://data.ggbn.org/schemas/ggbn/terms/Other"),
    ],
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/permitType_vocabulary",
)

createOC(
    name="Protocol",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Protocol"),
    definition=Literal("A method used during an action.", lang="en"),
    examples=[
        Literal("a pitfall method for sampling ground-dwelling arthropods"),
        Literal("a point-radius georeferencing method"),
        Literal("a linear regression model to estimate body mass from skeletal measurements"),
        Literal("a Bayesian phylogenetic inference method"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/Protocol",
)

createOC(
    name="Provenance",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Provenance"),
    definition=Literal("Information about an entity's origins.", lang="en"),
    comments=Literal("This is a convenience class to group related properties.", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/provenance",
)

# WARN: dwc:OrganismRelationship is not recognized, so for now consider dwc:ResourceRelationship. But do note that 
# WARN: Try and consider only specific cases, otherwise it might overlap with other owl:ObjectProperties.
# For example, the MaterialEntity example can also be handled by dwcdp:isPartOf or dwcdp:isDerivedFrom.
createOC(
    name="ResourceRelationship",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Resource Relationship"),
    definition=Literal("A relationship of one [rdfs:Resource] ([http://www.w3.org/2000/01/rdf-schema#Resource]) to another.", lang="en"),
    comments=Literal("Resources can be thought of as identifiable records or instances of classes and may include, but need not be limited to instances of [dwc:Occurrence], [dwc:Organism], [dwc:MaterialEntity], [dwc:Event], [dcterms:Location], [dwc:GeologicalContext], [dwc:Identification], or [dwc:Taxon.]", lang="en"),
    examples=[
        Literal("an instance of a dwc:Organism is the mother of another instance of a dwc:Organism"),
        Literal("a uniquely identified dwc:Occurrence represents the same dwc:Occurrence as another uniquely identified dwc:Occurrence"),
        Literal("a dwc:MaterialEntity is a subsample of another dwc:MaterialEntity"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/ResourceRelationship",
    references_s="http://rs.tdwg.org/dwc/terms/version/ResourceRelationship-2023-09-13",
)

createEOC(
    name="TypeDesignationType",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Type Designation Type"),
    definition=Literal("A category that best matches the nature of a type designation.", lang="en"),
    comments=Literal("From [https://rs.gbif.org/extension/gbif/1.0/typesandspecimen.xml](https://rs.gbif.org/extension/gbif/1.0/typesandspecimen.xml).", lang="en"),
    one_of=[
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/originalDesignation"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/presentDesignation"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/subsequentDesignation"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/monotypy"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/subsequentMonotypy"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/absoluteTautonymy"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/monotypy"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/linnaeanTautonymy"),
        URIRef("http://rs.gbif.org/vocabulary/gbif/type_designation_type/rulingByCommission"),
    ],
    version_of_s="http://rs.gbif.org/terms/1.0/typeDesignationType",
    references_s="https://rs.gbif.org/extension/gbif/1.0/typesandspecimen.xml",
)

createOC(
    name="UsagePolicy",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Usage Policy"),
    definition=Literal("Information about rights, usage, and attribution statements applicable to an entity.", lang="en"),
    comments=Literal("This is a convenience class to group related properties.", lang="en"),
    # card1_restrictions=[DWC["usagePolicyID"]],
    # card01_restrictions=[DC["rights"], DCTERMS["rights"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/UsagePolicy",
)

createOC(
    name="Survey",
    namespace=ECO,
    graph=g,
    pref_label=Literal("Survey"),
    definition=Literal("A biotic survey or inventory.", lang="en"),
    comments=Literal("This class includes properties found in the Humboldt Extension to Darwin Core ([eco:]), except for target scope terms, which can be accomodated in [eco:SurveyTarget].", lang="en"),
    examples=[
        Literal("a botanical survey of a protected area to assess native and invasive plant species"),
        Literal("a wetland vegetation mapping"),
        Literal("a camera trap deployment in a rainforest to monitor large mammals"),
        Literal("a frog call survey in wetlands across breeding seasons"),
        Literal("a coverboard survey for reptiles in forested environments"),
        Literal("a pollinator survey in an agricultural landscape"),
        Literal("a macroinvertebrate sampling in a freshwater stream to assess water quality"),
        Literal("a habitat- or ecosystem-level survey (e.g. coral reef health assessment, forest biodiversity assessment)"),
        Literal("an environmental impact assessment (e.g. pre-construction baseline survey for a wind farm project)"),
    ],
    # card1_restrictions=[DWC["eventID"], DWC["surveyID"]],
    version_of_s="http://rs.tdwg.org/eco/terms/Survey",
)

createOC(
    name="SurveyTarget",
    namespace=ECO,
    graph=g,
    pref_label=Literal("Survey Target"),
    definition=Literal("An intended scope for [dwc:Occurrence]s in a [eco:Survey].", lang="en"),
    examples=[
        Literal("all bird species"),
        Literal("all bird species except Larus gulls, fulmars and kittiwakes"),
        Literal("reproductive female Ctenomys sociabilis (only)"),
        Literal("Oncorhynchus mykiss and Oncorhynchus clarkii (only)"),
        Literal("all total lengths except < 12 inches"),
    ],
    # card1_restrictions=[DWC["surveyID"], DWC["surveyTargetID"]],
    version_of_s="http://rs.tdwg.org/eco/terms/SurveyTarget",
)

#####################################################################################################
# BEGIN CLASSES THROUGH OBJECT PROPERTY DEFINITIONS
#####################################################################################################

# createCTOP(
#     name="AssertionAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Assertion Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["assertedBy"],
#     use_inverse=True,
#     values_class=DWC["Assertion"],
#     definition=Literal("An instance of a [dcterms:Agent] that has made a [dwc:Assertion].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:assertedBy], the class is defined in description logic as [dwcdp:AssertionAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:assertedBy]⁻).[dwc:Assertion].", lang="en")
# )

# createCTOP(
#     name="AuthorAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Author Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["authoredBy"],
#     use_inverse=True,
#     values_class=DCTERMS["BibliographicResource"],
#     definition=Literal("An instance of a [dcterms:Agent] that has authored a [dcterms:BibliographicResource].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:authoredBy], the class is defined in description logic as [dwcdp:AuthorAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:authoredBy]⁻).[dcterms:BibliographicResource].", lang="en")
# )

# # WARN: Related to WebVOWL
# # TEST: Trying an inverse object property

# g.add((DWCDP["commentedOn"], OWL["inverseOf"], DWCDP["commentedBy"]))

# createCTOP(
#     name="CommenterAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Commenter Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["commentedOn"],
#     use_inverse=False,
#     values_class=AC["Media"],
#     definition=Literal("An instance of a [dcterms:Agent] that has commented a [dwc:Media].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:commentedBy], the class is defined in description logic as [dwcdp:Commenter] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:commentedBy]⁻).[ac:Media].", lang="en")
# )

# createCTOP(
#     name="ConductorAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Conductor Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["conductedBy"],
#     use_inverse=True,
#     values_class=DWC["Event"],
#     definition=Literal("An instance of a [dcterms:Agent] that has conducted a [dwc:Event].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:conductedBy], the class is defined in description logic as [dwc:ConductorAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:conductedBy]⁻).[dwc:Event].", lang="en")
# )

# # NOTE: Possibly find a better name, it looks too much like the object property dwcdp:datedMaterial
# createCTOP(
#     name="DatedMaterialEntity",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Dated Material Entity"),
#     subclass_list=[DWC["MaterialEntity"]],
#     object_prop=DWCDP["datedMaterial"],
#     use_inverse=True,
#     values_class=CHRONO["ChronometricAge"],
#     definition=Literal("An instance of a [dwc:MaterialEntity] that has been dated by a [chrono:ChronometricAge].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:datedMaterial], the class is defined in description logic as [dwc:DatedMaterialEntity] ≡ [dwc:MaterialEntity] ⊓ ∃([dwcdp:datedMaterial]⁻).[dwc:MaterialEntity].", lang="en")
# )

# # NOTE: Used bibo: property bibo:editor.
# # But bibo: does not provide straightforward object properties for other relationships like authoring and publishing.
# createCTOP(
#     name="EditorAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Editor Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     # object_prop=DWCDP.editedBy,
#     object_prop=BIBO["editor"],
#     use_inverse=True,
#     values_class=DCTERMS["BibliographicResource"],
#     definition=Literal("An instance of a [dcterms:Agent] that has edited a [dcterms:BibliographicResource].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:editedBy], the class is defined in description logic as [dwcdp:EditorAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:editedBy]⁻).[dcterms:BibliographicResource].", lang="en")
# )

# createCTOP(
#     name="FunderAgent",
#     namespace=DWC,
#     graph=g,
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["fundedBy"],
#     values_class=DWC["Provenance"],
#     use_inverse=True,
#     pref_label=Literal("Funder Agent"),
#     definition=Literal("An instance of a [dcterms:Agent] that has funded a [dwc:Provenance].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:fundedBy], the class is defined in description logic as [dwcdp:FunderAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:fundedBy]⁻).[dwc:Provenance].", lang="en")
# )

# # NOTE: Possibly find a better name, a bit too long
# createCTOP(
#     name="GeologicalContextMaterialEntity",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Geological Context Material Entity"),
#     subclass_list=[DWC["MaterialEntity"]],
#     object_prop=DWCDP["happenedWithin"],
#     use_inverse=False,
#     values_class=DWC["GeologicalContext"],
#     definition=Literal("An instance of a [dwc:MaterialEntity] that happened within a [dwc:GeologicalContext].", lang="en"),
# )

# createCTOP(
#     name="GeoreferencerAgent",
#     namespace=DWC,
#     graph=g,
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["georeferencedBy"],
#     values_class=DCTERMS["Location"],
#     use_inverse=True,
#     pref_label=Literal("Georeferencer Agent"),
#     definition=Literal("An instance of a [dcterms:Agent] that has georeferenced a [dcterms:Location].", lang="en"),
#     comments=Literal("Due to the directionality of the property [dwcdp:georeferencedBy], the class is defined in description logic as [dwcdp:GeoreferencerAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:georeferencedBy]⁻).[dcterms:Location].", lang="en")
# )

# createCTOP(
#     name="IdentificationAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Identification Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["identifiedBy"],
#     use_inverse=True,
#     values_class=DWC["Identification"],
#     definition=Literal("An instance of a [dcterms:Agent] that has published a [dwc:Identification]."),
#     comments=Literal("Due to the directionality of the property [dwcdp:identifiedBy], the class is defined in description logic as [dwcdp:IdentificationAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:identifiedBy]⁻).[dwc:Identification].")
# )

# createCTOP(
#     name="PublisherAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Publisher Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["publishedBy"],
#     use_inverse=True,
#     values_class=DCTERMS["BibliographicResource"],
#     definition=Literal("An instance of a [dcterms:Agent] that has published a [dcterms:BibliographicResource]."),
#     comments=Literal("Due to the directionality of the property [dwcdp:publishedBy], the class is defined in description logic as [dwcdp:PublisherAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:publishedBy]⁻).[dcterms:BibliographicResource].")
# )

# createCTOP(
#     name="ReviewerAgent",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Reviewer Agent"),
#     subclass_list=[DCTERMS["Agent"]],
#     object_prop=DWCDP["reviewedBy"],
#     use_inverse=True,
#     values_class=AC["Media"],
#     definition=Literal("An instance of a [dcterms:Agent] that has reviewed a [dwc:Media]."),
#     comments=Literal("Due to the directionality of the property [dwcdp:reviewedBy], the class is defined in description logic as [dwcdp:Reviewer] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:reviewedBy]⁻).[dwc:Media].")
# )


###############################################################################################


# createCTOP(
#     name="EventAssertion",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Event Assertion"),
#     subclass_list=[DWC["Assertion"]],
#     object_prop=DWCDP["about"],
#     use_inverse=False,
#     values_class=DWC["Event"],
#     definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:Event]."),
# )

# createCTOP(
#     name="ChronometricAgeAssertion",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Chronometric Age Assertion"),
#     subclass_list=[DWC["Assertion"]],
#     object_prop=DWCDP["about"],
#     use_inverse=False,
#     values_class=CHRONO["ChronometricAge"],
#     definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:ChronometricAge]."),
# )


createCTOP(
    name="MaterialEntityAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Material Entity Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=DWC["MaterialEntity"],
    definition=Literal("A dwc:Assertion made by a dcterms:Agent about a dwc:MaterialEntity."),
)

# createCTOP(
#     name="MediaAssertion",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Media Assertion"),
#     subclass_list=[DWC["Assertion"]],
#     object_prop=DWCDP["about"],
#     use_inverse=False,
#     values_class=AC["Media"],
#     definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [ac:Media]."),
# )

# createCTOP(
#     name="NucleotideAnalysisAssertion",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Nucleotide Analysis Assertion"),
#     subclass_list=[DWC["Assertion"]],
#     object_prop=DWCDP["about"],
#     use_inverse=False,
#     values_class=DWC["NucleotideAnalysis"],
#     definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:NucleotideAnalysis]."),
# )

createCTOP(
    name="OccurrenceAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Occurrence Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=DWC["Occurrence"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:Occurrence]."),
)

createCTOP(
    name="OrganismAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Organism Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=DWC["Organism"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:Organism]."),
)



##########################################################



# createCTOP(
#     name="AssertionProtocol",
#     namespace=DWCDP,
#     graph=g,
#     pref_label=Literal("Assertion Protocol"),
#     subclass_list=[DWC["Protocol"]],
#     object_prop=DWCDP["followed"],
#     use_inverse=True,
#     values_class=DWC["Assertion"],
#     definition=Literal("A [dwc:Protocol] followed by a [dcterms:Agent] for a [dwc:Assertion]."),
#     comments=Literal("Due to the directionality of the property [dwcdp:followed], the class is defined in description logic as [dwc:EventProtocol] ≡ [dwc:Protocol] ⊓ ∃([dwcdp:followed]⁻).[dwc:Assertion].")
# )

# # GOOD COMPLEX EXAMPLE
# # BEFORE AFTER ADD
# createCTOP(
#     name="EventProtocol",
#     namespace=DWCDP,
#     graph=g,
#     pref_label=Literal("Event Protocol"),
#     subclass_list=[DWC["Protocol"]],
#     object_prop=DWCDP["followed"],
#     use_inverse=True,
#     values_class=DWC["Event"],
#     definition=Literal("A [dwc:Protocol] followed by a [dcterms:Agent] for a [dwc:NucleotideAnalysis]."),
#     comments=Literal("Due to the directionality of the property [dwcdp:followed], the class is defined in description logic as [dwc:EventProtocol] ≡ [dwc:Protocol] ⊓ ∃([dwcdp:followed]⁻).[dwc:Event].")
# )

# NOTE: Particularly important one. It is the only dwc:Protocol that is the domain of the properties from GBIF, MIQE, MIXS, et al.
createCTOP(
    name="MolecularProtocol",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Molecular Protocol"),
    subclass_list=[DWC["Protocol"]],
    object_prop=DWCDP["followed"],
    use_inverse=True,
    values_class=DWC["NucleotideAnalysis"],
    definition=Literal("A [dwc:Protocol] used to derive and identify a [dwc:NucleotideSequence] from a [dwc:MaterialEntity]."),
    comments=Literal("Due to the directionality of the property [dwcdp:followed], the class is defined in description logic as [dwc:MolecularProtocol] ≡ [dwc:Protocol] ⊓ ∃([dwcdp:followed]⁻).[dwc:NucleotideAnalysis]."),
    card1_restrictions=[DWC["molecularProtocolID"]],
    maxcard1_restrictions=[DWC["assayType"],
                           MIXS["0000001"], MIXS["0000002"], MIXS["0000003"], MIXS["0000005"], MIXS["0000006"], MIXS["0000008"],
                           MIXS["0000012"], MIXS["0000013"], MIXS["0000015"], MIXS["0000016"], MIXS["0000017"], MIXS["0000020"],
                           
                           MIXS["0000092"], MIXS["0001107"], MIXS["0001320"]]
)

##############################################

# # NOTE: owl:inverseFunction test
# createCTOP(
#     name="AgentMedia",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Agent Media"),
#     subclass_list=[AC["Media"]],
#     object_prop=DWCDP["isMediaOf"],
#     use_inverse=False,
#     values_class=DCTERMS["Agent"],
#     definition=Literal("A [ac:Media] about a [dcterms:Agent]."),
# )

# # NOTE: owl:inverseFunction test
# createCTOP(
#     name="EventMedia",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Event Media"),
#     subclass_list=[AC["Media"]],
#     object_prop=DWCDP["isMediaOf"],
#     use_inverse=False,
#     values_class=DWC["Event"],
#     definition=Literal("A [ac:Media] about a [dwc:Event]."),
# )

# # NOTE: owl:inverseFunction test
# createCTOP(
#     name="GeologicalContextMedia",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Geological Context Media"),
#     subclass_list=[AC["Media"]],
#     object_prop=DWCDP["isMediaOf"],
#     use_inverse=False,
#     values_class=DWC["GeologicalContext"],
#     definition=Literal("A [ac:Media] about a [dwc:GeologicalContext]."),
# )

# # NOTE: owl:inverseFunction test
# createCTOP(
#     name="MaterialEntityMedia",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Material Entity Media"),
#     subclass_list=[AC["Media"]],
#     object_prop=DWCDP["isMediaOf"],
#     use_inverse=False,
#     values_class=DWC["MaterialEntity"],
#     definition=Literal("A [ac:Media] about a [dwc:MaterialEntity]."),
# )

# # NOTE: owl:inverseFunction test
# createCTOP(
#     name="OccurrenceMedia",
#     namespace=DWC,
#     graph=g,
#     pref_label=Literal("Occurrence Media"),
#     subclass_list=[AC["Media"]],
#     object_prop=DWCDP["isMediaOf"],
#     use_inverse=False,
#     values_class=DWC["Occurrence"],
#     definition=Literal("A [ac:Media] about a [dwc:Occurrence]."),
# )

# g.add((DWCDP["hasMedia"], OWL["inverseOf"], DWCDP["isMediaOf"]))


#########################################################

# NOTE: Create dwc:OrganismRelationship by hand for now
# Class declaration
g.add((DWC["OrganismRelationship"], RDF["type"], OWL["Class"]))
g.add((DWC["OrganismRelationship"], RDFS["subClassOf"], DWC["ResourceRelationship"]))

# Add DEFINEDBY
g.add((DWC["OrganismRelationship"], RDFS["isDefinedBy"], URIRef(str(DWC))))
g.add((DWC["OrganismRelationship"], SKOS["prefLabel"], Literal("Organism Relationship")))
g.add((DWC["OrganismRelationship"], SKOS["definition"], Literal("A [dwc:ResourceRelationship] of one [dwc:Organism] to another [dwc:Organism].", lang="en")))
g.add((DWC["OrganismRelationship"], RDFS["comment"], Literal("A [dwc:OrganismRelationship] must be a permanent relationship. Ephemeral relationships between [dwc:Organism]s should be recorded as [dwc:OrganismInteraction]s.", lang="en")))

# OWL Restrictions
Rsubj_class = BNode()
g.add((Rsubj_class, RDF["type"], OWL["Restriction"]))
g.add((Rsubj_class, OWL["onProperty"], DWCDP["relationshipOf"]))
g.add((Rsubj_class, OWL["someValuesFrom"], DWC["Organism"]))
g.add((DWC["OrganismRelationship"], RDFS["subClassOf"], Rsubj_class))

Robj_class = BNode()
g.add((Robj_class, RDF["type"], OWL["Restriction"]))
g.add((Robj_class, OWL["onProperty"], DWCDP["relationshipTo"]))
g.add((Robj_class, OWL["someValuesFrom"], DWC["Organism"]))
g.add((DWC["OrganismRelationship"], RDFS["subClassOf"], Robj_class))

#####################################################################################################
# BEGIN INDIVIDUALS
#####################################################################################################

# createSC(
#     name="originalDesignation",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Original Designation", lang="en"),
#     definition=Literal("If one nominal species is explicitly designated as the type species when a nominal genus-group taxon is established, that nominal species is the type species (type by original designation).", lang="en"),
# )

# createSC(
#     name="presentDesignation",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Present Designation", lang="en"),
# )

# createSC(
#     name="subsequentDesignation",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Subsequent Designation", lang="en"),
# )

# createSC(
#     name="monotypy",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Monotypy", lang="en"),
#     definition=Literal("Type species by monotypy. When an author establishes a new nominal genus-group taxon for a single taxonomic species and denotes that species by an available name, the nominal species so named is the type species.", lang="en"),
# )

# createSC(
#     name="subsequentMonotypy",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Subsequent Monotypy", lang="en"),
# )

# createSC(
#     name="tautonymy",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Tautonymy", lang="en"),
#     definition=Literal("If a valid species-group name, or its cited synonym, originally included in a nominal genus-group taxon is identical with the name of that taxon, the nominal species denoted by that specific name (if available) is the type species.", lang="en")
# )

# createSC(
#     name="absoluteTautonymy",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Absolute Tautonymy", lang="en"),
# )

# createSC(
#     name="linnaeanTautonymy",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Linnaean Tautonymy", lang="en"),
#     definition=Literal("The identical spelling of a new generic or subgeneric name established before 1931 and a pre-1758 name cited as a synonym of only one of the species or subspecies originally included in that genus.", lang="en",)
# )

# createSC(
#     name="rulingByCommission",
#     namespace=TDT,
#     graph=g,
#     pref_label=Literal("Ruling By Commission", lang="en"),
# )

# createSC(
#     name="Collecting_Permit",
#     namespace=GGBN,
#     graph=g,
#     pref_label=Literal("Collecting Permit", lang="en"),
#     definition=Literal("A value of the ggbnvoc:permitType_vocabulary.", lang="en"),
# )

# createSC(
#     name="Import_Permit",
#     namespace=GGBN,
#     graph=g,
#     pref_label=Literal("Import Permit", lang="en"),
#     definition=Literal("A value of the ggbnvoc:permitType_vocabulary.", lang="en"),
# )

createSC(
    name="d001",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Native (category A)", lang="en"),
    definition=Literal("Not transported beyond limits of native range.", lang="en"),
    comments=Literal("Considered native and naturally occurring. See also \"category A\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d001",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d001-2021-09-01",
)

createSC(
    name="d002",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Captive (category B1)", lang="en"),
    definition=Literal("Individuals in captivity or quarantine (i.e., individuals provided with conditions suitable for them, but explicit measures of containment are in place).", lang="en"),
    comments=Literal("Only for cases where specific actions have been taken place to prevent escape of individuals or propagules. See also \"category B1\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d002",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d002-2021-09-01",
)

createSC(
    name="d003",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Cultivated (category B2)", lang="en"),
    definition=Literal("Individuals in cultivation (i.e., individuals provided with conditions suitable for them, but explicit measures to prevent dispersal are limited at best).", lang="en"),
    comments=Literal("Examples include gardens, parks and farms. See also \"category B2\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d003",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d003-2021-09-01",
)

createSC(
    name="d004",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Released (category B3)", lang="en"),
    definition=Literal("Individuals directly released into novel environment.", lang="en"),
    comments=Literal("For example, fish stocked for angling, birds for hunting. See also \"category B2\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d004",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d004-2021-09-01",
)

createSC(
    name="d005",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Failing (category C0)", lang="en"),
    definition=Literal("Individuals released outside of captivity or cultivation in a location, but incapable of surviving for a significant period.", lang="en"),
    comments=Literal("For example, frost-tender plants sown or planted in a cold climate. See also \"category C0\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d005",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d005-2021-09-01",
)

createSC(
    name="d006",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Casual (category C1)", lang="en"),
    definition=Literal("Individuals surviving outside of captivity or cultivation in a location with no reproduction.", lang="en"),
    comments=Literal("Trees planted in the wild for forestry or ornament may come under this category. See also \"category C1\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d006",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d006-2021-09-01",
)

createSC(
    name="d007",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Reproducing (category C2)", lang="en"),
    definition=Literal("Individuals surviving outside of captivity or cultivation in a location with no reproduction.", lang="en"),
    comments=Literal("Offspring are produced, but these either do not survive or are not fertile enough to maintain the population. See also \"category C2\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d007",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d007-2021-09-01",
)

createSC(
    name="d008",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Established (category C3)", lang="en"),
    definition=Literal("Individuals surviving outside of captivity or cultivation in a location. Reproduction occurring, and population self-sustaining.", lang="en"),
    comments=Literal("The population is maintained by reproduction, but is not spreading. See also \"category C2\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d008",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d008-2021-09-01",
)

createSC(
    name="d009",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Colonising (category D1)", lang="en"),
    definition=Literal("Self-sustaining population outside of captivity or cultivation, with individuals surviving a significant distance from the original point of introduction.", lang="en"),
    comments=Literal("The population is maintained by reproduction and is spreading. See also \"category D1\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d009",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d009-2021-09-01",
)

createSC(
    name="d010",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Invasive (category D2)", lang="en"),
    definition=Literal("Self-sustaining population outside of captivity or cultivation, with individuals surviving and reproducing a significant distance from the original point of introduction.", lang="en"),
    comments=Literal("The population is maintained by reproduction, is spreading, and its progeny are also reproducing and spreading. See also \"category D2\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d010",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d010-2021-09-01",
)

createSC(
    name="d011",
    namespace=DWCDOE,
    graph=g,
    pref_label=Literal("Widespread invasive (category E)", lang="en"),
    definition=Literal("Fully invasive species, with individuals dispersing, surviving and reproducing at multiple sites across a spectrum of habitats and geographic range.", lang="en"),
    comments=Literal("This term is only used for those invasives with the highest degree of encroachment. See also \"category E\" in Blackburn et al. 2011 ([https://doi.org/10.1016/j.tree.2011.03.023](https://doi.org/10.1016/j.tree.2011.03.023)).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcdoe/values/d011",
    references_s="http://rs.tdwg.org/dwcdoe/values/version/d011-2021-09-01",
)

createSC(
    name="e001",
    namespace=DWCEM,
    graph=g,
    pref_label=Literal("Native (indigenous)", lang="en"),
    definition=Literal("A taxon occurring within its natural range.", lang="en"),
    comments=Literal("What is considered native to an area varies with the biogeographic history of an area and the local interpretation of what is a \"natural range\".", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcem/values/e001",
    references_s="http://rs.tdwg.org/dwcem/values/version/e001-2021-09-01",
)

createSC(
    name="e002",
    namespace=DWCEM,
    graph=g,
    pref_label=Literal("Native (reintroduced)", lang="en"),
    definition=Literal("A taxon re-established by direct introduction by humans into an area that was once part of its natural range, but from where it had become extinct.", lang="en"),
    comments=Literal("Where a taxon has become extirpated from an area where it had naturally occurred it may be returned to that area deliberately with the intention of re-establishing it.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcem/values/e002",
    references_s="http://rs.tdwg.org/dwcem/values/version/e002-2025-06-12",
)

createSC(
    name="e003",
    namespace=DWCEM,
    graph=g,
    pref_label=Literal("Introduced (alien, exotic, non-native, nonindigenous)", lang="en"),
    definition=Literal("Establishment of a taxon by human agency into an area that is not part of its natural range.", lang="en"),
    comments=Literal("Organisms can be introduced to novel areas and habitats by human activity, either on purpose or by accident. Humans can also inadvertently create corridors that break down natural barriers to dispersal and allow organisms to spread beyond their natural range.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcem/values/e003",
    references_s="http://rs.tdwg.org/dwcem/values/version/e003-2021-09-01",
)

createSC(
    name="e004",
    namespace=DWCEM,
    graph=g,
    pref_label=Literal("Introduced (assisted colonisation)", lang="en"),
    definition=Literal("Establishment of a taxon specifically with the intention of creating a self-sustaining wild population in an area that is not part of the taxon's natural range.", lang="en"),
    comments=Literal("In the event of environmental change and habitat destruction a conservation option is to introduce a taxon into an area it did not naturally occur.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcem/values/e004",
    references_s="http://rs.tdwg.org/dwcem/values/version/e004-2021-09-01",
)

createSC(
    name="e005",
    namespace=DWCEM,
    graph=g,
    pref_label=Literal("Vagrant (casual)", lang="en"),
    definition=Literal("The temporary occurrence of a taxon far outside its natural or migratory range.", lang="en"),
    comments=Literal("Natural events and human activity can disperse organisms unpredictably into places where they may stay or survive for a period.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcem/values/e005",
    references_s="http://rs.tdwg.org/dwcem/values/version/e005-2020-10-13",
)

createSC(
    name="e006",
    namespace=DWCEM,
    graph=g,
    pref_label=Literal("Uncertain (unknown, cryptogenic)", lang="en"),
    definition=Literal("The origin of the occurrence of the taxon in an area is obscure.", lang="en"),
    comments=Literal("When there is a lack of fossil or historical evidence for the occurrence of a taxon in an area it can be impossible to know if the taxon is new to the area or native.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcem/values/e006",
    references_s="http://rs.tdwg.org/dwcem/values/version/e006-2021-09-01",
)

createSC(
    name="e007",
    namespace=DWCEM,
    graph=g,
    pref_label=Literal("Native (endemic)", lang="en"),
    definition=Literal("A taxon with a natural distribution restricted to a single geographical area.", lang="en"),
    comments=Literal("The term endemic is a subcategory of native and relates to geography, such as \"areas of endemism\", bioregions, and sometimes administrative boundaries. While a native taxon can naturally occur in several geographical areas an endemic taxon only occurs in one. In Darwin Core terms this would mean, \"A dwc:Organism referred to is recognized as a member of a dwc:Taxon endemic to the dcterms:Location at the time of the dwc:Occurrence.\"", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcem/values/e007",
    references_s="http://rs.tdwg.org/dwcem/values/version/e007-2025-06-12",
)

createSC(
    name="p001",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Biological Control", lang="en"),
    definition=Literal("Organisms occuring in an area because they were introduced for the purpose of biological control of another organism.", lang="en"),
    comments=Literal("Released intentionally into the (semi)natural environment with the purpose of controlling the population(s) of one or more organisms. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p001",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p001-2021-09-01",
)

createSC(
    name="p002",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Erosion Control", lang="en"),
    definition=Literal("Organisms introduced for the purpose of erosion control/dune stabilization (windbreaks, hedges, etc.).", lang="en"),
    comments=Literal("Probably only applicable to plants. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p002",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p002-2021-09-01",
)

createSC(
    name="p003",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Fishery In The Wild", lang="en"),
    definition=Literal("Fish stocked into the wild either to create a fishery or for recreational angling.", lang="en"),
    comments=Literal("Largely applicable to freshwater and anadromous fish. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p003",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p003-2021-09-01",
)

createSC(
    name="p004",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Hunting", lang="en"),
    definition=Literal("Animals stocked into the wild specifically with the intention that they would be hunted for sport.", lang="en"),
    comments=Literal("Largely applicable to terrestrial vertebrates. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p004",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p004-2021-09-01",
)

createSC(
    name="p005",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Landscape Improvement", lang="en"),
    definition=Literal("Landscape/flora/fauna \"improvement\" in the wild.", lang="en"),
    comments=Literal("\"Improvement\" in this context is intended for introductions for the purpose of aesthetic enhancement of the landscape, as opposed to practical introductions for the purpose of erosion control, agriculture, forestry etc. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p005",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p005-2021-09-01",
)

createSC(
    name="p006",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Conservation Or Wildlife Management", lang="en"),
    definition=Literal("Organisms introduced for conservation purposes or wildlife management.", lang="en"),
    comments=Literal("The organism was released with the intention of improving the conservation status of the species or the conservation status other species in the habitat. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p006",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p006-2021-09-01",
)

createSC(
    name="p007",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Released For Use", lang="en"),
    definition=Literal("Release in nature for use (other than above, e.g., fur, transport, medical use).", lang="en"),
    comments=Literal("This term refers to organisms intentionally and directly released into the wild to serve a specific purpose. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p007",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p007-2021-09-01",
)

createSC(
    name="p008",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Other Intentional Release", lang="en"),
    definition=Literal("A catch-all term for intentional releases not for human use that are not covered by other more specific terms.", lang="en"),
    comments=Literal("Compare with \"other escape from confinement\". See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p045"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p008",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p008-2021-09-01",
)

createSC(
    name="p009",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Agriculture (Including Biofuel Feedstocks)", lang="en"),
    definition=Literal("Plants grown with the intention of harvesting.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p009",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p009-2021-09-01",
)

createSC(
    name="p010",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Aquaculture/Mariculture", lang="en"),
    definition=Literal("The analog of agriculture and farmed animals, specifically related to aquatic organisms.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p010",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p010-2021-09-01",
)

createSC(
    name="p011",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Botanic Garden/Zoo/Aquaria (Excluding Domestic Aquaria)", lang="en"),
    definition=Literal("Organisms in public collections of plants and/or animals.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p011",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p011-2021-09-01",
)

createSC(
    name="p012",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Pet/Aquarium/Terrarium Species (Including Live Food For Such Species)", lang="en"),
    definition=Literal("Privately kept animals.", lang="en"),
    comments=Literal("Animals kept for hunting, such as falcons and ferrets, SHOULD be included here, not under the hunting term. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p012",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p012-2021-09-01",
)

createSC(
    name="p013",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Farmed Animals (Including Animals Left Under Limited Control)", lang="en"),
    definition=Literal("Animals cared for and bred with the specific intention of using their products, such as meat and milk.", lang="en"),
    comments=Literal("Farmed animals are generally kept in a defined area, such as a fields. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p013",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p013-2021-09-01",
)

createSC(
    name="p014",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Forestry (Including Reforestation)", lang="en"),
    definition=Literal("Trees specifically introduced to provide timber and other forestry products.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p014",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p014-2021-09-01",
)

createSC(
    name="p015",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Fur Farms", lang="en"),
    definition=Literal("Organisms escaped from a fur farm, including unauthorised releases.", lang="en"),
    comments=Literal("Probably only applicable to vertebrates raised for their pelts and skins. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p015",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p015-2021-09-01",
)

createSC(
    name="p016",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Horticulture", lang="en"),
    definition=Literal("Plants distributed by the ornamental and decorative plants industry.", lang="en"),
    comments=Literal("This term excludes plants and other organisms from aquaria and terrariums, which SHOULD be classified under the pet/aquarium/terrarium term. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p016",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p016-2021-09-01",
)

createSC(
    name="p017",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Ornamental Purpose Other Than Horticulture", lang="en"),
    definition=Literal("Ornamental plants introduced through pathways other than the horticultural industry.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p017",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p017-2021-09-01",
)

createSC(
    name="p018",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Research And Ex-Situ Breeding (In Facilities)", lang="en"),
    definition=Literal("Plants and animals introduced for the purpose of breeding or scientific and medical research, including science education.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p018",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p018-2021-09-01",
)

createSC(
    name="p019",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Live Food And Live Bait", lang="en"),
    definition=Literal("Live food imported for human consumption or live bait, such as shellfish and snails.", lang="en"),
    comments=Literal("Live food, such as mealworms, for the organisms kept as pets should be classified under the pet term. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p019",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p019-2021-09-01",
)

createSC(
    name="p020",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Other Escape From Confinement", lang="en"),
    definition=Literal("Organisms brought into an area with the intention of keeping them in captivity permanently, but that have subsequently escaped.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p020",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p020-2021-09-01",
)

createSC(
    name="p021",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Contaminant Nursery Material", lang="en"),
    definition=Literal("Organisms transported into an area together with plant material.", lang="en"),
    comments=Literal("These may be other plants, diseases, fungi and animals. They may be attached to the plant or within the soil. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p021",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p021-2021-09-01",
)

createSC(
    name="p022",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Contaminated Bait", lang="en"),
    definition=Literal("Contaminants, pathogens and parasites transported with live, frozen or preserved bait used to catch fish or other organisms.", lang="en"),
    comments=Literal("Typical examples include crustaceans, cephalopods and molluscs. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p022",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p022-2021-09-01",
)

createSC(
    name="p023",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Food Contaminant (Including Of Live Food)", lang="en"),
    definition=Literal("Foods for human consumption, whether they are transported live or dead.", lang="en"),
    comments=Literal("This term includes unintentional introduction of contaminants such as diseases on those foods and in the case of plants, should include seeds. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p023",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p023-2021-09-01",
)

createSC(
    name="p024",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Contaminant On Animals (Except Parasites, Organisms Transported By Host/Vector)", lang="en"),
    definition=Literal("Contaminants carried either on or in the body of transported animals.", lang="en"),
    comments=Literal("This term excludes parasites and pathogens, which SHOULD be classified under their own specific term (\"parasites on animals\"). Transported animals carry other organisms in their coats, in their guts and in soil on their hooves and feet. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p024",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p024-2021-09-01",
)

createSC(
    name="p025",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Parasites On Animals (Including Organisms Transported By Host And Vector)", lang="en"),
    definition=Literal("Parasitic and pathogenic organisms transported with their host or vector animal.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p025",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p025-2021-09-01",
)

createSC(
    name="p026",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Contaminant On Plants (Except Parasites, Species Transported By Host/Vector)", lang="en"),
    definition=Literal("Organisms transported on plant material.", lang="en"),
    comments=Literal("This term excludes organisms carried on contaminant nursery material, seed contaminants, and the material from the timber trade, which SHOULD be classified under their own pathway terms. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p026",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p026-2021-09-01",
)

createSC(
    name="p027",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Parasites On Plants (Including Species Transported By Host And Vector)", lang="en"),
    definition=Literal("Parasitic and pathogenic organisms transported with their host or vector plant.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p027",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p027-2021-09-01",
)

createSC(
    name="p028",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Seed Contaminant", lang="en"),
    definition=Literal("Organisms contaminating transported seeds.", lang="en"),
    comments=Literal("These may be parasites or pathogens of seeds or species that eat seeds, whether intended to be transported or not. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p028",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p028-2021-09-01",
)

createSC(
    name="p029",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Timber Trade", lang="en"),
    definition=Literal("Contaminants on unprocessed timber, processed wood and wood-derived products.", lang="en"),
    comments=Literal("This term excludes packing material and habitat material made from wood, which SHOULD be included under their own terms (\"packing material\" and \"transportation of habitat material\"). Examples include wooden furniture, saw dust and fire wood. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p029",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p029-2021-09-01",
)

createSC(
    name="p030",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Transportation Of Habitat Material (Soil, Vegetation, Wood, Etc.)", lang="en"),
    definition=Literal("Organisms transported with their habitat material to a new location.", lang="en"),
    comments=Literal("Examples include materials such as soil, vegetation, straw and wood chips. Unless these materials are sterilised the organisms can be transported with their habitat to a new location. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p047"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p030",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p030-2021-09-01",
)


createSC(
    name="p031",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Angling/Fishing Equipment", lang="en"),
    definition=Literal("Aquatic organisms moved between sites on equipment of recreational anglers and professional fishermen.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p031",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p031-2021-09-01",
)


createSC(
    name="p032",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Container/Bulk", lang="en"),
    definition=Literal("Stowaways transported in or on cargo containers or bulk cargo units.", lang="en"),
    comments=Literal("The difference between this category and others, such as \"hitchhikers on ship/boat\", is that the organism embarked and disembarked from the container rather than the ship. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p032",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p032-2021-09-01",
)

createSC(
    name="p033",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Hitchhikers In Or On Airplane", lang="en"),
    definition=Literal("Organisms that enter airplanes or other aircraft, such as helicopters, and are transported by them to another location.", lang="en"),
    comments=Literal("This term does not apply to organisms that embarked in containers that were subsequently loaded onto an aircraft. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p033",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p033-2021-09-01",
)

createSC(
    name="p034",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Hitchhikers On Ship/Boat (Excluding Ballast Water And Hull Fouling)", lang="en"),
    definition=Literal("Organisms that enter directly onto boats or ships and are transported by them to another location.", lang="en"),
    comments=Literal("This term does not apply to organisms that embarked in containers that are subsequently loaded onto the ship, nor to contaminants of products loaded onto the ship. The term is intended for organisms that directly interact with the boat or ship. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p034",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p034-2021-09-01",
)

createSC(
    name="p035",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Machinery/Equipment", lang="en"),
    definition=Literal("Organisms carried on the surfaces of or within heavy machinery and equipment.", lang="en"),
    comments=Literal("This includes military equipment, farm machinery and manufacturing equipment. This term does not include products carried by vehicles. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p035",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p035-2021-09-01",
)


createSC(
    name="p036",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("People And Their Luggage/Equipment (In Particular Tourism)", lang="en"),
    definition=Literal("Organisms transported on people and/or their personal luggage.", lang="en"),
    comments=Literal("This term excludes recreational angling equipment, which SHOULD be classified under its own term (\"angling/fishing equipment\"). Examples include organisms transported by tourists. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p036",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p036-2021-09-01",
)

createSC(
    name="p037",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Organic Packing Material, In Particular Wood Packaging", lang="en"),
    definition=Literal("Organic material, particularly unprocessed plant material that is used to pack transported goods.", lang="en"),
    comments=Literal("Examples include woodern pallets, boxes, bags and baskets. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p037",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p037-2021-09-01",
)

createSC(
    name="p038",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Ship/Boat Ballast Water", lang="en"),
    definition=Literal("Organisms transported within the water pumped into boats and ships to provide ballast.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p038",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p037-2021-09-01",
)

createSC(
    name="p039",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Ship/Boat Hull Fouling", lang="en"),
    definition=Literal("Organisms that attach themselves to the subsurface hull of boats and ships.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p039",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p039-2021-09-01",
)

createSC(
    name="p040",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Vehicles (Car, Train, Etc.)", lang="en"),
    definition=Literal("Other vehicle hitchhikers that have been unintentionally dispersed, but are not covered by other terms.", lang="en"),
    comments=Literal("These organisms may be carried on or within the vehicle. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p040",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p040-2021-09-01",
)

createSC(
    name="p041",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Other Means Of Transport", lang="en"),
    definition=Literal("A catch-all term for any transport related dispersal that is not covered in other terms.", lang="en"),
    comments=Literal("Examples include fouling from offshore oil and gas platforms, offshore renewable energy sites (such as wind farms, pipelines, cable transport, etc.). See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p048"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p041",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p041-2021-09-01",
)

createSC(
    name="p042",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Interconnected Waterways/Basins/Seas", lang="en"),
    definition=Literal("Organisms that dispersed through artificial waterways created to connect previosuly unconnected water bodies.", lang="en"),
    comments=Literal("Organisms transported along these corridors in ballast or as hull fouling SHOULD be categorised under the \"ship/boat ballast water\" or \"ship/boat hull fouling\" terms. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p049"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p042",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p042-2021-09-01",
)

createSC(
    name="p043",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Tunnels And Land Bridges", lang="en"),
    definition=Literal("Unintentional dispersal by organisms using artificial tunnels, bridges, roads and railways.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p049"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p043",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p043-2021-09-01",
)

createSC(
    name="p044",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Natural Dispersal Across Borders Of Invasive Alien Organisms", lang="en"),
    definition=Literal("Organisms transported and released by humans in a (semi)natural environment with the intention that they should live there without further human aid.", lang="en"),
    comments=Literal("Dispersal of organisms to new regions by natural dispersal from regions in which they are alien. These are alien species that have previously been introduced through one of these pathways: release in nature, escape from confinement, transport-contaminant, transport-stowaway, or corridor. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p050"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p044",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p044-2021-09-01",
)

createSC(
    name="p045",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Release In Nature", lang="en"),
    definition=Literal("Organisms transported and released by humans in a (semi)natural environment with the intention that they should live there without further human aid.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p051"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p045",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p045-2021-09-01",
)

createSC(
    name="p046",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Escape From Confinement", lang="en"),
    definition=Literal("Organisms intentionally transported by humans and intended to be kept in captivity or cultivation, but having inadvertently escaped from human control.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p051"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p046",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p046-2021-09-01",
)

createSC(
    name="p047",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Transport-Contaminant", lang="en"),
    definition=Literal("An umbrella term for all species transported as contaminants in other products.", lang="en"),
    comments=Literal("An alien species is a contaminant if it had a trophic or biotic relationship to organisms or items being transported and was to some extent dependent on them for survival. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p052"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p047",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p047-2021-09-01",
)

createSC(
    name="p048",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Transport-Stowaway", lang="en"),
    definition=Literal("An umbrella term for all species transported by riding on forms of transport where the organism has a direct interaction with the transport and is not merely carried as part of, or a contaminant of cargo.", lang="en"),
    comments=Literal("A stowaway has no trophic or biotic relationship to the organisms or items being transported. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p052"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p048",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p048-2021-09-01",
)

createSC(
    name="p049",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Corridor", lang="en"),
    definition=Literal("Infrastructure, such as bridges, tunnels and canals have removed natural barriers to dispersal and allowed a species to move into a novel location.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p053"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p049",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p049-2021-09-01",
)

createSC(
    name="p050",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Unaided", lang="en"),
    definition=Literal("Organisms that spread by natural dispersal, without action or assistance by humans, from regions in which they are also alien.", lang="en"),
    comments=Literal("The term refers to secondary dispersal from an area where the taxon is also alien. See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    broader=URIRef("http://rs.tdwg.org/dwcpw/values/p053"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p051",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p051-2021-09-01",
)

createSC(
    name="p051",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Intentional", lang="en"),
    definition=Literal("Organisms were brought to new area with the specific intention of keeping them alive in the new region, regardless of whether they were intended to be cultivated or released into the wild.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p051",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p051-2021-09-01",
)

createSC(
    name="p052",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Unintentional", lang="en"),
    definition=Literal("The organism was unintentionally brought to a new region.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p052",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p052-2021-09-01",
)

createSC(
    name="p053",
    namespace=DWCPW,
    graph=g,
    pref_label=Literal("Corridor and Dispersal", lang="en"),
    definition=Literal("Organisms dispersed naturally, even if that dispersal was aided by changes in the landscape created by humans.", lang="en"),
    comments=Literal("See also Harrower et al. 2017: [http://nora.nerc.ac.uk/id/eprint/519129](http://nora.nerc.ac.uk/id/eprint/519129).", lang="en"),
    version_of_s="http://rs.tdwg.org/dwcpw/values/p053",
    references_s="http://rs.tdwg.org/dwcpw/values/version/p053-2021-09-01",
)

#####################################################################################################
# BEGIN AXIOMS
#####################################################################################################

# NOTE: Can a dwc:Event be a eco:Survey?
declare_disjoint(
    classes=[CHRONO["ChronometricAge"], DCTERMS["Agent"], DCTERMS["Location"], AC["Media"], DWC["Assertion"], DWC["Event"], DWC["GeologicalContext"], DWC["MaterialEntity"], DWC["NucleotideAnalysis"], DWC["NucleotideSequence"], DWC["Occurrence"], DWC["Organism"], DWC["OrganismInteraction"], DWC["Protocol"], DWC["ResourceRelationship"], DWC["UsagePolicy"], ECO["Survey"], ECO["SurveyTarget"]],
    graph=g
)

from rdflib.collection import Collection

# NOTE: Try a property chain
# For a test case: dwcdp:basedOn o dwcdp:isPartOf -> dwcdp:basedOn
prop_chain = BNode()
Collection(g, prop_chain, [DWCDP["basedOn"], DWCDP["isPartOf"]])
g.add((DWCDP["basedOn"], OWL.propertyChainAxiom, prop_chain))


#####################################################################################################
# BEGIN OBJECT PROPERTY DEFINITIONS
#####################################################################################################

# NOTE: REVOIR COMMENTS. THIS DOCUMENT? ALSO, ACCEPT BOTH A STRING OR A URI?
createDP(
    name="rights",
    namespace=DC,
    graph=g,
    domains=DWC["UsagePolicy"],
    ranges=[
        XSD["anyURI"],
        XSD["string"],
    ],
    pref_label=Literal("Rights (DC)"),
    definition=Literal("Information about rights held in and over the resource. A full-text, readable copyright statement, as rquired by the national legislation of the copyright holder. On collections, this applies to all contained objects, unless the object itself has a different statement. Do not place just the name of the copyright holder(s) here! That belongs in a list in the [xmpRights:Owner] field, which should be supplied only if [dc:rights] is not `Public Domain`, which is appropriate only if the resource is known to be not under copyright. See also the entry for [dcterms:rights] in this document and see the DMCI FAQ on [dc:] and [dcterms:] Namespaces for discussion of the rationale for terms in two namespaces. Normal practice is to use the same Label if both are provided. Labels have no effect on information discovery and are only suggestions."),
    examples=[
        Literal("Copyright 2014 Ron Thomas"),
        Literal("http://creativecommons.org/licenses/by/3.0/legalcode"),
    ],
    version_of_s="http://purl.org/dc/elements/1.1/rights",
)

# WARN: Verify domain
# BUG: dc:source is source (heh) of inconsistency
createDP(
    name="source",
    namespace=DC,
    graph=g,
    domains=OWL["Thing"],
    # domains=[DWC["UsagePolicy"]],
    ranges=RDFS["Literal"],
    # ranges=[XSD["anyURI"], XSD["string"]],
    pref_label=Literal("Source (DC)"),
    definition=Literal("A related resource from which the described resource is derived", lang="en"),
    comments=Literal("The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system.", lang="en"),
    version_of_s="http://purl.org/dc/elements/1.1/source",
)

#############################################################################

createOP(
    name="rights",
    namespace=DCTERMS,
    graph=g,
    domains=DWC["UsagePolicy"],
    ranges=XSD["anyURI"],
    pref_label=Literal("Rights (DCTERMS)"),
    definition=Literal("Information about rights held in and over the resource."),
    comments=Literal("Typically, rights information includes a statement about various property rights associated with the resource, including intellectual property rights. Recommended practice is to refer to a rights statement with a URI. If this is not possible or feasible, a literal value (name, label, or short text) may be provided."),
    version_of_s="http://purl.org/dc/terms/rights",
)

createOP(
    name="rightsHolder",
    namespace=DCTERMS,
    graph=g,
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Rights Holder"),
    definition=Literal("A person or organization owning or managing rights over the resource."),
    comments=Literal("Recommended practice is to refer to the rights holder with a URI. If this is not possible or feasible, a literal value that identifies the rights holder may be provided."),
    version_of_s="http://purl.org/dc/terms/rightsHolder",
)

createOP(
    name="spatial",
    namespace=DCTERMS,
    graph=g,
    ranges=DCTERMS["Location"],
    pref_label=Literal("Spatial Coverage"),
    definition=Literal("Spatial characteristics of the resource.", lang="en"),
    version_of_s="http://purl.org/dc/terms/spatial",
)

createOP(
    name="type",
    namespace=DCTERMS,
    graph=g,
    pref_label=Literal("Type"),
    definition=Literal("The nature or genre of the resource."),
    comments=Literal("Recommended practice is to use a controlled vocabulary such as the DCMI Type Vocabulary [DCMI-TYPE](http://dublincore.org/documents/dcmi-type-vocabulary/). To describe the file format, physical medium, or dimensions of the resource, use the property Format."),
    version_of_s="http://purl.org/dc/terms/type",
)

#############################################################################

# BUG: To avoid inconsistencies, changed range list
createOP(
    name="assertionTypeIRI",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Assertion"],
    pref_label=Literal("Assertion Type (IRI)"),
    definition=Literal("An IRI of a controlled vocabulary value for a type of [dwc:Assertion].", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for a term in a controlled vocabulary.", lang="en"),
    version_of_s="http://example.com/term-pending/dwciri/assertionTypeIRI",
)

# NOTE: I added the example IRI
createOP(
    name="assertionValueIRI",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Assertion"],
    pref_label=Literal("Assertion Value (IRI)"),
    definition=Literal("An IRI of the controlled vocabulary value for a value of a [dwc:Assertion].", lang="en"),
    examples=[
        URIRef("http://purl.obolibrary.org/obo/OBA_VT0000047"),
    ],
    version_of_s="http://example.com/term-pending/dwciri/assertionValueIRI",
)

# WARN: Comment in JSON file says dwc:SurveyTargetType?
createOP(
    name="surveyTargetTypeIRI",
    namespace=DWCIRI,
    graph=g,
    domains=ECO["SurveyTarget"],
    pref_label=Literal("Survey Target Type IRI"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [eco:SurveyTargetType] is given.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for a term in a controlled vocabulary.", lang="en"),
    subproperty_list=[DCTERMS["type"]],
    version_of_s="http://purl.org/dc/terms/type",
)

createOP(
    name="behavior",
    namespace=DWCIRI,
    graph=g,
    domains=[DWC["OccurrenceAssertion"], DWC["OrganismAssertion"]],
    pref_label=Literal("Behavior (IRI)"),
    definition=Literal("A description of the behavior shown by the subject at the time the dwc:Occurrence was recorded.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/behavior",
    references_s="http://rs.tdwg.org/dwc/iri/version/behavior-2025-07-10",
)

createOP(
    name="caste",
    namespace=DWCIRI,
    graph=g,
    domains=[DWC["OccurrenceAssertion"], DWC["OrganismAssertion"]],
    pref_label=Literal("Caste (IRI)"),
    definition=Literal("Categorisation of individuals for eusocial species (including some mammals and arthropods).", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary that aligns best with the dwc:Taxon. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/caste",
    references_s="http://rs.tdwg.org/dwc/iri/version/caste-2025-07-10",
)

# WARN: Revoir domain
createOP(
    name="dataGeneralizations",
    namespace=DWCIRI,
    graph=g,
    pref_label=Literal("Data Generalizations (IRI)"),
    definition=Literal("Actions taken to make the shared data less specific or complete than in its original form. Suggests that alternative data of higher quality may be available on request.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/dataGeneralizations",
    references_s="http://rs.tdwg.org/dwc/iri/version/dataGeneralizations-2025-07-10",
)

# WARN: Verify if actually about dwc:Occurrence
createOP(
    name="degreeOfEstablishment",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Occurrence"],
    ranges=DWC["DegreeOfEstablishment"],
    pref_label=Literal("Degree Of Establishment (IRI)"),
    definition=Literal("The degree to which a dwc:Organism survives, reproduces, and expands its range at the given place and time.", lang="en"),
    comments=Literal("Recommended best practice is to use IRIs from the controlled vocabulary designated for use with this term, listed at [http://rs.tdwg.org/dwc/doc/doe/](http://rs.tdwg.org/dwc/doc/doe/). For details, refer to [https://doi.org/10.3897/biss.3.38084](https://doi.org/10.3897/biss.3.38084). Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    examples=[
        URIRef("http://rs.tdwg.org/dwcdoe/values/d003"),
        URIRef("http://rs.tdwg.org/dwcdoe/values/d005"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/iri/degreeOfEstablishment",
    references_s="http://rs.tdwg.org/dwc/iri/version/degreeOfEstablishment-2025-07-10",
)

# WARN: Revoir domain
createOP(
    name="discipline",
    namespace=DWCIRI,
    graph=g,
    pref_label=Literal("Discipline (IRI)"),
    definition=Literal("The primary branch or branches of knowledge represented by the record.", lang="en"),
    comments=Literal("This term can be used to classify records according to branches of knowledge. Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/discipline",
    references_s="http://rs.tdwg.org/dwc/iri/version/discipline-2025-06-12",
)

createOP(
    name="disposition",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["MaterialEntity"],
    pref_label=Literal("Disposition (IRI)"),
    definition=Literal("The current state of a specimen with respect to the collection identified in dwc:collectionCode or dwc:collectionID.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/disposition",
    references_s="http://rs.tdwg.org/dwc/iri/version/disposition-2025-07-10",
)

createOP(
    name="earliestGeochronologicalEra",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["MaterialEntity"],
    pref_label=Literal("Earliest Geochronological Era"),
    definition=Literal("Use to link a dwc:GeologicalContext instance to chronostratigraphic time periods at the lowest possible level in a standardized hierarchy. Use this property to point to the earliest possible geological time period from which the dwc:MaterialEntity was collected.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI from a controlled vocabulary. A \"convenience property\" that replaces Darwin Core literal-value terms related to geological context. See Section 2.7.6 of the Darwin Core RDF Guide for details.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/earliestGeochronologicalEra",
    references_s="http://rs.tdwg.org/dwc/iri/version/earliestGeochronologicalEra-2023-09-13",
)

createOP(
    name="establishmentMeans",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Occurrence"],
    ranges=DWC["EstablishmentMeans"],
    pref_label=Literal("Establishment Means (IRI)"),
    definition=Literal("Statement about whether a dwc:Organism has been introduced to a given place and time through the direct or indirect activity of modern humans.", lang="en"),
    comments=Literal("Recommended best practice is to use IRIs from the controlled vocabulary designated for use with this term, listed at [http://rs.tdwg.org/dwc/doc/em/](http://rs.tdwg.org/dwc/doc/em/). For details, refer to [https://doi.org/10.3897/biss.3.38084](https://doi.org/10.3897/biss.3.38084). Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    examples=[
        URIRef("http://rs.tdwg.org/dwcem/values/e001"),
        URIRef("http://rs.tdwg.org/dwcem/values/e005"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/iri/establishmentMeans",
    references_s="http://rs.tdwg.org/dwc/iri/version/establishmentMeans-2025-07-10",
)

createOP(
    name="eventType",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Event"],
    pref_label=Literal("Event Type (IRI)"),
    definition=Literal("The nature of the dwc:Event.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Regardless of the dwc:eventType, the interval of the dwc:Event can be captured in dwc:eventDate. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/eventType",
    references_s="http://rs.tdwg.org/dwc/iri/version/eventType-2025-07-10",
)

createOP(
    name="fieldNotes",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Event"],
    pref_label=Literal("Field Notes (IRI)"),
    definition=Literal("One of a) an indicator of the existence of, b) a reference to (publication, URI), or c) the text of notes taken in the field about the dwc:Event.", lang="en"),
    comments=Literal("The subject is a dwc:Event instance and the object is a (possibly IRI-identified) resource that is the field notes.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/fieldNotes",
    references_s="http://rs.tdwg.org/dwc/iri/version/fieldNotes-2023-06-28",
)

createOP(
    name="fieldNumber",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Event"],
    pref_label=Literal("Field Number (IRI)"),
    definition=Literal("An identifier given to the event in the field. Often serves as a link between field notes and the dwc:Event.", lang="en"),
    comments=Literal("The subject is a (possibly IRI-identified) resource that is the field notes and the object is a dwc:Event instance.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/fieldNumber",
    references_s="http://rs.tdwg.org/dwc/iri/version/fieldNumber-2023-06-28",
)

createOP(
    name="footprintWKT",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Footprint WKT (IRI)"),
    definition=Literal("A Well-Known Text (WKT) representation of the shape (footprint, geometry) that defines the dcterms:Location. A dcterms:Location may have both a point-radius representation (see dwc:decimalLatitude) and a footprint representation, and they may differ from each other.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/footprintWKT",
    references_s="http://rs.tdwg.org/dwc/iri/version/footprintWKT-2025-07-10",
)

createOP(
    name="geodeticDatum",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Geodetic Datum (IRI)"),
    definition=Literal("The ellipsoid, geodetic datum, or spatial reference system (SRS) upon which the geographic coordinates given in dwc:decimalLatitude and dwc:decimalLongitude are based.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for the EPSG code of the SRS, if known. Otherwise use a controlled vocabulary for the name or code of the geodetic datum, if known. Otherwise use a controlled vocabulary for the name or code of the ellipsoid, if known. If none of these is known, use an IRI corresponding to the value not recorded.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/geodeticDatum",
    references_s="http://rs.tdwg.org/dwc/iri/version/geodeticDatum-2025-06-12",
)

createOP(
    name="georeferencedBy",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Georeferenced By (IRI)"),
    definition=Literal("A person, group, or organization who determined the georeference (spatial representation) for the dcterms:Location.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/georeferencedBy",
    references_s="http://rs.tdwg.org/dwc/iri/version/georeferencedBy-2025-07-10",
)

createOP(
    name="georeferenceProtocol",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Georeference Protocol (IRI)"),
    definition=Literal("A description or reference to the methods used to determine the spatial footprint, coordinates, and uncertainties.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/georeferenceProtocol",
    references_s="http://rs.tdwg.org/dwc/iri/version/georeferenceProtocol-2025-07-10",
)

createOP(
    name="georeferenceSources",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Georeference Sources (IRI)"),
    definition=Literal("A map, gazetteer, or other resource used to georeference the dcterms:Location.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/georeferenceSources",
    references_s="http://rs.tdwg.org/dwc/iri/version/georeferenceSources-2025-07-10",
)

createOP(
    name="georeferenceVerificationStatus",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Georeference Verification Status (IRI)"),
    definition=Literal("A categorical description of the extent to which the georeference has been verified to represent the best possible spatial description for the dcterms:Location of the dwc:Occurrence.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/georeferenceVerificationStatus",
    references_s="http://rs.tdwg.org/dwc/iri/version/georeferenceVerificationStatus-2025-07-10",
)

createOP(
    name="habitat",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Event"],
    pref_label=Literal("Habitat (IRI)"),
    definition=Literal("A category or description of the habitat in which the dwc:Event occurred.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/habitat",
    references_s="http://rs.tdwg.org/dwc/iri/version/habitat-2025-07-10",
)

createOP(
    name="identifiedBy",
    namespace=DWCIRI,
    graph=g,
    domains=[
        DWC["Identification"],
        DWC["Occurrence"],
        ECO["Survey"],
    ],
    pref_label=Literal("Identified By (IRI)"),
    definition=Literal("A person, group, or organization who assigned the dwc:Taxon to the subject.", lang="en"),
    comments=Literal("When used in the context of an Event (such as in the Humboldt Extension), the subject consists of all of the dwc:Organisms related to the Event. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/identifiedBy",
    references_s="http://rs.tdwg.org/dwc/iri/version/identifiedBy-2025-07-10",
)

createOP(
    name="locationAccordingTo",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Location According To (IRI)"),
    definition=Literal("Information about the source of this dcterms:Location information. Could be a publication (gazetteer), institution, or team of individuals.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/locationAccordingTo",
    references_s="http://rs.tdwg.org/dwc/iri/version/locationAccordingTo-2025-07-10",
)

createOP(
    name="occurrenceStatus",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Occurrence"],
    pref_label=Literal("Occurrence Status (IRI)"),
    definition=Literal("A statement about the presence or absence of a dwc:Taxon at a dcterms:Location.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/occurrenceStatus",
    references_s="http://rs.tdwg.org/dwc/iri/version/occurrenceStatus-2025-07-10",
)

createOP(
    name="pathway",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Occurrence"],
    ranges=DWC["Pathway"],
    pref_label=Literal("Pathway (IRI)"),
    definition=Literal("The process by which a dwc:Organism came to be in a given place at a given time.", lang="en"),
    comments=Literal("Recommended best practice is to use IRIs from the controlled vocabulary designated for use with this term, listed at [http://rs.tdwg.org/dwc/doc/pw/](http://rs.tdwg.org/dwc/doc/pw/). For details, refer to [https://doi.org/10.3897/biss.3.38084](https://doi.org/10.3897/biss.3.38084). Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    examples=[
        URIRef("http://rs.tdwg.org/dwcpw/values/p002"),
        URIRef("http://rs.tdwg.org/dwcpw/values/p046"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/iri/pathway",
    references_s="http://rs.tdwg.org/dwc/iri/version/pathway-2025-07-10",
)

createOP(
    name="recordedBy",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Occurrence"],
    pref_label=Literal("Recorded By (IRI)"),
    definition=Literal("A person, group, or organization responsible for recording the original dwc:Occurrence.", lang="en"),
    comments=Literal("Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/recordedBy",
    references_s="http://rs.tdwg.org/dwc/iri/version/recordedBy-2025-07-10",
)

# WARN: Verify if actually about dwc:Occurrence
createOP(
    name="reproductiveCondition",
    namespace=DWCIRI,
    graph=g,
    domains=[
        DWC["OccurrenceAssertion"],
        DWC["OrganismAssertion"],
    ],
    pref_label=Literal("Reproductive Condition (IRI)"),
    definition=Literal("The reproductive condition of the biological individual(s) represented in the dwc:Occurrence.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/reproductiveCondition",
    references_s="http://rs.tdwg.org/dwc/iri/version/reproductiveCondition-2025-07-10",
)

createOP(
    name="samplingProtocol",
    namespace=DWCIRI,
    graph=g,
    domains=DWC["Event"],
    pref_label=Literal("Sampling Protocol (IRI)"),
    definition=Literal("The methods or protocols used during a dwc:Event, denoted by an IRI.", lang="en"),
    comments=Literal("Recommended best practice is describe a dwc:Event with no more than one sampling protocol. In the case of a summary dwc:Event in which a specific protocol can not be attributed to specific dwc:Occurrences, the recommended best practice is to repeat the property for each IRI that denotes a different sampling protocol that applies to the dwc:Occurrence.", lang="en"),
    examples=URIRef("https://doi.org/10.1111/j.1466-8238.2009.00467.x"),
    version_of_s="http://rs.tdwg.org/dwc/iri/samplingProtocol",
    references_s="http://rs.tdwg.org/dwc/iri/version/samplingProtocol-2023-06-28",
)

createOP(
    name="verbatimCoordinateSystem",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Verbatim Coordinate System (IRI)"),
    definition=Literal("The spatial coordinate system for the dwc:verbatimLatitude and dwc:verbatimLongitude or the dwc:verbatimCoordinates of the dcterms:Location.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/verbatimCoordinateSystem",
    references_s="http://rs.tdwg.org/dwc/iri/version/verbatimCoordinateSystem-2025-07-10",
)

createOP(
    name="verbatimSRS",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Verbatim SRS (IRI)"),
    definition=Literal("The ellipsoid, geodetic datum, or spatial reference system (SRS) upon which coordinates given in dwc:verbatimLatitude and dwc:verbatimLongitude, or dwc:verbatimCoordinates are based.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for the EPSG code of the SRS, if known. Otherwise use a controlled vocabulary IRI for the name or code of the geodetic datum, if known. Otherwise use a controlled vocabulary IRI for the name or code of the ellipsoid, if known. Otherwise use an IRI for the value corresponding to `not recorded`.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/verbatimSRS",
    references_s="http://rs.tdwg.org/dwc/iri/version/verbatimSRS-2025-06-12",
)

createOP(
    name="verticalDatum",
    namespace=DWCIRI,
    graph=g,
    domains=DCTERMS["Location"],
    pref_label=Literal("Vertical Datum (IRI)"),
    definition=Literal("The vertical datum used as the reference upon which the values in the elevation terms are based.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/verticalDatum",
    references_s="http://rs.tdwg.org/dwc/iri/version/verticalDatum-2025-07-10",
)

createOP(
    name="vitality",
    namespace=DWCIRI,
    graph=g,
    domains=[DWC["OccurrenceAssertion"], DWC["OrganismAssertion"]],
    pref_label=Literal("Vitality (IRI)"),
    definition=Literal("An indication of whether a dwc:Organism was alive or dead at the time of collection or observation.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Intended to be used with records having a dwc:basisOfRecord of `PreservedSpecimen`, `MaterialEntity`, `MaterialSample`, or `HumanObservation`. Terms in the dwciri: namespace are intended to be used in RDF with non-literal objects.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/iri/vitality",
    references_s="http://rs.tdwg.org/dwc/iri/version/vitality-2025-07-10",
)

#############################################################################

createOP(
    name="about",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Assertion"],
    ranges=[
        AC["Media"],
        CHRONO["ChronometricAge"],
        DWC["Event"],
        DWC["MaterialEntity"],
        DWC["NucleotideAnalysis"],
        DWC["Occurrence"],
        DWC["Organism"],
    ],
    pref_label=Literal("About"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Assertion] to the object it is about. This object can be a [chrono:ChronometricAge], [dwc:Event], [dwc:MaterialEntity], [dwc:Media], [dwc:NucleotideAnalysis], [dwc:Occurrence], [dwc:Organism].", lang="en"),
)

# NOTE: Consider the types of things a permit could allow for.
# For now, dwc:Event, dwc:NucleotideAnalysis and eco:Survey make sense.
createOP(
    name="allowsFor",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Permit"],
    ranges=[
        DWC["Event"],
        DWC["NucleotideAnalysis"],
        ECO["Survey"],
    ],
    pref_label=Literal("Allows For"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Permit] to the activities it allows for. These activities can be varied, and include [dwc:Event], [dwc:NucleotideAnalysis] and [eco:Survey].", lang="en"),
)

createOP(
    name="analysisOf",
    namespace=DWCDP,
    graph=g,
    domains=DWC["NucleotideAnalysis"],
    ranges=DWC["MaterialEntity"],
    pref_label=Literal("Analysis Of"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:NucleotideAnalysis] to the [dwc:MaterialEntity] of which it is an analysis of.", lang="en"),
)

createOP(
    name="assertedBy",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Assertion"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Asserted By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Assertion] to the [dcterms:Agent] that asserted it.", lang="en"),
)

createOP(
    name="authoredBy",
    namespace=DWCDP,
    graph=g,
    domains=DCTERMS["BibliographicResource"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Authored By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that authored it.", lang="en"),
)

# NOTE: Can an dwc:Identification be dwcdp:basedOn a dwc:NucleotideAnalysis? I thought it was logically possible through the dwc:NucleotideSequence it produced? If so, why not have the same for dwc:Event and dwc:Occurrence?
createOP(
    name="basedOn",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Identification"],
    ranges=[
        AC["Media"],
        DWC["MaterialEntity"],
        DWC["NucleotideAnalysis"],
        DWC["NucleotideSequence"],
        DWC["Occurrence"],
    ],
    pref_label=Literal("Based On"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Identification] to the entity on which it is based. These entities include [ac:Media], [dwc:MaterialEntity], [dwc:NucleotideAnalysis], [dwc:NucleotideSequence] and [dwc:Occurrence].", lang="en"),
)

createOP(
    name="commentedBy",
    namespace=DWCDP,
    graph=g,
    domains=AC["Media"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Commented By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Media] to the [dcterms:Agent] that commented it.", lang="en"),
)

createOP(
    name="conductedBy",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Event"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Conducted By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Event] to the [dcterms:Agent] that conducted it.", lang="en"),
)

createOP(
    name="datedMaterial",
    namespace=DWCDP,
    graph=g,
    domains=CHRONO["ChronometricAge"],
    ranges=DWC["MaterialEntity"],
    pref_label=Literal("Dated Material"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [chrono:ChronometricAge] to the [dwc:MaterialEntity] it represents the age of.", lang="en"),
)

# NOTE: Could be redundant to bibo:editor, but bibo:editor has a domain of bibo:Document, not dcterms:BibliographicResource, so resources would need to be declared as both.
# NOTE: I imagine this is related to the OWA.
createOP(
    name="editedBy",
    namespace=DWCDP,
    pref_label=Literal("Edited By"),
    graph=g,
    domains=DCTERMS["BibliographicResource"],
    ranges=DCTERMS["Agent"],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that edited it."),
)

# createOP(
#     name="editor",
#     namespace = BIBO,
#     graph = g,
#     domains = DCTERMS["BibliographicResource"],
#     ranges = DCTERMS["Agent"],
#     pref_label = Literal("Edited By"),
#     definition = Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that edited it.", lang="en"),
#     comments = Literal("A person having managerial and sometimes policy-making responsibility for the editorial part of a publishing firm or of a newspaper, magazine, or other publication.", lang="en"),
# )

createOP(
    name="followed",
    namespace=DWCDP,
    graph=g,
    domains=[
        CHRONO["ChronometricAge"],
        DWC["Assertion"],
        DWC["Event"],
        DWC["NucleotideAnalysis"],
        DWC["MaterialEntity"],
        DWC["Occurrence"],
        ECO["Survey"],
    ],
    ranges=DWC["Protocol"],
    pref_label=Literal("Followed"),
    definition=Literal("An [owl:ObjectProperty] used to relate a resource to the [dwc:Protocol] it followed. These resources can be varied and include [chrono:ChronometricAge], [dwc:Assertion], [dwc:Event], [dwc:MaterialEntity], [dwc:NucleotideAnalysis], [dwc:Occurrence], [eco:Survey]", lang="en"),
)

# WARN: Later link to subclasses of dwc:Protocol to avoid cross-class usage of the term.
g.add((DWCDP["usedFor"], OWL["inverseOf"], DWCDP["followed"]))

createOP(
    name="fundedBy",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Provenance"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Funded By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Provenance] to the [dwc:Agent] that funded it.", lang="en"),
)

createOP(
    name="georeferencedBy",
    namespace=DWCDP,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Georeferenced By"),
    subproperty_list=[
        DWCIRI["georeferencedBy"],
    ],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:Location] to the [dwc:Agent] that georeferenced it.", lang="en"),
)

# WARN: Change definition.
createOP(
    name="happenedDuring",
    namespace=DWCDP,
    graph=g,
    domains=[
        DWC["Event"],
        DWC["Occurrence"],
        DWC["OrganismInteraction"],
        ECO["Survey"],
    ],
    ranges=DWC["Event"],
    pref_label=Literal("Happened During"),
    additional_list=[OWL["TransitiveProperty"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Event] to its parent [dwc:Event]."),
    comments=Literal("This property is also an [owl:TransitiveProperty], which allows reasoners to infer hierarchical sampling patterns.", lang="en"),
)

# WARN: Check for consistency.
createOP(
    name="happenedWithin",
    namespace=DWCDP,
    graph=g,
    domains=[
        DWC["Event"],
        DWC["MaterialEntity"],
    ],
    ranges=DWC["GeologicalContext"],
    pref_label=Literal("Happened Within"),
    definition=Literal("An [owl:ObjectProperty] used to relate either a [dwc:Event] or a [dwc:MaterialEntity] to the [dwc:GeologicalContext] within which it happened.", lang="en"),
)

createOP(
    name="hasMedia",
    namespace=DWCDP,
    graph=g,
    domains=[
        CHRONO["ChronometricAge"],
        DCTERMS["Agent"],
        DWC["Event"],
        DWC["GeologicalContext"],
        DWC["MaterialEntity"],
        DWC["Occurrence"],
        DWC["OrganismInteraction"],
    ],
    ranges=AC["Media"],
    pref_label=Literal("Has Media"),
    definition=Literal("An [owl:ObjectProperty] used to relate an entity to an instance of [ac:Media]. These entities can be [chrono:ChronometricAge], [dcterms:Agent], [dwc:Event], [dwc:GeologicalContext], [dwc:MaterialEntity], [dwc:Occurrence], [dwc:OrganismInteraction]", lang="en"),
    comments=Literal("This property also has a [owl:InverseProperty], [dwcdp:isMediaOf], which allows reasoners queries to go through different ways.", lang="en"),
)

createOP(
    name="hasPermitStatus",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Permit"],
    ranges=GGBN["permitStatus_vocabulary"],
    pref_label=Literal("Has Permit Status"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Permit] to concepts associated in [ggbn:permitStatus_vocabulary].", lang="en"),
)

createOP(
    name="hasPermitType",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Permit"],
    ranges=GGBN["permitType_vocabulary"],
    pref_label=Literal("Has Permit Type"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Permit] to concepts associated in [ggbn:permitType_vocabulary].", lang="en"),
)

createOP(
    name="identifiedBy",
    namespace=DWCDP,
    graph=g,
    domains=[
        DWC["Identification"],
        DWC["Occurrence"],
        ECO["Survey"],
    ],
    ranges=DCTERMS["Agent"],
    subproperty_list=[
        DWCIRI["identifiedBy"],
    ],
    pref_label=Literal("Identified By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Identification] to the [dwc:Agent] that identified it.", lang="en"),
)

createOP(
    name="identificationsBy",
    namespace=DWCDP,
    graph=g,
    domains=ECO["Survey"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Identifications By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [eco:Survey] to the [dwc:Agent] who conducted the identifications.", lang="en"),
    comments=Literal("The property [dwcdp:idenficationsBy] should not be confused with [dwcdp:identifiedBy], which has a different [rdfs:domain]. The former applies to a [eco:Survey], whereas the latter applies to a [dwc:Identification].", lang="en"),
)

createOP(
    name="involves",
    namespace=DWCDP,
    graph=g,
    domains=[DWC["Occurrence"]],
    ranges=[DWC["Organism"]],
    pref_label=Literal("Involves"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Occurrence] to the [dwc:Organism] it involves.", lang="en"),
)

# NOTE: Recheck transitivity.
createOP(
    name="isDerivedFrom",
    namespace=DWCDP,
    graph=g,
    domains=[
        AC["Media"],
        DWC["MaterialEntity"],
    ],
    ranges=[
        AC["Media"],
        DWC["MaterialEntity"],
    ],
    additional_list=[OWL["TransitiveProperty"]],
    pref_label=Literal("Is Derived From"),
    definition=Literal("An [owl:ObjectProperty] used to relate a subject entity to the entity from which it was derived.", lang="en"),
    comments=Literal("Though the [rdfs:domain] and [rdfs:range] of this property are varied, [owl:Restriction]s on the classes prevent cross-class use of the term.", lang="en"),
)

createOP(
    name="isPartOf",
    namespace=DWCDP,
    graph=g,
    domains=[
        AC["Media"],
        DCTERMS["BibliographicResource"],
        DWC["MaterialEntity"],
    ],
    ranges=[
        AC["Media"],
        DCTERMS["BibliographicResource"],
        DWC["MaterialEntity"],
    ],
    pref_label=Literal("Is Part Of"),
    definition=Literal("An [owl:ObjectProperty] used to relate a subject entity to the entity from which it was derived.", lang="en"),
    comments=Literal("Though the [rdfs:domain] and [rdfs:range] of this property are varied, [owl:Restriction]s on the classes prevent cross-class use of the term.", lang="en"),
)

createOP(
    name="issuedBy",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Permit"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Issued By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Permit] to the [dcterms:Agent] that issued it.", lang="en"),
)

createOP(
    name="materialCollectedDuring",
    namespace=DWCDP,
    graph=g,
    domains=DWC["NucleotideAnalysis"],
    ranges=DWC["Event"],
    pref_label=Literal("Material Collected During"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:NucleotideAnalysis] to the [dwc:Event] from which the material was collected.", lang="en"),
)

# NOTE: dwc:MolecularProtocol is included in the explorer, but I think it should be handled by dwc:Protocol.
# WARN: Rework
createOP(
    name="mentionedIn",
    namespace=DWCDP,
    graph=g,
    domains=[
        CHRONO["ChronometricAge"],
        DWC["Event"],
        DWC["Identification"],
        DWC["MaterialEntity"],
        DWC["Occurrence"],
        DWC["Organism"],
        DWC["OrganismInteraction"],
        DWC["Protocol"],
        ECO["Survey"]
    ],
    ranges=DCTERMS["BibliographicResource"],
    pref_label=Literal("Mentionned In"),
    definition=Literal("An [owl:ObjectProperty] used to relate a resource to a [dcterms:BibliographicResource] where it was mentionned. These resources include [chrono:ChronometricAge], [dwc:Event], [dwc:Identification], [dwc:MaterialEntity], [dwc:Occurrence], [dwc:Organism], [dwc:OrganismInteraction], [dwc:Protocol] and [eco:Survey].", lang="en"),
)

createOP(
    name="ownedBy",
    namespace=DWCDP,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Owned By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:MaterialEntity] to the [dcterms:Agent] which owns it.", lang="en"),
)

createOP(
    name="produced",
    namespace=DWCDP,
    graph=g,
    domains=DWC["NucleotideAnalysis"],
    ranges=DWC["NucleotideSequence"],
    pref_label=Literal("Produced"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:NucleotideSequence] to the [dwc:NucleotideAnalysis] that produced it.", lang="en"),
)

createOP(
    name="publishedBy",
    namespace=DWCDP,
    graph=g,
    domains=DCTERMS["BibliographicResource"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Published By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that published it.", lang="en"),
)

createOP(
    name="reviewedBy",
    namespace=DWCDP,
    graph=g,
    domains=AC["Media"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Reviewed By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Media] to the [dcterms:Agent] that reviewed it.", lang="en"),
)

createOP(
    name="spatialLocation",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Event"],
    ranges=DCTERMS["Location"],
    subproperty_list=[DCTERMS["spatial"]],
    pref_label=Literal("Spatial Location"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Event] to the [dcterms:Location] it spatially occurred in.", lang="en"),
    version_of_s="http://purl.org/dc/elements/terms/source",
)

createOP(
    name="storedIn",
    namespace=DWCDP,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=DCTERMS["Agent"],
    pref_label=Literal("Stored In"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:MaterialEntity] to the [dcterms:Agent] in which it is stored.", lang="en"),
)

createOP(
    name="targetFor",
    namespace=DWCDP,
    graph=g,
    domains=ECO["SurveyTarget"],
    ranges=ECO["Survey"],
    pref_label=Literal("Target For"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [eco:SurveyTarget] to the [eco:Survey] it is a target for.", lang="en"),
)

# NOTE: For the dwc:OrganismInteraction, preferably consider longer names and avoid reserved keywords.
createOP(
    name="interactionBy",
    namespace=DWCDP,
    graph=g,
    domains=DWC["OrganismInteraction"],
    ranges=DWC["Occurrence"],
    pref_label=Literal("Interaction By"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:OrganismInteraction] to the [dwc:Occurrence] it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the [dwc:Occurrence] considered by this property should be the subject of the statement.", lang="en"),
)

# NOTE: For the dwc:OrganismInteraction, preferably consider longer names and avoid reserved keywords.
createOP(
    name="interactionWith",
    namespace=DWCDP,
    graph=g,
    domains=DWC["OrganismInteraction"],
    ranges=DWC["Occurrence"],
    pref_label=Literal("Interaction With"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:OrganismInteraction] to the [dwc:Occurrence] it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the [dwc:Occurrence] considered by this property should be the object of the statement.", lang="en"),
)

# NOTE: For the dwc:ResourceRelationship, preferably consider longer names and avoid reserved keywords.
createOP(
    name="relationshipOf",
    namespace=DWCDP,
    graph=g,
    pref_label=Literal("Relationship Of"),
    definition=Literal("An [owl:ObjectProperty] used to relate [dwc:ResourceRelationship] to the resource it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the resource considered by this property should be the subject of the statement.", lang="en"),
)

# NOTE: For the dwc:ResourceRelationship, preferably consider longer names and avoid reserved keywords.
createOP(
    name="relationshipTo",
    namespace=DWCDP,
    graph=g,
    pref_label=Literal("Relationship To"),
    definition=Literal("An [owl:ObjectProperty] used to relate [dwc:ResourceRelationship] to the resource it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the resource considered by this property should be the object of the statement.", lang="en"),
    examples=Literal("bb:RobberflyHuntingBee dwcdp:interactionWith bb:Bee456 ."),
)

# NOTE: For now, use the same name as the class, but with camelCase.
createOP(
    name="typeDesignationType",
    namespace=DWCDP,
    graph=g,
    domains=DWC["Identification"],
    ranges=DWC["TypeDesignationType"],
    pref_label=Literal("Type Designation Type"),
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Identification] to an instance of a [dwc:TypeDesignationType].", lang="en"),
    comments=Literal("The class [dwc:TypeDesignationType] considers a finite set of named individuals.", lang="en"),
)

# TEST: Example to see how not considering owl:unionOf affects WebVOWL
# BUG: Simply considering the domains separately considers the intersection
g.add((DWCDP["hasUsagePolicy"], RDF["type"], OWL["ObjectProperty"]))
g.add((DWCDP["hasUsagePolicy"], RDFS["domain"], AC["Media"]))
g.add((DWCDP["hasUsagePolicy"], RDFS["domain"], DWC["MaterialEntity"]))
g.add((DWCDP["hasUsagePolicy"], RDFS["range"], DWC["UsagePolicy"]))

#############################################################################

# NOTE: Property I created. I do not see why there is not a dwciri: analogue of dwc:surveyTargetTypeSource. I would like to be able to give the URI of something like the NERC vocabulary from which my term was taken (e.g. `http://vocab/nerc.ac.uk/collection/S11/current/`).
# BUG: Change to an object property
createOP(
    name="surveyTargetTypeSourceIRI",
    namespace=ECOIRI,
    graph=g,
    domains=ECO["SurveyTarget"],
    pref_label=Literal("Survey Target Type Source IRI"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [eco:surveyTargetValue] is given.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for a controlled vocabulary. This term is to be used only with IRI values and not strings.", lang="en"),
    subproperty_list=[DCTERMS["source"]],
    version_of_s="http://purl.org/dc/elements/terms/source",
)



#####################################################################################################
# BEGIN DATATYPE PROPERTY DEFINITIONS
#####################################################################################################

createDP(
    name="caption",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Caption"),
    definition=Literal("Free-form text to be displayed together with (rather than instead of) a resource that is suitable for captions (especially images).", lang="en"),
    comments=Literal("If both [dcterms:description] and [ac:caption] are present in the metadata, a [dcterms:description] is typically displayed instead of the resource, a [ac:caption] together with the resource. Thus, in HTML it would be appropriate to use [ac:caption] values in figcaption elements. Often only one of the [dcterms:description] or [ac:caption] is present; choose the term most appropriate for your metadata.", lang="en"),
    version_of_s="http://rs.tdwg.org/ac/terms/caption",
    references_s="http://rs.tdwg.org/ac/terms/version/caption-2021-10-05",
)

createDP(
    name="freqHigh",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=XSD["decimal"],
    pref_label=Literal("Upper Frequency Bound"),
    definition=Literal("The highest frequency of the phenomena reflected in the multimedia item or Region of Interest.", lang="en"),
    comments=Literal("Numeric value in hertz (Hz). This term refers to the sound events depicted and not to the constraints of the recording medium, so are in principle independent from sampleRate. If [dwc:scientificName] is specified and if applied to the entire multimedia item, these frequency bounds refer to the sounds of the species given in the [dwc:scientificName] throughout the whole recording. Although many users will specify both [ac:freqLow] and [ac:freqHigh], it is permitted to specify just one or the other, for example if only one of the bounds is discernible.", lang="en"),
    examples=[
        Literal("60", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/freqHigh",
    references_s="http://rs.tdwg.org/ac/terms/version/freqHigh-2021-10-05",
)

createDP(
    name="freqLow",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=XSD["decimal"],
    pref_label=Literal("Lower Frequency Bound"),
    definition=Literal("The lowest frequency of the phenomena reflected in the multimedia item or Region of Interest.", lang="en"),
    comments=Literal("Numeric value in hertz (Hz). This term refers to the sound events depicted and not to the constraints of the recording medium, so are in principle independent from sampleRate. If [dwc:scientificName] is specified and if applied to the entire multimedia item, these frequency bounds refer to the sounds of the species given in the [dwc:scientificName] throughout the whole recording. Although many users will specify both [ac:freqLow] and [ac:freqHigh], it is permitted to specify just one or the other, for example if only one of the bounds is discernible.", lang="en"),
    examples=[
        Literal("60", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/freqLow",
    references_s="http://rs.tdwg.org/ac/terms/version/freqLow-2021-10-05",
)

createDP(
    name="fundingAttribution",
    namespace=AC,
    graph=g,
    domains=DWC["Provenance"],
    ranges=XSD["string"],
    pref_label=Literal("Funding Attribution"),
    definition=Literal("A list (concatenated and separated) of names of the funding organizations or agencies that provided funding for a project.", lang="en"),
    comments=Literal("Specify the full official name of the funding body. This should include the complete name without abbreviations, unless the abbreviation is an official and commonly recognized form (e.g., `NSF` for the `National Science Foundation`). Recommended best practice is to separate the values in a list with space vertical bar space (` | `).", lang="en"),
    examples=[
        Literal("Artsdatabanken"),
        Literal("National Science Foundation"),
        Literal("Norges forskningsråd"),
        Literal("Ocean Census | Nippon Foundation"),
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/fundingAttribution",
    references_s="http://rs.tdwg.org/ac/terms/version/fundingAttribution-2020-01-27",
)

# WARN: It is in ac:, and there is no aciri: but it is built to be an object property
# Could be a way to insert URIs into a database, but declare it as an OP
# I guess that if they are all URIs, the way to go would be to create an actual OP from it
# (i.e. dwcdp:fundedBy) by splitting on the pipe operator
createDP(
    name="fundingAttributionID",
    namespace=AC,
    graph=g,
    domains=DWC["Provenance"],
    ranges=XSD["string"],
    pref_label=Literal("Funding Attribution ID"),
    definition=Literal("An identifier for a dcterms:Agent that financially supported a project.", lang="en"),
    comments=Literal("Provide a unique identifier for the funding body, such as an identifier used in governmental or international databases. If no official identifier exists, use a persistent and unique identifier within your organization or dataset. Recommended best practice is to separate the values in a list with space vertical bar space (` | `).", lang="en"),
    examples=[
        Literal("https://ror.org/00epmv149"),
        Literal("https://ror.org/00epmv149 | https://ror.org/04jnzhb65"),
        Literal("https://www.wikidata.org/wiki/Q13102615"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/fundingAttributionID",
    references_s="http://rs.tdwg.org/dwc/terms/version/fundingAttributionID-2025-06-12",
)

createDP(
    name="heightFrac",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=XSD["decimal"],
    pref_label=Literal("Fractional Height"),
    definition=Literal("The height of the bounding rectangle, expressed as a decimal fraction of the height of a [dwc:Media] resource."),
    comments=Literal("The sum of a valid value plus [ac:yFrac] MUST be greater than zero and less than or equal to one. The precision of this value SHOULD be great enough that when [ac:heightFrac] and [ac:yFrac] are used with the [exif:PixelYDimension] of the Best Quality variant of the Service Access point to calculate the lower right corner of the rectangle, rounding to the nearest integer results in the same vertical pixel originally used to define the point. This term MUST NOT be used with [ac:radius] to define a region of interest. Zero-sized bounding rectangles are not allowed. To designate a point, use the radius option with a zero value."),
    examples=[
        Literal("0.5", datatype=XSD["decimal"]),
        Literal("1", datatype=XSD["decimal"])
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/heightFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/heightFrac-2021-10-05",
)

# NOTE: RECHECK naming
# Consequently, recheck if is a version of ID family or not
createDP(
    name="isROIOf",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Is Part Of Media ID"),
    definition=Literal("An identifier for an [ac:Media] resource of which this [ac:Media] resource is a part.", lang="en"),
    comments=Literal("This term can be used to define an [ac:RegionOfInterest] within an [ac:Media] resource. Recommended best practice is to use a globally unique identifier.", lang="en"),
    version_of_s="http://rs.tdwg.org/ac/terms/isROIOf",
    references_s="http://rs.tdwg.org/ac/terms/version/isROIOf-2021-10-05",
)

createDP(
    name="radius",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=XSD["integer"],
    pref_label=Literal("Radius"),
    definition=Literal("The radius of a bounding circle or arc, expressed as a fraction of the width of a [dwc:Media] resource.", lang="en"),
    comments=Literal("A valid value MUST be greater than or equal to zero. A valid value MAY cause the designated circle to extend beyond the bounds of a [dwc:Media] resource. In that case, the arc within a [dwc:Media] resource plus the bounds of a [dwc:Media] resource specify the region of interest. This term MUST NOT be used with [ac:widthFrac] or [ac:heightFrac] to define a region of interest. This term may be used with [ac:xFrac] and [ac:yFrac] to define a point. In that case, the implication is that the point falls on some object of interest within a [dwc:Media] resource, but nothing more can be assumed about the bounds of that object.", lang="en"),
    examples=[
        Literal("100", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/radius",
    references_s="http://rs.tdwg.org/ac/terms/version/radius-2021-10-05",
)

# NOTE: JSON file says dwc:Media, but we mostly consider ac:Media.
createDP(
    name="subtypeLiteral",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Subtype Literal"),
    definition=Literal("A subcategory that allows further specialization of a [dwc:Media] resource type than [mediaType].", lang="en"),
    comments=Literal("The [ac:subtypeLiteral] term MUST NOT be applied to Collection objects. However, the Description term in the Content Coverage Vocabulary might add further description to a Collection object. Controlled string values SHOULD be selected from the Controlled Vocabulary for [ac:subtype]. Human-readable information about the Controlled Vocabulary for [ac:subtype] is at [http://rs.tdwg.org/ac/doc/subtype/]. It is best practice to use [ac:subtype] instead of [ac:subytpeLiteral] whenever practical.", lang="en"),
    version_of_s="http://rs.tdwg.org/ac/terms/subtypeLiteral",
    references_s="http://rs.tdwg.org/ac/terms/version/subtypeLiteral-2023-09-05",
)

createDP(
    name="widthFrac",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=XSD["decimal"],
    pref_label=Literal("Fractional Width"),
    definition=Literal("The width of the bounding rectangle, expressed as a decimal fraction of the width of a [dwc:Media] resource.", lang="en"),
    comments=Literal("The sum of a valid value plus [ac:xFrac] MUST be greater than zero and less than or equal to one. The precision of this value SHOULD be great enough that when [ac:widthFrac] and [ac:xFrac] are used with the [exif:PixelXDimension] of the Best Quality variant of the Service Access point to calculate the lower right corner of the rectangle, rounding to the nearest integer results in the same horizontal pixel originally used to define the point. This term MUST NOT be used with [ac:radius] to define a region of interest. Zero-sized bounding rectangles are not allowed. To designate a point, use the radius option with a zero value.", lang="en"),
    examples=[
        Literal("0.5", datatype=XSD["decimal"]),
        Literal("1", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/widthFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/widthFrac-2021-10-05",
)

createDP(
    name="xFrac",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=XSD["decimal"],
    pref_label=Literal("Fractional X"),
    definition=Literal("The horizontal position of a reference point, measured from the left side of a [dwc:Media] resource and expressed as a decimal fraction of the width of a [dwc:Media] resource.", lang="en"),
    comments=Literal("A valid value MUST be greater than or equal to zero and less than or equal to one. The precision of this value SHOULD be great enough that when the [ac:xFrac] value is multiplied by the [exif:PixelXDimension] of the Best Quality variant of the Service Access point, rounding to the nearest integer results in the same horizontal pixel location originally used to define the point. This point can serve as the horizontal position of the upper left corner of a bounding rectangle, or as the center of a circle.", lang="en"),
    examples=[
        Literal("0.5", datatype=XSD["decimal"]),
        Literal("1", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/xFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/xFrac-2021-10-05",
)

createDP(
    name="yFrac",
    namespace=AC,
    graph=g,
    domains=AC["Media"],
    ranges=XSD["decimal"],
    pref_label=Literal("Fractional Y"),
    definition=Literal("The vertical position of a reference point, measured from the top of a [dwc:Media] resource and expressed as a decimal fraction of the height of a [dwc:Media] resource.", lang="en"),
    comments=Literal("A valid value MUST be greater than or equal to zero and less than or equal to one. The precision of this value SHOULD be great enough that when the [ac:yFrac] value is multiplied by the [exif:PixelYDimension] of the Best Quality variant of the Service Access point, rounding to the nearest integer results in the same vertical pixel originally used to define the point. This point can serve as the vertical position of the upper left corner of a bounding rectangle, or as the center of a circle.", lang="en"),
    examples=[
        Literal("0.5", datatype=XSD["decimal"]),
        Literal("1", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/ac/terms/yFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/yFrac-2021-10-05",
)

createDP(
    name="description",
    namespace=DCTERMS,
    graph=g,
#    domains=[AC["Media"]],
    domains=OWL["Thing"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Description"),
    definition=Literal("An account of the resource."),
    comments=Literal("Description of collection or individual resource, containing the Who, What, When, Where and Why as free-form text. This property optionally allows the presentation of detailed information and will in most cases be show together with the resource title. If both a [dcterms:description] and a [ac:caption] are present in the metadata, a [dcterms:description] is typically displayed instead of the resource, whereas a [ac:caption] is displayed together with the resource. The [dcterms:description] should aim to be a good proxy for the underlying media resource in cases where only text can be shown, whereas the [ac:caption] may only make sense when shown together with the media. Thus, in HTML it would e appropriate to use [dcterms:description] values for alt attributes in img elements. Often only one of description or caption is present; choose the term most appropriate for your metadata. It is the role of implementers of an [ac:] concrete representation (e.g. an XML Schema, an RDF representation, etc.) to decide and document how formatting advice will be represented in descriptions serialized according to such representations."),
    version_of_s="http://purl.org/dc/terms/description",
)

# WARN: Consider subproperty of dc:identifier with caution
createDP(
    name="identifier",
    namespace=DCTERMS,
    graph=g,
    domains=OWL["Thing"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Identifier"),
    definition=Literal("An unambiguous reference to the resource within a given context."),
    comments=Literal("Recommended practice is to identify the resource by means of a string conforming to an identification system. Examples include International Standard Book Number (ISBN), Digital Object Identifier (DOI), and Uniform Resource Name (URN). Persistent identifiers should be provided as HTTP URIs."),
    version_of_s="http://purl.org/dc/terms/identifier",
)

# BUG: SHOULD BE AN OP.
# NOTE: Felt that the second part was more apt of a comment.
# createDP(
#     name="rights",
#     namespace=DCTERMS,
#     graph=g,
#     domains=DWC["UsagePolicy"],
#     ranges=XSD["anyURI"],
#     pref_label=Literal("Rights (DCTERMS)"),
#     definition=Literal("A URI pointing to structured information about rights held in and over the resource."),
#     comments=Literal("At least one of [dcterms:rights] and [dc:rights] must be supplied but, when feasible, supplying both may make the metadata more widely useful. They must specify the same rights. In case of ambiguity, [dcterms:rights] prevails."),
#     examples=[
#         Literal("http://creativecommons.org/licenses/by/3.0/legalcode"),
#         Literal("http://creativecommons.org/publicdomain/zero/1.0"),
#         ],
#     version_of_s="http://purl.org/dc/terms/rights",
# )

# WARN: Verify domain
# BUG: Object Property, so owl:Thing
createDP(
    name="source",
    namespace=DCTERMS,
    graph=g,
    domains=OWL["Thing"],
    ranges=OWL["Thing"],
    # domains=[DWC["UsagePolicy"]],
    # ranges=[XSD["anyURI"], XSD["string"]],
    pref_label=Literal("Source (DCTERMS)"),
    definition=Literal("A related resource from which the described resource is derived", lang="en"),
    comments=Literal("This property is intended to be used with non-literal values. The described resource may be derived from the related resource in whole or in part. Best practice is to identify the related resource by means of a URI or string conforming to a formal identification system.", lang="en"),
    version_of_s="http://purl.org/dc/terms/source",
)

createDP(
    name="title",
    namespace=DCTERMS,
    graph=g,
#    domains=[AC["Media"]],
    domains=OWL["Thing"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Title"),
    definition=Literal("A name given to a resource."),
    comments=Literal("Concise title, name, or brief descriptive label of institution, resource collection, or individual resource. This field SHOULD include the complete title with all the subtitles, if any. It is strongly suggested to provide a title. The title facilitates interactions with humans: e.g, it could be used as display text of hyperlinks or to provide a choice of images in a pick list. The title is therefore highly useful and an effort should be made to provide it where it is not already available. When the resource is a collection without an institutional or official name, but with a thematic content, a descriptive title, e.g. \"Urban Ants of New England\", would be suitable. In individual media resources depicting taxa, the scientific name or names of taxa are often a good title. Common names, in addition to or instead of scientific names are also acceptable. Indications of action or roles captured by the media resource, such as predatory acts, are desireable (\"Rattlesnake eating deer mouse\", \"Pollinators of California Native Plants\")."),
    version_of_s="http://purl.org/dc/terms/title",
)

# NOTE: REVOIR COMMENTS. SHOULD READ CONTROLLED VOCABULARY
# BUG: Was used for ac:Media, but should be general, also should be an OP
# createOP(
#     name="type",
#     namespace=DCTERMS,
#     graph=g,
#     # domains=[OWL["Thing"]],
#     # domains=[AC["Media"]],
#     # ranges=[RDFS["Literal"]],
#     # ranges=[OWL["Thing"]],
#     pref_label=Literal("Media Type"),
#     definition=Literal("A category that best matches the nature of an [ac:Media] resource."),
#     comments=Literal("Recommended best practice is to use a globally unique identifier."),
#     # examples=[
#     #     Literal("Sound"),
#     #     Literal("StillImage"),
#     #     Literal("MovingImage"),
#     #     Literal("InteractiveResource"),
#     #     Literal("Text"),
#     # ],
#     version_of_s="http://purl.org/dc/terms/type",
# )

createDP(
    name="agentID",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Agent"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Agent ID"),
    definition=Literal("An identifier for a [dcterms:Agent]."),
    subproperty_list=[DCTERMS["identifier"]],
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/agentID"
)

createDP(
    name="agentRemarks",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Agent"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Agent Remarks"),
    definition=Literal("Comments or notes about a [dcterms:Agent]."),
    version_of_s="http://example.com/term-pending/dwc/agentRemarks"
)

createDP(
    name="agentType",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Agent"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Agent Type"),
    definition=Literal("A category that best matches the nature of a [dcterms:Agent]."),
    comments=Literal("Recommended best practice is to use a controlled vocabulary."),
    examples=[
        Literal("person"),
        Literal("group"),
        Literal("organization"),
        Literal("camera"),
    ],
    version_of_s="http://example.com/term-pending/dwc/agentType",
)

createDP(
    name="assayType",
    namespace=DWC,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assay Type"),
    definition=Literal("A method used in the study to detect taxon/taxa of interest in the sample"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary."),
    examples=[
        Literal("targeted"),
        Literal("metabarcoding"),
        Literal("other"),
    ],
    version_of_s="http://example.com/term-pending/dwc/assayType",
)

# NOTE: I would have liked an xsd:date like datatype, but non-ISO 8601 and / make it difficult.
createDP(
    name="assertionEffectiveDate",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assertion Effective Date"),
    definition=Literal("A date on which a state or measurement of a [dwc:Assertion] was deemed to first be in effect."),
    comments=Literal("Recommended best practice is to use a date that conforms to ISO 8601-1:2019."),
    examples=[
        Literal("1963-04-08T14:07-06:00"),
        Literal("2009-02-20T08:40Z"),
        Literal("2018-08-29T15:19"),
        Literal("1809-02-12"),
        Literal("1906-06"),
        Literal("1971"),
        Literal("2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"),
        Literal("1900/1909"),
        Literal("2007-11-13/15"),
    ],
    version_of_s="http://example.com/term-pending/dwc/assertionEffectiveDate",
)

createDP(
    name="assertionID",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assertion ID"),
    definition=Literal("An identifier for a [dwc:Assertion]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/assertionID"
)

# NOTE: I would have liked an xsd:date like datatype, but non-ISO 8601 and / make it difficult.
createDP(
    name="assertionMadeDate",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assertion Made Date"),
    definition=Literal("A date on which a [dwc:Assertion] was created."),
    comments=Literal("Recommended best practice is to use a date that conforms to ISO 8601-1:2019."),
    examples=[
        Literal("1963-04-08T14:07-06:00"),
        Literal("2009-02-20T08:40Z"),
        Literal("2018-08-29T15:19"),
        Literal("1809-02-12"),
        Literal("1906-06"),
        Literal("1971"),
        Literal("2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"),
        Literal("1900/1909"),
        Literal("2007-11-13/15"),
    ],
    version_of_s="http://example.com/term-pending/dwc/assertionMadeDate",
)

createDP(
    name="assertionType",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assertion Type"),
    definition=Literal("A category that best matches the nature of a [dwc:Assertion]."),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the [dwciri:] namespace that allows only an IRI as a value, whereas this term allows for any string literal value."),
    examples=[
        Literal("tail length"),
        Literal("temperature"),
        Literal("trap line length"),
        Literal("survey area"),
        Literal("trap type"),
        ],
    version_of_s="http://example.com/term-pending/dwc/assertionType",
)

# NOTE: Personally, I think a dwc:assertionTypeSourceIRI being a subproperty of dcterms:source would be a better fit.
createDP(
    name="assertionTypeSource",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assertion Type Source"),
    definition=Literal("A reference to the controlled vocabulary in which the definition of a value in [dwc:assertionType] is given."),
    version_of_s="http://purl.org/dc/elements/1.1/source",
    subproperty_list=[DC["source"]],
)

createDP(
    name="assertionValue",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assertion Value"),
    definition=Literal("An asserted value, if it is not numeric."),
    version_of_s="http://example.com/term-pending/dwc/assertionValue",
)

# NOTE: xsd:decimal should be able to handle all real numbers (i.e. including integers).
createDP(
    name="assertionValueNumeric",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=XSD["decimal"],
    pref_label=Literal("Assertion Value Numeric"),
    definition=Literal("An asserted value, if it is numeric."),
    version_of_s="http://example.com/term-pending/dwc/assertionValueNumeric",
)

# NOTE: Personally, I think a dwc:assertionValueSourceIRI being a subproperty of dcterms:source would be a better fit.
createDP(
    name="assertionValueSource",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Assertion Value Source"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [dwc:assertionValue] is given."),
    subproperty_list=[DC["source"]],
    version_of_s="http://purl.org/dc/elements/1.1/source",
)

createDP(
    name="bed",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Bed"),
    definition=Literal("The full name of the lithostratigraphic bed from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Harlem coal"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/bed",
    references_s="http://rs.tdwg.org/dwc/terms/version/bed-2023-09-13",
)

createDP(
    name="caste",
    namespace=DWC,
    graph=g,
    domains=[
        DWC["OccurrenceAssertion"],
        DWC["OrganismAssertion"]
    ],
    ranges=XSD["string"],
    pref_label=Literal("Caste"),
    definition=Literal("Categorisation of individuals for eusocial species (including some mammals and arthropods).", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary that aligns best with the dwc:Taxon. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("queen"),
        Literal("male alate"),
        Literal("intercaste"),
        Literal("minor worker"),
        Literal("soldier"),
        Literal("ergatoid"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/caste",
    references_s="http://rs.tdwg.org/dwc/terms/version/caste-2023-06-28",
)

createDP(
    name="causeOfDeath",
    namespace=DWC,
    graph=g,
    domains=[
        DWC["Occurrence"],
        DWC["Organism"],
    ],
    ranges=XSD["string"],
    pref_label=Literal("Cause Of Death"),
    definition=Literal("An indication of the known or suspected cause of death of a dwc:Organism.", lang="en"),
    comments=Literal("The cause may be due to natural causes (e.g., `disease`, `predation`), human-related activities (e.g., `roadkill`, `pollution`), or other environmental factors (e.g., `extreme weather events`).", lang="en"),
    examples=[
        Literal("trapped"),
        Literal("poisoned"),
        Literal("starved"),
        Literal("drowned"),
        Literal("shot"),
        Literal("starved"),
        Literal("drowned"),
        Literal("shot"),
        Literal("old age"),
        Literal("roadkill"),
        Literal("disease"),
        Literal("herbicide`"),
        Literal("burned"),
        Literal("infanticide"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/causeOfDeath",
    references_s="http://rs.tdwg.org/dwc/terms/version/causeOfDeath-2025-06-12",
)

createDP(
    name="continent",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Continent"),
    definition=Literal("The name of the continent in which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names. Recommended best practice is to leave this field blank if the dcterms:Location spans multiple entities at this administrative level or if the dcterms:Location might be in one or another of multiple possible entities at this level. Multiplicity and uncertainty of the geographic entity can be captured either in the term dwc:higherGeography or in the term dwc:locality, or both.", lang="en"),
    examples=[
        Literal("Africa"),
        Literal("Antarctica"),
        Literal("Asia"),
        Literal("Europe"),
        Literal("North America"),
        Literal("Oceania"),
        Literal("South America"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/continent",
    references_s="http://rs.tdwg.org/dwc/terms/version/continent-2023-06-28",
)

createDP(
    name="coordinatePrecision",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["decimal"],
    pref_label=Literal("Coordinate Precision"),
    definition=Literal("A decimal representation of the precision of the coordinates given in the dwc:decimalLatitude and dwc:decimalLongitude.", lang="en"),
    examples=[
        Literal("0.00001", datatype=XSD["decimal"]),
        Literal("0.000278", datatype=XSD["decimal"]),
        Literal("0.01667", datatype=XSD["decimal"]),
        Literal("1.0", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/coordinatePrecision",
    references_s="http://rs.tdwg.org/dwc/terms/version/coordinatePrecision-2023-06-28",
)

# NOTE: xsd:decimal seems appropriates
createDP(
    name="coordinateUncertaintyInMeters",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["decimal"],
    pref_label=Literal("Coordinate Uncertainty In Meters"),
    definition=Literal("The horizontal distance (in meters) from the given dwc:decimalLatitude and dwc:decimalLongitude describing the smallest circle containing the whole of the dcterms:Location. Leave the value empty if the uncertainty is unknown, cannot be estimated, or is not applicable (because there are no coordinates). Zero is not a valid value for this term.", lang="en"),
    examples=[
        Literal("30", datatype=XSD["decimal"]),
        Literal("100", datatype=XSD["decimal"]),
        Literal("71", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/coordinateUncertaintyInMeters",
    references_s="http://rs.tdwg.org/dwc/terms/version/coordinateUncertaintyInMeters-2023-06-28",
)

createDP(
    name="country",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Country"),
    definition=Literal("The name of the country or major administrative unit in which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names. Recommended best practice is to leave this field blank if the dcterms:Location spans multiple entities at this administrative level or if the dcterms:Location might be in one or another of multiple possible entities at this level. Multiplicity and uncertainty of the geographic entity can be captured either in the term dwc:higherGeography or in the term dwc:locality, or both.", lang="en"),
    examples=[
        Literal("Denmark"),
        Literal("Colombia"),
        Literal("España"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/country",
    references_s="http://rs.tdwg.org/dwc/terms/version/country-2023-06-28",
)

createDP(
    name="countryCode",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Country Code"),
    definition=Literal("The standard code for the country in which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use an ISO 3166-1-alpha-2 country code, or `ZZ` (for an unknown location or a location unassignable to a single country code), or `XZ` (for the high seas beyond national jurisdictions).", lang="en"),
    examples=[
        Literal("AR"),
        Literal("SV"),
        Literal("XZ"),
        Literal("ZZ"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/countryCode",
    references_s="http://rs.tdwg.org/dwc/terms/version/countryCode-2025-06-12",
)

createDP(
    name="county",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    # ranges=XSD["string"],
    ranges=RDF["langString"],
    pref_label=Literal("Second Order Division"),
    definition=Literal("The full, unabbreviated name of the next smaller administrative region than stateProvince (county, shire, department, etc.) in which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names. Recommended best practice is to leave this field blank if the dcterms:Location spans multiple entities at this administrative level or if the dcterms:Location might be in one or another of multiple possible entities at this level. Multiplicity and uncertainty of the geographic entity can be captured either in the term dwc:higherGeography or in the term dwc:locality, or both.", lang="en"),
    examples=[
        Literal("Missoula"),
        Literal("Los Lagos"),
        Literal("Mataró"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/county",
    references_s="http://rs.tdwg.org/dwc/terms/version/county-2023-06-28",
)

createDP(
    name="datasetID",
    namespace=DWC,
    graph=g,
    domains=DWC["Provenance"],
    ranges=XSD["string"],
    pref_label=Literal("Dataset ID"),
    definition=Literal("An identifier for a dataset from which data originated.", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    examples=[
        Literal("b15d4952-7d20-46f1-8a3e-556a512b04c5"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/datasetID",
    references_s="http://rs.tdwg.org/dwc/terms/version/datasetID-2017-10-06",
)

createDP(
    name="day",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["integer"],
    pref_label=Literal("Day"),
    definition=Literal("The integer day of the month on which the dwc:Event occurred.", lang="en"),
    examples=[
        Literal("9", datatype=XSD["integer"]),
        Literal("28", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/day",
    references_s="http://rs.tdwg.org/dwc/terms/version/day-2023-06-28",
)

createDP(
    name="decimalLatitude",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["decimal"],
    pref_label=Literal("Decimal Latitude"),
    definition=Literal("The geographic latitude (in decimal degrees, using the spatial reference system given in dwc:geodeticDatum) of the geographic center of a dcterms:Location. Positive values are north of the Equator, negative values are south of it. Legal values lie between `-90` and `90`, inclusive.", lang="en"),
    examples=[
        Literal("-41.0983423", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/decimalLatitude",
    references_s="http://rs.tdwg.org/dwc/terms/version/decimalLatitude-2023-06-28",
)

createDP(
    name="decimalLongitude",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["decimal"],
    pref_label=Literal("Decimal Longitude"),
    definition=Literal("The geographic longitude (in decimal degrees, using the spatial reference system given in dwc:geodeticDatum) of the geographic center of a dcterms:Location. Positive values are east of the Greenwich Meridian, negative values are west of it. Legal values lie between `-180` and `180`, inclusive.", lang="en"),
    examples=[
        Literal("-41.0983423", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/decimalLongitude",
    references_s="http://rs.tdwg.org/dwc/terms/version/decimalLongitude-2023-06-28",
)

createEDP(
    name="degreeOfEstablishment",
    namespace=DWC,
    graph=g,
    domains=DWC["Occurrence"],
    one_of=[
        Literal("native"),
        Literal("captive"),
        Literal("cultivated"),
        Literal("released"),
        Literal("failing"),
        Literal("casual"),
        Literal("reproducing"),
        Literal("established"),
        Literal("colonising"),
        Literal("invasive"),
    ],
    pref_label=Literal("Degree of Establishment", lang="en"),
    definition=Literal("The degree to which a dwc:Organism survives, reproduces, and expands its range at the given place and time.", lang="en"),
    comments=Literal("Recommended best practice is to use controlled value strings from the controlled vocabulary designated for use with this term, listed at [http://rs.tdwg.org/dwc/doc/doe/](http://rs.tdwg.org/dwc/doc/doe/). For details, refer to [https://doi.org/10.3897/biss.3.38084](https://doi.org/10.3897/biss.3.38084). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("native"),
        Literal("captive"),
        Literal("cultivated"),
        Literal("released"),
        Literal("failing"),
        Literal("casual"),
        Literal("reproducing"),
        Literal("established"),
        Literal("colonising"),
        Literal("invasive"),
        Literal("widespreadInvasive"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/degreeOfEstablishment",
    references_s="http://rs.tdwg.org/dwc/terms/version/degreeOfEstablishment-2023-06-28",
)

createDP(
    name="derivedFromMediaID",
    namespace=DWC,
    graph=g,
    domains=AC["Media"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Derived From Media ID"),
    definition=Literal("An identifier for an [ac:Media] resource of which this [ac:Media] resource is a part."),
    comments=Literal("This term can be used when an [ac:Media] resource has been separated from its source [ac:Media] resource. Recommended best practice is to use a globally unique identifier."),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/derivedFromMediaID",
)

createDP(
    name="disposition",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Disposition"),
    definition=Literal("A current state of a dwc:MaterialEntity with respect to where it can be found.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("in collection"),
        Literal("missing"),
        Literal("on loan"),
        Literal("used up"),
        Literal("destroyed"),
        Literal("deaccessioned"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/disposition",
    references_s="http://rs.tdwg.org/dwc/terms/version/disposition-2023-09-13",
)

createDP(
    name="earliestAgeOrLowestStage",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Earliest Age Or Lowest Stage"),
    definition=Literal("The full name of the earliest possible geochronologic age or lowest chronostratigraphic stage attributable to the stratigraphic horizon from which the dwc:MaterialEntity was collected.", lang="en"),
    examples=[
        Literal("Atlantic"),
        Literal("Boreal"),
        Literal("Skullrockian"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/earliestAgeOrLowestStage",
    references_s="http://rs.tdwg.org/dwc/terms/version/earliestAgeOrLowestStage-2023-09-13",
)

createDP(
    name="earliestEonOrLowestEonothem",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Earliest Eon Or Lowest Eonothem"),
    definition=Literal("The full name of the earliest possible geochronologic eon or lowest chronostratigraphic eonothem or the informal name (`Precambrian`) attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Phanerozoic"),
        Literal("Proterozoic"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/earliestEonOrLowestEonothem",
    references_s="http://rs.tdwg.org/dwc/terms/version/earliestEonOrLowestEonothem-2023-09-13",
)

createDP(
    name="earliestEpochOrLowestSeries",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Earliest Epoch Or Lowest Series"),
    definition=Literal("The full name of the earliest possible geochronologic epoch or lowest chronostratigraphic series attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Holocene"),
        Literal("Pleistocene"),
        Literal("Ibexian Series"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/earliestEpochOrLowestSeries",
    references_s="http://rs.tdwg.org/dwc/terms/version/earliestEpochOrLowestSeries-2023-09-13",
)

createDP(
    name="earliestEraOrLowestErathem",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Earliest Era Or Lowest Erathem"),
    definition=Literal("The full name of the earliest possible geochronologic era or lowest chronostratigraphic erathem attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Cenozoic"),
        Literal("Mesozoic"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/earliestEraOrLowestErathem",
    references_s="http://rs.tdwg.org/dwc/terms/version/earliestEraOrLowestErathem-2023-09-13",
)

createDP(
    name="earliestPeriodOrLowestSystem",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Earliest Period Or Lowest System"),
    definition=Literal("The full name of the earliest possible geochronologic period or lowest chronostratigraphic system attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Neogene"),
        Literal("Tertiary"),
        Literal("Quaternary"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/earliestPeriodOrLowestSystem",
    references_s="http://rs.tdwg.org/dwc/terms/version/earliestPeriodOrLowestSystem-2023-09-13",
)

# NOTE: Used the same range restriction as the DwCDP SQL schema for compatibility
createRDP(
    name="endDayOfYear",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    range_n=XSD["integer"],
    restrictions=[
        [XSD["minInclusive"], 1, XSD["integer"]],
        [XSD["maxInclusive"], 366, XSD["integer"]],
    ],
    pref_label=Literal("End Day Of Year"),
    definition=Literal("The latest integer day of the year on which a dwc:Event occurred.", lang="en"),
    comments=Literal("The value is `1` for January 1 and `365` for December 31, except in a leap year, in which case it is `366`.", lang="en"),
    examples=[
        Literal("1", datatype=XSD["integer"]),
        Literal("32", datatype=XSD["integer"]),
        Literal("366", datatype=XSD["integer"]),
        Literal("365", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/endDayOfYear",
    references_s="http://rs.tdwg.org/dwc/terms/version/endDayOfYear-2023-06-28",
)

# WARN: List of examples in list of terms does not propose nativeEndemic (added in 20205)
createEDP(
    name="establishmentMeans",
    namespace=DWC,
    graph=g,
    domains=DWC["Occurrence"],
    one_of=[
        Literal("native"),
        Literal("nativeReintroduced"),
        Literal("introduced"),
        Literal("introducedAssistedColonisation"),
        Literal("vagrant"),
        Literal("uncertain"),
        Literal("nativeEndemic"),        
    ],
    pref_label=Literal("Establishment Means", lang="en"),
    definition=Literal("Statement about whether a dwc:Organism has been introduced to a given place and time through the direct or indirect activity of modern humans.", lang="en"),
    comments=Literal("Recommended best practice is to use controlled value strings from the controlled vocabulary designated for use with this term, listed at [http://rs.tdwg.org/dwc/doc/em/](http://rs.tdwg.org/dwc/doc/em/). For details, refer to [https://doi.org/10.3897/biss.3.38084](https://doi.org/10.3897/biss.3.38084). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("native"),
        Literal("nativeReintroduced"),
        Literal("introduced"),
        Literal("introducedAssistedColonisation"),
        Literal("vagrant"),
        Literal("uncertain"),
        Literal("nativeEndemic"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/establishmentMeans",
    references_s="http://rs.tdwg.org/dwc/terms/version/establishmentMeans-2023-06-28",
)

createDP(
    name="eventDate",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["string"],
    pref_label=Literal("Event Date"),
    definition=Literal("The date-time or interval during which a dwc:Event occurred. For occurrences, this is the date-time when the dwc:Event was recorded. Not suitable for a time in a geological context.", lang="en"),
    comments=Literal("Recommended best practice is to use a date that conforms to ISO 8601-1:2019.", lang="en"),
    examples=[
        Literal("1963-04-08T14:07-06:00"),
        Literal("2009-02-20T08:40Z"),
        Literal("2018-08-29T15:19"),
        Literal("1809-02-12"),
        Literal("1906-06"),
        Literal("1971"),
        Literal("2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"),
        Literal("1900/1909"),
        Literal("2007-11-13/15"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/eventDate",
    references_s="http://rs.tdwg.org/dwc/terms/version/eventDate-2025-06-12"
)

createDP(
    name="eventID",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Event ID"),
    definition=Literal("An identifier for a [dwc:Event].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    examples=[
        Literal("INBO:VIS:Ev:00009375"),
    ],
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/eventID",
    references_s="http://rs.tdwg.org/dwc/terms/version/eventID-2023-06-28"
)

createDP(
    name="eventRemarks",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=RDF["langString"],
    pref_label=Literal("Event Remarks"),
    definition=Literal("Comments or notes about the dwc:Event.", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    examples=[
        Literal("After the recent rains the river is nearly at flood stage."),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/eventRemarks",
    references_s="http://rs.tdwg.org/dwc/terms/version/eventRemarks-2023-06-28"
)

# WARN: Left the range to xsd:string as some examples are not compliant with xsd:time
createDP(
    name="eventTime",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["string"],
    pref_label=Literal("Event Time"),
    definition=Literal("The time or interval during which a dwc:Event occurred.", lang="en"),
    comments=Literal("Recommended best practice is to use a time of day that conforms to ISO 8601-1:2019.", lang="en"),
    examples=[
        Literal("14:07-06:00"),
        Literal("08:40:21Z"),
        Literal("13:00:00Z/15:30:00Z"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/eventTime",
    references_s="http://rs.tdwg.org/dwc/terms/version/eventTime-2025-06-12"
)

createDP(
    name="eventType",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=RDF["langString"],
    pref_label=Literal("Event Type"),
    definition=Literal("A narrow category that best matches the nature of a dwc:Event.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("BioBlitz"),
        Literal("camera trap deployment"),
        Literal("expedition"),
        Literal("project"),
        Literal("site visit"),
        Literal("trawl"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/eventType",
    references_s="http://rs.tdwg.org/dwc/terms/version/eventType-2023-06-28"
)

createDP(
    name="fieldNotes",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["anyURI"],
    pref_label=Literal("Field Notes"),
    definition=Literal("One of a) an indicator of the existence of, b) a reference to (publication, URI), or c) the text of notes taken in the field about the dwc:Event.", lang="en"),
    comments=Literal("This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("Notes available in the Grinnell-Miller Library."),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/fieldNotes",
    references_s="http://rs.tdwg.org/dwc/terms/version/fieldNotes-2023-06-28"
)

createDP(
    name="fieldNumber",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["string"],
    pref_label=Literal("Field Number"),
    definition=Literal("An identifier given to the dwc:Event in the field. Often serves as a link between field notes and the dwc:Event.", lang="en"),
    comments=Literal("This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("RV Sol 87-03-08"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/fieldNumber",
    references_s="http://rs.tdwg.org/dwc/terms/version/fieldNumber-2023-06-28"
)

createDP(
    name="footprintSRS",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Footprint SRS"),
    definition=Literal("The ellipsoid, geodetic datum, or spatial reference system (SRS) upon which the geometry given in dwc:footprintWKT is based.", lang="en"),
    comments=Literal("Recommended best practice is to use the EPSG code of the SRS, if known. Otherwise use a controlled vocabulary for the name or code of the geodetic datum, if known. Otherwise use a controlled vocabulary for the name or code of the ellipsoid, if known. If none of these is known, use the value not recorded. It is also permitted to provide the SRS in Well-Known-Text, especially if no EPSG code provides the necessary values for the attributes of the SRS. Do not use this term to describe the SRS of the dwc:decimalLatitude and dwc:decimalLongitude, nor of any verbatim coordinates - use the dwc:geodeticDatum and dwc:verbatimSRS instead. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("EPSG:4326"),
        Literal("GEOGCS[\"GCS_WGS_1984\", DATUM[\"D_WGS_1984\", SPHEROID[\"WGS_1984\",6378137,298.257223563]], PRIMEM[\"Greenwich\",0], UNIT[\"Degree\",0.0174532925199433]]"),
        Literal("not recorded"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/footprintSRS",
    references_s="http://rs.tdwg.org/dwc/terms/version/footprintSRS-2025-06-12",
)

createDP(
    name="footprintWKT",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Footprint WKT"),
    definition=Literal("A Well-Known Text (WKT) representation of the shape (footprint, geometry) that defines the dcterms:Location. A dcterms:Location may have both a point-radius representation (see dwc:decimalLatitude) and a footprint representation, and they may differ from each other.", lang="en"),
    comments=Literal("This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("POLYGON ((10 20, 11 20, 11 21, 10 21, 10 20))"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/footprintWKT",
    references_s="http://rs.tdwg.org/dwc/terms/version/footprintWKT-2023-06-28",
)

createDP(
    name="formation",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Formation"),
    definition=Literal("The full name of the lithostratigraphic formation from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Notch Peak Formation"),
        Literal("House Limestone"),
        Literal("Fillmore Formation"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/formation",
    references_s="http://rs.tdwg.org/dwc/terms/version/formation-2023-09-13",
)

createDP(
    name="geodeticDatum",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Geodetic Datum"),
    definition=Literal("The ellipsoid, geodetic datum, or spatial reference system (SRS) upon which the geographic coordinates given in dwc:decimalLatitude and dwc:decimalLongitude are based.", lang="en"),
    comments=Literal("Recommended best practice is to use the EPSG code of the SRS, if known. Otherwise use a controlled vocabulary for the name or code of the geodetic datum, if known. Otherwise use a controlled vocabulary for the name or code of the ellipsoid, if known. If none of these is known, use the value not recorded. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for a string literal value.", lang="en"),
    examples=[
        Literal("EPSG:4326"),
        Literal("WGS84"),
        Literal("NAD27"),
        Literal("Campo Inchauspe"),
        Literal("European 1950"),
        Literal("Clarke 1866"),
        Literal("not recorded"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/geodeticDatum",
    references_s="http://rs.tdwg.org/dwc/terms/version/geodeticDatum-2025-06-12",
)

createDP(
    name="geologicalContextID",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Geological Context ID"),
    definition=Literal("An identifier for a [dwc:GeologicalContext]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    examples=[
        Literal("https://opencontext.org/subjects/e54377f7-4452-4315-b676-40679b10c4d9"),
    ],
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/geologicalContextID",
    references_s="http://rs.tdwg.org/dwc/terms/version/geologicalContextID-2023-06-28"
)

createDP(
    name="georeferencedBy",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Georeferenced By"),
    definition=Literal("A list (concatenated and separated) of names of people, groups, or organizations who determined the georeference (spatial representation) for the dcterms:Location.", lang="en"),
    comments=Literal("Recommended best practice is to separate the values in a list with space vertical bar space (` | `). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("Brad Millen (ROM)"),
        Literal("Kristina Yamamoto | Janet Fang"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/georeferencedBy",
    references_s="http://rs.tdwg.org/dwc/terms/version/georeferencedBy-2023-06-28",
)

createDP(
    name="georeferencedDate",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Georeferenced Date"),
    definition=Literal("The date on which the dcterms:Location was georeferenced.", lang="en"),
    comments=Literal("Recommended best practice is to use a date that conforms to ISO 8601-1:2019.", lang="en"),
    examples=[
        Literal("1963-04-08T14:07-06:00"),
        Literal("2009-02-20T08:40Z"),
        Literal("2018-08-29T15:19"),
        Literal("1809-02-12"),
        Literal("1906-06"),
        Literal("1971"),
        Literal("2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"),
        Literal("1900/1909"),
        Literal("2007-11-13/15"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/georeferencedDate",
    references_s="http://rs.tdwg.org/dwc/terms/version/georeferencedDate-2025-06-12",
)

createDP(
    name="georeferenceProtocol",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Georeference Protocol"),
    definition=Literal("A description or reference to the methods used to determine the spatial footprint, coordinates, and uncertainties.", lang="en"),
    comments=Literal("This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("Georeferencing Quick Reference Guide (Zermoglio et al. 2020, https://doi.org/10.35035/e09p-h128)"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/georeferenceProtocol",
    references_s="http://rs.tdwg.org/dwc/terms/version/georeferenceProtocol-2023-06-28",
)

createDP(
    name="georeferenceRemarks",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Georeference Remarks"),
    definition=Literal("Comments or notes about the spatial description determination, explaining assumptions made in addition or opposition to the those formalized in the method referred to in dwc:georeferenceProtocol.", lang="en"),
    examples=[
        Literal("Assumed distance by road (Hwy. 101)"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/georeferenceRemarks",
    references_s="http://rs.tdwg.org/dwc/terms/version/georeferenceRemarks-2025-06-12",
)

createDP(
    name="georeferenceSources",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=[
        XSD["anyURI"],
        XSD["string"],
    ],
    pref_label=Literal("Georeference Sources"),
    definition=Literal("A list (concatenated and separated) of maps, gazetteers, or other resources used to georeference the dcterms:Location, described specifically enough to allow anyone in the future to use the same resources.", lang="en"),
    comments=Literal("Recommended best practice is to separate the values in a list with space vertical bar space (` | `). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("https://www.geonames.org/", datatype=XSD["anyURI"]),
        Literal("USGS 1:24000 Florence Montana Quad 1967 | Terrametrics 2008 on Google Earth"),
        Literal("GeoLocate"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/georeferenceSources",
    references_s="http://rs.tdwg.org/dwc/terms/version/georeferenceSources-2023-06-28",
)

createDP(
    name="georeferenceVerificationStatus",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Georeference Verification Status"),
    definition=Literal("A categorical description of the extent to which the georeference has been verified to represent the best possible spatial description for the dcterms:Location of the dwc:Occurrence.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("unable to georeference"),
        Literal("requires georeference"),
        Literal("requires verification"),
        Literal("verified by data custodian"),
        Literal("verified by contributor"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/georeferenceVerificationStatus",
    references_s="http://rs.tdwg.org/dwc/terms/version/georeferenceVerificationStatus-2023-06-28",
)

createDP(
    name="group",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Group"),
    definition=Literal("The full name of the lithostratigraphic group from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Bathurst"),
        Literal("Lower Wealden"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/group",
    references_s="http://rs.tdwg.org/dwc/terms/version/group-2023-09-13",
)

createDP(
    name="habitat",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=RDF["langString"],
    pref_label=Literal("Habitat"),
    definition=Literal("A category or description of the habitat in which the dwc:Event occurred.", lang="en"),
    comments=Literal("This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("oak savanna"),
        Literal("pre-cordilleran steppe"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/habitat",
    references_s="http://rs.tdwg.org/dwc/terms/version/habitat-2023-06-28",
)

createDP(
    name="higherGeography",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Higher Geography"),
    definition=Literal("A list (concatenated and separated) of geographic names less specific than the information captured in the dwc:locality term.", lang="en"),
    comments=Literal("Recommended best practice is to separate the values in a list with space vertical bar space (` | `), with terms in order from least specific to most specific.", lang="en"),
    examples=[
        Literal("North Atlantic Ocean"),
        Literal("South America | Argentina | Patagonia | Parque Nacional Nahuel Huapi | Neuquén | Los Lagos"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/higherGeography",
    references_s="http://rs.tdwg.org/dwc/terms/version/higherGeography-2023-06-28",
)

createDP(
    name="higherGeographyID",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=[
        XSD["anyURI"],
        XSD["string"],
    ],
    pref_label=Literal("Higher Geography ID"),
    definition=Literal("An identifier for the geographic region within which the dcterms:Location occurred.", lang="en"),
    comments=Literal("Recommended best practice is to use a persistent identifier from a controlled vocabulary such as the Getty Thesaurus of Geographic Names.", lang="en"),
    examples=[
        Literal("http://vocab.getty.edu/tgn/1002002", datatype=XSD["anyURI"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/higherGeographyID",
    references_s="http://rs.tdwg.org/dwc/terms/version/higherGeographyID-2023-06-28",
)

createDP(
    name="highestBiostratigraphicZone",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Highest Biostratigraphic Zone"),
    definition=Literal("The full name of the highest possible geological biostratigraphic zone of the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Blancan"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/highestBiostratigraphicZone",
    references_s="http://rs.tdwg.org/dwc/terms/version/highestBiostratigraphicZone-2023-09-13",
)

createDP(
    name="identificationID",
    namespace=DWC,
    graph=g,
    domains=DWC["Identification"],
    ranges=XSD["string"],
    pref_label=Literal("Identification ID"),
    definition=Literal("An identifier for a dwc:Identification.", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    examples=[
        Literal("9992"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/identificationID",
    references_s="http://rs.tdwg.org/dwc/terms/version/identificationID-2023-06-28",
)

createDP(
    name="island",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Island"),
    definition=Literal("The name of the island on or near which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names.", lang="en"),
    examples=[
        Literal("Nosy Be"),
        Literal("Bikini Atoll"),
        Literal("Vancouver"),
        Literal("Viti Levu"),
        Literal("Zanzibar"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/island",
    references_s="http://rs.tdwg.org/dwc/terms/version/island-2023-06-28",
)

createDP(
    name="islandGroup",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Island Group"),
    definition=Literal("The name of the island group in which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names.", lang="en"),
    examples=[
        Literal("Alexander Archipelago"),
        Literal("Archipiélago Diego Ramírez"),
        Literal("Seychelles"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/islandGroup",
    references_s="http://rs.tdwg.org/dwc/terms/version/islandGroup-2023-06-28",
)

createDP(
    name="latestAgeOrHighestStage",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Latest Age Or Highest Stage"),
    definition=Literal("The full name of the latest possible geochronologic age or highest chronostratigraphic stage attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Atlantic"),
        Literal("Boreal"),
        Literal("Skullrockian"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/latestAgeOrHighestStage",
    references_s="http://rs.tdwg.org/dwc/terms/version/latestAgeOrHighestStage-2023-09-13",
)

createDP(
    name="latestEonOrHighestEonothem",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Latest Eon Or Highest Eonothem"),
    definition=Literal("The full name of the latest possible geochronologic eon or highest chronostratigraphic eonothem or the informal name (`Precambrian`) attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Phanerozoic"),
        Literal("Proterozoic"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/latestEonOrHighestEonothem",
    references_s="http://rs.tdwg.org/dwc/terms/version/latestEonOrHighestEonothem-2025-06-12",
)

createDP(
    name="latestEpochOrHighestSeries",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Latest Epoch Or Highest Series"),
    definition=Literal("The full name of the latest possible geochronologic epoch or highest chronostratigraphic series attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Holocene"),
        Literal("Pleistocene"),
        Literal("Ibexian Series"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/latestEpochOrHighestSeries",
    references_s="http://rs.tdwg.org/dwc/terms/version/latestEpochOrHighestSeries-2023-09-13",
)

createDP(
    name="latestEraOrHighestErathem",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Latest Era Or Highest Erathem"),
    definition=Literal("The full name of the latest possible geochronologic era or highest chronostratigraphic erathem attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Cenozoic"),
        Literal("Mesozoic"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/latestEraOrHighestErathem",
    references_s="http://rs.tdwg.org/dwc/terms/version/latestEraOrHighestErathem-2023-09-13",
)

createDP(
    name="latestPeriodOrHighestSystem",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Latest Period Or Highest System"),
    definition=Literal("The full name of the latest possible geochronologic period or highest chronostratigraphic system attributable to the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Neogene"),
        Literal("Tertiary"),
        Literal("Quaternary"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/latestPeriodOrHighestSystem",
    references_s="http://rs.tdwg.org/dwc/terms/version/latestPeriodOrHighestSystem-2023-09-13",
)

createDP(
    name="lithostratigraphicTerms",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Lithostratigraphic Terms"),
    definition=Literal("The combination of all lithostratigraphic names for the rock from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Pleistocene-Weichselien"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/lithostratigraphicTerms",
    references_s="http://rs.tdwg.org/dwc/terms/version/lithostratigraphicTerms-2025-06-12",
)

createDP(
    name="locality",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=RDF["langString"],
    pref_label=Literal("Locality"),
    definition=Literal("The specific description of the place.", lang="en"),
    comments=Literal("Less specific geographic information can be provided in other geographic terms (dwc:higherGeography, dwc:continent, dwc:country, dwc:stateProvince, dwc:county, dwc:municipality, dwc:waterBody, dwc:island, dwc:islandGroup). This term may contain information modified from the original to correct perceived errors or standardize the description.", lang="en"),
    examples=[
        Literal("Bariloche, 25 km NNE via Ruta Nacional 40 (=Ruta 237)"),
        Literal("Queets Rainforest, Olympic National Park"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/locality",
    references_s="http://rs.tdwg.org/dwc/terms/version/locality-2023-06-28",
)

createDP(
    name="locationAccordingTo",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=RDF["langString"],
    pref_label=Literal("Location According To"),
    definition=Literal("Information about the source of this dcterms:Location information. Could be a publication (gazetteer), institution, or team of individuals.", lang="en"),
    comments=Literal("This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("Getty Thesaurus of Geographic Names"),
        Literal("GADM"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/locationAccordingTo",
    references_s="http://rs.tdwg.org/dwc/terms/version/locationAccordingTo-2023-06-28",
)

createDP(
    name="locationRemarks",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=RDF["langString"],
    pref_label=Literal("Location Remarks"),
    definition=Literal("Comments or notes about the dcterms:Location.", lang="en"),
    examples=[
        Literal("under water since 2005"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/locationRemarks",
    references_s="http://rs.tdwg.org/dwc/terms/version/locationRemarks-2023-06-28",
)

createDP(
    name="lowestBiostratigraphicZone",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Lowest Biostratigraphic Zone"),
    definition=Literal("The full name of the lowest possible geological biostratigraphic zone of the stratigraphic horizon from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Maastrichtian"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/lowestBiostratigraphicZone",
    references_s="http://rs.tdwg.org/dwc/terms/version/lowestBiostratigraphicZone-2023-09-13",
)

createDP(
    name="materialEntityID",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Material Entity ID"),
    definition=Literal("An identifier for a [dwc:MaterialEntity].", lang="en"),
    comments=Literal("Values of [dwc:materialEntityID] are intended to uniquely and persistently identify a particular [dwc:MaterialEntity] within some context. Examples of context include a particular sample collection, an organization, or the worldwide scale. Recommended best practice is to use a persistent, globally unique identifier. The identifier is bound to a physical object (a [dwc:MaterialEntity]) as opposed to a particular digital record (representation) of that physical object.", lang="en"),
    examples=[
        Literal("06809dc5-f143-459a-be1a-6f03e63fc083"),
    ],
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/materialEntityID",
    references_s="http://rs.tdwg.org/dwc/terms/version/materialEntityID-2023-09-13"
)

# NOTE: Used the same range restriction as the DwCDP SQL schema for compatibility
createRDP(
    name="maximumDepthInMeters",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    range_n=XSD["decimal"],
    restrictions=[
        [XSD["minInclusive"], 0, XSD["decimal"]],
        [XSD["maxInclusive"], 11000, XSD["decimal"]],
    ],
    pref_label=Literal("Maximum Depth In Meters"),
    definition=Literal("The greater depth of a range of depth below the local surface, in meters.", lang="en"),
    examples=[
        Literal("0", datatype=XSD["decimal"]),
        Literal("200", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/maximumDepthInMeters",
    references_s="http://rs.tdwg.org/dwc/terms/version/maximumDepthInMeters-2023-06-28",
)

createDP(
    name="maximumDistanceAboveSurfaceInMeters",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["decimal"],
    pref_label=Literal("Maximum Distance Above Surface In Meters"),
    definition=Literal("The greater distance in a range of distance from a reference surface in the vertical direction, in meters. Use positive values for locations above the surface, negative values for locations below. If depth measures are given, the reference surface is the location given by the depth, otherwise the reference surface is the location given by the elevation.", lang="en"),
    examples=[
        Literal("-1.5", datatype=XSD["decimal"]),
        Literal("4.2", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/maximumDistanceAboveSurfaceInMeters",
    references_s="http://rs.tdwg.org/dwc/terms/version/maximumDistanceAboveSurfaceInMeters-2023-06-28",
)

# NOTE: Used the same range restriction as the DwCDP SQL schema for compatibility
createRDP(
    name="maximumElevationInMeters",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    range_n=XSD["decimal"],
    restrictions=[
        [XSD["minInclusive"], -430, XSD["decimal"]],
        [XSD["maxInclusive"], 8850, XSD["decimal"]],
    ],
    pref_label=Literal("Maximum Elevation In Meters"),
    definition=Literal("The upper limit of the range of elevation (altitude, usually above sea level), in meters.", lang="en"),
    examples=[
        Literal("-205", datatype=XSD["decimal"]),
        Literal("1236", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/maximumElevationInMeters",
    references_s="http://rs.tdwg.org/dwc/terms/version/maximumElevationInMeters-2023-06-28",
)

# NOTE: Confirm namespace dwc: or ac:
createDP(
    name="mediaID",
    namespace=DWC,
    graph=g,
    domains=AC["Media"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Media ID"),
    definition=Literal("An identifier for an [ac:Media] resource.", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/mediaID",
)

createDP(
    name="member",
    namespace=DWC,
    graph=g,
    domains=DWC["GeologicalContext"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Member"),
    definition=Literal("The full name of the lithostratigraphic member from which the [dwc:MaterialEntity] was collected.", lang="en"),
    examples=[
        Literal("Lava Dam Member"),
        Literal("Hellnmaria Member"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/member",
    references_s="http://rs.tdwg.org/dwc/terms/version/member-2023-09-13",
)

# NOTE: Used the same range restriction as the DwCDP SQL schema for compatibility
createRDP(
    name="minimumDepthInMeters",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    range_n=XSD["decimal"],
    restrictions=[
        [XSD["minInclusive"], 0, XSD["decimal"]],
        [XSD["maxInclusive"], 11000, XSD["decimal"]],
    ],
    pref_label=Literal("Minimum Depth In Meters"),
    definition=Literal("The lesser depth of a range of depth below the local surface, in meters.", lang="en"),
    examples=[
        Literal("0", datatype=XSD["decimal"]),
        Literal("100", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/minimumDepthInMeters",
    references_s="http://rs.tdwg.org/dwc/terms/version/minimumDepthInMeters-2023-06-28",
)

createDP(
    name="minimumDistanceAboveSurfaceInMeterss",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["decimal"],
    pref_label=Literal("Minimum Distance Above Surface In Meters"),
    definition=Literal("The lesser distance in a range of distance from a reference surface in the vertical direction, in meters. Use positive values for locations above the surface, negative values for locations below. If depth measures are given, the reference surface is the location given by the depth, otherwise the reference surface is the location given by the elevation.", lang="en"),
    examples=[
        Literal("-1.5", datatype=XSD["decimal"]),
        Literal("4.2", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/minimumDistanceAboveSurfaceInMeterss",
    references_s="http://rs.tdwg.org/dwc/terms/version/minimumDistanceAboveSurfaceInMeters-2023-06-28",
)

# NOTE: Used the same range restriction as the DwCDP SQL schema for compatibility
createRDP(
    name="minimumElevationInMeters",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    range_n=XSD["decimal"],
    restrictions=[
        [XSD["minInclusive"], -430, XSD["decimal"]],
        [XSD["maxInclusive"], 8850, XSD["decimal"]],
    ],
    pref_label=Literal("Minimum Elevation In Meters"),
    definition=Literal("The lower limit of the range of elevation (altitude, usually above sea level), in meters.", lang="en"),
    examples=[
        Literal("-100", datatype=XSD["decimal"]),
        Literal("802", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/minimumElevationInMeters",
    references_s="http://rs.tdwg.org/dwc/terms/version/minimumElevationInMeters-2023-06-28",
)

createDP(
    name="molecularProtocolID",
    namespace=DWC,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Molecular Protocol ID"),
    definition=Literal("An identifier for a [dwc:MolecularProtocol].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/molecularProtocolID",
)

createDP(
    name="month",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["integer"],
    pref_label=Literal("Month"),
    definition=Literal("The integer month in which the dwc:Event occurred.", lang="en"),
    examples=[
        Literal("1", datatype=XSD["integer"]),
        Literal("10", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/month",
    references_s="http://rs.tdwg.org/dwc/terms/version/month-2023-06-28",
)

createDP(
    name="municipality",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Third Order Division"),
    definition=Literal("The full, unabbreviated name of the next smaller administrative region than county (city, municipality, etc.) in which the dcterms:Location occurs. Do not use this term for a nearby named place that does not contain the actual dcterms:Location.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names. Recommended best practice is to leave this field blank if the dcterms:Location spans multiple entities at this administrative level or if the dcterms:Location might be in one or another of multiple possible entities at this level. Multiplicity and uncertainty of the geographic entity can be captured either in the term dwc:higherGeography or in the term dwc:locality, or both.", lang="en"),
    examples=[
        Literal("Holzminden"),
        Literal("Araçatuba"),
        Literal("Ga-Segonyana"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/municipality",
    references_s="http://rs.tdwg.org/dwc/terms/version/municipality-2023-06-28",
)

createDP(
    name="nucleotideAnalysisID",
    namespace=DWC,
    graph=g,
    domains=DWC["NucleotideAnalysis"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Nucleotide Analysis ID"),
    definition=Literal("An identifier for a [dwc:NucleotideAnalysis].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/nucleotideAnalysisID",
)

createDP(
    name="nucleotideSequenceID",
    namespace=DWC,
    graph=g,
    domains=DWC["NucleotideSequence"],
    ranges=XSD["string"],
    pref_label=Literal("Nucleotide Sequence ID"),
    subproperty_list=[DCTERMS["identifier"]],
    definition=Literal("An identifier for a [dwc:NucleotideSequence].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/molecularProtocolID",
)

createDP(
    name="nucleotideSequenceRemarks",
    namespace=DWC,
    graph=g,
    domains=DWC["NucleotideSequence"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Nucleotide Sequence Remarks"),
    definition=Literal("Comments or notes about a [dwc:NucleotideSequence].", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/nucleotideSequenceRemarks",
)

createDP(
    name="objectQuantity",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=[
        XSD["integer"],
        XSD["string"],
    ],
    pref_label=Literal("Object Quantity"),
    definition=Literal("A number or enumeration value for the quantity of differentiable dwc:MaterialEntities comprising this dwc:MaterialEntity.", lang="en"),
    comments=Literal("An dwc:objectQuantity must have a corresponding dwc:objectQuantityType.", lang="en"),
    examples=[
        Literal("27", datatype=XSD["integer"]),
        Literal("many"),
    ],
    version_of_s="http://example.com/term-pending/dwc/objectQuantity",
)

createDP(
    name="objectQuantityType",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Object Quantity Type"),
    definition=Literal("The type of quantification system used for the quantity of dwc:MaterialEntities.", lang="en"),
    comments=Literal("An dwc:objectQuantityType must have a corresponding dwc:objectQuantity.", lang="en"),
    examples=[
        Literal("individuals"),
    ],
    version_of_s="http://example.com/term-pending/dwc/objectQuantityType",
)

createDP(
    name="occurrenceID",
    namespace=DWC,
    graph=g,
    domains=DWC["Occurrence"],
    ranges=[
        XSD["anyURI"],
        XSD["string"],
    ],
    pref_label=Literal("Occurrence ID"),
    definition=Literal("An identifier for the dwc:Occurrence (as opposed to a particular digital record of the dwc:Occurrence). In the absence of a persistent global unique identifier, construct one from a combination of identifiers in the record that will most closely make the dwc:occurrenceID globally unique.", lang="en"),
    comments=Literal("Recommended best practice is to use a persistent, globally unique identifier.", lang="en"),
    examples=[
        Literal("http://arctos.database.museum/guid/MSB:Mamm:233627", datatype=XSD["anyURI"]),
        Literal("000866d2-c177-4648-a200-ead4007051b9"),
        Literal("urn:catalog:UWBM:Bird:89776", datatype=XSD["anyURI"]),
    ],
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/occurrenceID",
    references_s="http://rs.tdwg.org/dwc/terms/version/occurrenceID-2023-06-28",
)

createDP(
    name="occurrenceRemarks",
    namespace=DWC,
    graph=g,
    domains=DWC["Occurrence"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Occurrence Remarks"),
    definition=Literal("Comments or notes about the dwc:Occurrence.", lang="en"),
    examples=[
        Literal("found dead on road"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/occurrenceRemarks",
    references_s="http://rs.tdwg.org/dwc/terms/version/occurrenceRemarks-2023-06-28",
)

# WARN: Considered the enumerated terms from the DwCDP SQL schema.
# It considers `not detected` and not `notDetected`
createEDP(
    name="occurrenceStatus",
    namespace=DWC,
    graph=g,
    domains=DWC["Occurrence"],
    pref_label=Literal("Occurrence Status"),
    one_of=[
        Literal("absent"),
        Literal("detected"),
        Literal("not detected"),
        Literal("present"),
    ],
    definition=Literal("A statement about the detection or non-detection of a dwc:Organism.", lang="en"),
    comments=Literal("For dwc:Occurrences, the default vocabulary is recommended to consist of `detected` and `notDetected`, but can be extended by implementers with good justification. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("detected"),
        Literal("notDetected"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/occurrenceStatus",
    references_s="http://rs.tdwg.org/dwc/terms/version/occurrenceStatus-2023-06-28",
)

createDP(
    name="organismID",
    namespace=DWC,
    graph=g,
    domains=DWC["Organism"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Organism ID"),
    definition=Literal("An identifier for a [dwc:Organism].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/organismID",
    references_s="http://rs.tdwg.org/dwc/terms/version/organismID-2023-06-28",
)

createDP(
    name="organismInteractionID",
    namespace=DWC,
    graph=g,
    domains=DWC["OrganismInteraction"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Organism Interaction ID"),
    definition=Literal("An identifier for a [dwc:OrganismInteraction].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/organismID",
)

createDP(
    name="organismName",
    namespace=DWC,
    graph=g,
    domains=DWC["Organism"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Organism Name"),
    definition=Literal("A textual name or label assigned to a dwc:Organism instance.", lang="en"),
    examples=[
        Literal("Huberta"),
        Literal("Boab Prison Tree"),
        Literal("J pod"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/organismName",
    references_s="http://rs.tdwg.org/dwc/terms/version/organismName-2023-06-28",
)

createDP(
    name="organismRemarks",
    namespace=DWC,
    graph=g,
    domains=DWC["Organism"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Organism Remarks"),
    definition=Literal("Comments or notes about the dwc:Organism instance.", lang="en"),
    examples=[
        Literal("One of a litter of six"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/organismRemarks",
    references_s="http://rs.tdwg.org/dwc/terms/version/organismRemarks-2023-06-28",
)

createDP(
    name="organismScope",
    namespace=DWC,
    graph=g,
    domains=DWC["Organism"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Organism Scope"),
    definition=Literal("A description of the kind of dwc:Organism instance. Can be used to indicate whether the dwc:Organism instance represents a discrete organism or if it represents a particular type of aggregation.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term is not intended to be used to specify a type of dwc:Taxon. To describe the kind of dwc:Organism using a URI object in RDF, use rdf:type ([http://www.w3.org/1999/02/22-rdf-syntax-ns#type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type)) instead.", lang="en"),
    examples=[
        Literal("multicellular organism"),
        Literal("virus"),
        Literal("clone"),
        Literal("pack"),
        Literal("colony"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/organismScope",
    references_s="http://rs.tdwg.org/dwc/terms/version/organismScope-2023-06-28",
)

createDP(
    name="ownerInstitutionCode",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Owner Institution Code"),
    definition=Literal("A name (or acronym) in use by an institution having ownership of a dwc:MaterialEntity.", lang="en"),
    examples=[
        Literal("NPS"),
        Literal("APN"),
        Literal("InBio"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/ownerInstitutionCode",
    references_s="http://rs.tdwg.org/dwc/terms/version/ownerInstitutionCode-2023-06-28",
)

createDP(
    name="parentEventID",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Parent Event ID"),
    definition=Literal("An identifier for the broader dwc:Event that groups this and potentially other dwc:Events.", lang="en"),
    comments=Literal("Use a globally unique identifier for a dwc:Event or an identifier for a dwc:Event that is specific to the data set."),
    examples=[
        Literal("A1"),
    ],
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/parentEventID",
    references_s="http://rs.tdwg.org/dwc/terms/version/parentEventID-2023-06-28",
)

# createDP(
#     name="pathway",
#     namespace=DWC,
#     graph=g,
#     domains=DWC["Occurrence"],
#     ranges=XSD["string"],
#     pref_label=Literal("Pathway"),
#     definition=Literal("The process by which a dwc:Organism came to be in a given place at a given time.", lang="en"),
#     comments=Literal("Recommended best practice is to use controlled value strings from the controlled vocabulary designated for use with this term, listed at [http://rs.tdwg.org/dwc/doc/pw/](http://rs.tdwg.org/dwc/doc/pw/). For details, refer to [https://doi.org/10.3897/biss.3.38084](https://doi.org/10.3897/biss.3.38084). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
#     examples=[
#         Literal("releasedForUse"),
#         Literal("otherEscape"),
#         Literal("transportContaminant"),
#         Literal("transportStowaway"),
#         Literal("corridor"),
#         Literal("unaided"),
#     ],
#     version_of_s="http://rs.tdwg.org/dwc/terms/pathway",
#     references_s="http://rs.tdwg.org/dwc/terms/version/pathway-2023-06-28",
# )

createEDP(
    name="pathway",
    namespace=DWC,
    graph=g,
    domains=DWC["Occurrence"],
    one_of=[
        Literal("biologicalControl"),
        Literal("erosionControl"),
        Literal("fisheryInTheWild"),
        Literal("hunting"),
        Literal("landscapeImprovement"),
        Literal("conservationOrWildlifeManagement"),
        Literal("releasedForUse"),
        Literal("otherIntentionalRelease"),
        Literal("agriculture"),
        Literal("aquacultureMariculture"),
        Literal("publicGardenZooAquaria"),
        Literal("pet"),
        Literal("farmedAnimals"),
        Literal("forestry"),
        Literal("fur"),
        Literal("horticulture"),
        Literal("ornamentalNonHorticulture"),
        Literal("research"),
        Literal("liveFoodLiveBait"),
        Literal("otherEscape"),
        Literal("contaminantNursery"),
        Literal("contaminateBait"),
        Literal("foodContaminant"),
        Literal("contaminantOnAnimals"),
        Literal("parasitesOnAnimals"),
        Literal("contaminantOnPlants"),
        Literal("parasitesOnPlants"),
        Literal("seedContaminant"),
        Literal("timberTrade"),
        Literal("transportationHabitatMaterial"),
        Literal("fishingEquipment"),
        Literal("containerBulk"),
        Literal("hitchhikersAirplane"),
        Literal("hitchhikersShip"),
        Literal("machineryEquipment"),
        Literal("people"),
        Literal("packingMaterial"),
        Literal("ballastWater"),
        Literal("hullFouling"),
        Literal("vehicles"),
        Literal("otherTransport"),
        Literal("waterwaysBasinsSeas"),
        Literal("tunnelsBridges"),
        Literal("naturalDispersal"),
        Literal("releaseInNature"),
        Literal("escapeFromConfinement"),
        Literal("transportContaminant"),
        Literal("transportStowaway"),
        Literal("corridor"),
        Literal("unaided"),
        Literal("intentional"),
        Literal("unintentional"),
        Literal("corridorAndDispersal"),
    ],
    pref_label=Literal("Pathway", lang="en"),
    definition=Literal("The process by which a dwc:Organism came to be in a given place at a given time.", lang="en"),
    comments=Literal("Recommended best practice is to use controlled value strings from the controlled vocabulary designated for use with this term, listed at [http://rs.tdwg.org/dwc/doc/pw/](http://rs.tdwg.org/dwc/doc/pw/). For details, refer to [https://doi.org/10.3897/biss.3.38084](https://doi.org/10.3897/biss.3.38084). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("releasedForUse"),
        Literal("otherEscape"),
        Literal("transportContaminant"),
        Literal("transportStowaway"),
        Literal("corridor"),
        Literal("unaided"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/pathway",
    references_s="http://rs.tdwg.org/dwc/terms/version/pathway-2023-06-28",
)

createDP(
    name="pointRadiusSpatialFit",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["decimal"],
    pref_label=Literal("Point Radius Spatial Fit"),
    definition=Literal("The ratio of the area of the point-radius (dwc:decimalLatitude, dwc:decimalLongitude, dwc:coordinateUncertaintyInMeters) to the area of the true (original, or most specific) spatial representation of the dcterms:Location. Legal values are `0`, greater than or equal to `1`, or undefined. A value of `1` is an exact match or 100% overlap. A value of `0` should be used if the given point-radius does not completely contain the original representation. The dwc:pointRadiusSpatialFit is undefined (and should be left empty) if the original representation is any geometry without area (e.g., a point or polyline) and without uncertainty and the given georeference is not that same geometry (without uncertainty). If both the original and the given georeference are the same point, the dwc:pointRadiusSpatialFit is `1`.", lang="en"),
    comments=Literal("Detailed explanations with graphical examples can be found in the Georeferencing Best Practices, Chapman and Wieczorek, 2020 ([https://doi.org/10.15468/doc-gg7h-s853](https://doi.org/10.15468/doc-gg7h-s853)).", lang="en"),
    examples=[
        Literal("0", datatype=XSD["decimal"]),
        Literal("1", datatype=XSD["decimal"]),
        Literal("1.5708", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/pointRadiusSpatialFit",
    references_s="http://rs.tdwg.org/dwc/terms/version/pointRadiusSpatialFit-2023-06-28",
)

createDP(
    name="preferredAgentName",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Agent"],
    ranges=RDFS["Literal"],
    subproperty_list=[DCTERMS["title"]],
    pref_label=Literal("Preferred Agent Name"),
    definition=Literal("A name of a [dcterms:Agent] preferred in searches and results.", lang="en"),
    version_of_s="http://purl.org/dc/terms/title",
)

createDP(
    name="preferredEventName",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=RDFS["Literal"],
    subproperty_list=[DCTERMS["title"]],
    pref_label=Literal("Preferred Event Name"),
    definition=Literal("The name of a [dwc:Event] preferred in searches and results.", lang="en"),
    version_of_s="http://purl.org/dc/terms/title",
)

createDP(
    name="preparations",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Preparations"),
    definition=Literal("A list (concatenated and separated) of preparations and preservation methods for a dwc:MaterialEntity.", lang="en"),
    comments=Literal("Recommended best practice is to separate the values in a list with space vertical bar space (` | `). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("fossil"),
        Literal("cast"),
        Literal("photograph"),
        Literal("DNA extract"),
        Literal("skin | skull | skeleton"),
        Literal("whole animal (EtOH) | tissue (EDTA)"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/preparations",
    references_s="http://rs.tdwg.org/dwc/terms/version/preparations-2025-06-12",
)

createDP(
    name="projectID",
    namespace=DWC,
    graph=g,
    domains=DWC["Provenance"],
    ranges=[
        XSD["anyURI"],
        XSD["string"],
    ],
    pref_label=Literal("Project ID"),
    definition=Literal("A list (concatenated and separated) of identifiers for projects that contributed to a dwc:Event.", lang="en"),
    comments=Literal("A projectID may be shared in multiple distinct datasets. The nature of the association can be described in the metadata project description element. This term should be used to provide a globally unique identifier (GUID) for a project, if available. This could be a DOI, URI, or any other persistent identifier that ensures a project can be uniquely distinguished from others. Recommended best practice is to separate the values in a list with space vertical bar space (` | `).", lang="en"),
    examples=[
        Literal("https://arvenetternansen.com/", datatype=XSD["anyURI"]),
        Literal("https://doi.org/10.26259/3b15eca7", datatype=XSD["anyURI"]),
        Literal("https://doi.org/10.3030/101180559", datatype=XSD["anyURI"]),
        Literal("OC202405"),
        Literal("RCN276730"),
        Literal("RCN276730 | Artsproject_7-24"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/projectID",
    references_s="http://rs.tdwg.org/dwc/terms/version/projectID-2025-06-12",
)

createDP(
    name="projectTitle",
    namespace=DWC,
    graph=g,
    domains=DWC["Provenance"],
    ranges=RDF["langString"],
    pref_label=Literal("Project Title"),
    definition=Literal("A list (concatenated and separated) of titles or names for projects that contributed to a dwc:Event.", lang="en"),
    comments=Literal("Use this term to provide the official name or title of a project as it is commonly known and cited. Avoid abbreviations unless they are widely understood. Recommended best practice is to separate the values in a list with space vertical bar space (` | `).", lang="en"),
    examples=[
        Literal("Arctic Deep"),
        Literal("Scalidophora i Noreg"),
        Literal("The Nansen Legacy"),
        Literal("Underwater Oases of the Mar del Plata Canyon: Talud Continental IV"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/projectTitle",
    references_s="http://rs.tdwg.org/dwc/terms/version/projectTitle-2025-06-12",
)

createDP(
    name="protocolDescription",
    namespace=DWC,
    graph=g,
    domains=DWC["Protocol"],
    ranges=RDF["langString"],
    pref_label=Literal("Protocol Description"),
    definition=Literal("A detailed description of a dwc:Protocol.", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/protocolDescription",
)

createDP(
    name="protocolID",
    namespace=DWC,
    graph=g,
    domains=DWC["Protocol"],
    ranges=XSD["string"],
    pref_label=Literal("Protocol ID"),
    definition=Literal("An identifier for a dwc:Protocol.", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/protocolID",
)

createDP(
    name="protocolName",
    namespace=DWC,
    graph=g,
    domains=DWC["Protocol"],
    ranges=RDF["langString"],
    pref_label=Literal("Protocol ID"),
    definition=Literal("A name of a dwc:Protocol.", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    examples=[
        Literal("ad hoc observation"),
        Literal("bottom trawl"),
        Literal("point count"),
        Literal("UV light trap"),
    ],
    subproperty_list=[DCTERMS["title"]],
    version_of_s="http://example.com/term-pending/dwc/protocolName",
)

createDP(
    name="protocolType",
    namespace=DWC,
    graph=g,
    domains=DWC["Protocol"],
    ranges=XSD["string"],
    pref_label=Literal("Protocol Type"),
    definition=Literal("A category that best matches the nature of a dwc:Protocol.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary.", lang="en"),
    examples=[
        Literal("measurement"),
        Literal("georeference"),
        Literal("chronometric age"),
        Literal("chronometric age conversion"),
        Literal("sampling effort"),
    ],
    version_of_s="http://example.com/term-pending/dwc/protocolType",
)

createDP(
    name="protocolRemarks",
    namespace=DWC,
    graph=g,
    domains=DWC["Protocol"],
    ranges=RDF["langString"],
    pref_label=Literal("Protocol Remarks"),
    definition=Literal("Comments or notes about a dwc:Protocol.", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/protocolRemarks",
)

createDP(
    name="readCount",
    namespace=DWC,
    graph=g,
    domains=DWC["NucleotideAnalysis"],
    ranges=XSD["integer"],
    pref_label=Literal("Read Count"),
    definition=Literal("A number of reads for a [dwc:NucleotideSequence] in a [dwc:NucleotideAnalysis].", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/readCount",
)

createDP(
    name="relationshipEstablishedDate",
    namespace=DWC,
    graph=g,
    domains=DWC["ResourceRelationship"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Relationship Established Date"),
    definition=Literal("A date on which a [dwc:ResourceRelationship] was established.", lang="en"),
    comments=Literal("Recommended best practice is to use a date that conforms to ISO 8601-1:2019.", lang="en"),
    examples=[
        Literal("1963-04-08T14:07-06:00"),
        Literal("2009-02-20T08:40Z"),
        Literal("2018-08-29T15:19"),
        Literal("1809-02-12"),
        Literal("1906-06"),
        Literal("1971"),
        Literal("2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"),
        Literal("1900/1909"),
        Literal("2007-11-13/15"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/relationshipEstablishedDate",
    references_s="http://rs.tdwg.org/dwc/terms/version/relationshipEstablishedDate-2025-06-12",
)

# WARN: It is in dwc: and not dwciri: but by its construction it is made to be an object property
createOP(
    name="relationshipOfResourceID",
    namespace=DWC,
    graph=g,
    domains=DWC["ResourceRelationship"],
    pref_label=Literal("Relationship Of Resource ID"),
    definition=Literal("An identifier for the relationship type (predicate) that connects the subject identified by dwc:resourceID to its object identified by dwc:relatedResourceID.", lang="en"),
    comments=Literal("Recommended best practice is to use the identifiers of the terms in a controlled vocabulary, such as the OBO Relation Ontology.", lang="en"),
    examples=[
        Literal("http://purl.obolibrary.org/obo/RO_0002456"),
        Literal("http://purl.obolibrary.org/obo/RO_0002455"),
        Literal("https://www.inaturalist.org/observation_fields/879"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/relationshipOfResourceID",
    references_s="http://rs.tdwg.org/dwc/terms/version/relationshipOfResourceID-2023-06-28",
)

createDP(
    name="relationshipRemarks",
    namespace=DWC,
    graph=g,
    domains=DWC["ResourceRelationship"],
    # ranges=XSD["string"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Relationship Remarks"),
    definition=Literal("Comments or notes about the relationship between the two resources.", lang="en"),
    examples=[
        Literal("mother and offspring collected from the same nest"),
        Literal("pollinator captured in the act"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/relationshipRemarks",
    references_s="http://rs.tdwg.org/dwc/terms/version/relationshipRemarks-2023-06-28",
)

createOP(
    name="relationshipTypeIRI",
    namespace=DWC,
    graph=g,
    domains=DWC["ResourceRelationship"],
    pref_label=Literal("Relationship Type (IRI)"),
    definition=Literal("An IRI of a controlled vocabulary value for the type of a dwc:ResourceRelationship.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for a term in a controlled vocabulary.", lang="en"),
    examples=[
        URIRef("http://purl.obolibrary.org/obo/RO_0002456"),
        URIRef("http://purl.obolibrary.org/obo/RO_0002455"),
        URIRef("https://www.inaturalist.org/observation_fields/879"),
    ],
    subproperty_list=[DWC["relationshipOfResourceID"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/relationshipOfResourceID",
    references_s="http://rs.tdwg.org/dwc/terms/version/relationshipOfResourceID-2023-06-28",
)

createDP(
    name="reproductiveCondition",
    namespace=DWC,
    graph=g,
    domains=[
        DWC["OccurrenceAssertion"],
        DWC["OrganismAssertion"],
    ],
    ranges=XSD["string"],
    pref_label=Literal("Reproductive Condition"),
    definition=Literal("The reproductive condition of the biological individual(s) represented in the dwc:Occurrence.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("non-reproductive"),
        Literal("pregnant"),
        Literal("in bloom"),
        Literal("fruit-bearing"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/reproductiveCondition",
    references_s="http://rs.tdwg.org/dwc/terms/version/reproductiveCondition-2023-06-28",
)

createDP(
    name="resourceID",
    namespace=DWC,
    graph=g,
    domains=DWC["ResourceRelationship"],
    ranges=XSD["string"],
    pref_label=Literal("Resource ID"),
    definition=Literal("An identifier for the resource that is the subject of the relationship.", lang="en"),
    examples=Literal("f809b9e0-b09b-11e8-96f8-529269fb1459"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/resourceID",
    references_s="http://rs.tdwg.org/dwc/terms/version/resourceID-2018-09-06",
)

createDP(
    name="resourceRelationshipID",
    namespace=DWC,
    graph=g,
    domains=DWC["ResourceRelationship"],
    ranges=XSD["string"],
    pref_label=Literal("Resource Relationship ID"),
    definition=Literal("An identifier for an instance of relationship between one resource (the subject) and another (dwc:relatedResource, the object).", lang="en"),
    examples=Literal("04b16710-b09c-11e8-96f8-529269fb1459"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/resourceRelationshipID",
    references_s="http://rs.tdwg.org/dwc/terms/version/resourceRelationshipID-2023-06-28",
)

createDP(
    name="resourceRelationshipID",
    namespace=DWC,
    graph=g,
    domains=DWC["ResourceRelationship"],
    ranges=XSD["string"],
    pref_label=Literal("Resource Relationship ID"),
    definition=Literal("An identifier for an instance of relationship between one resource (the subject) and another (dwc:relatedResource, the object).", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/resourceRelationshipID",
    references_s="http://rs.tdwg.org/dwc/terms/version/resourceRelationshipID-2023-06-28",
)

createDP(
    name="samplingEffort",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["string"],
    pref_label=Literal("Sampling Effort"),
    definition=Literal("The amount of effort expended during a dwc:Event.", lang="en"),
    examples=[
        Literal("40 trap-nights"),
        Literal("10 observer-hours"),
        Literal("10 km by foot"),
        Literal("30 km by car"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/samplingEffort",
    references_s="http://rs.tdwg.org/dwc/terms/version/samplingEffort-2023-06-28",
)

createDP(
    name="samplingProtocol",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["string"],
    pref_label=Literal("Sampling Protocol"),
    definition=Literal("The names of, references to, or descriptions of the methods or protocols used during a dwc:Event.", lang="en"),
    comments=Literal("Recommended best practice is describe a dwc:Event with no more than one sampling protocol. In the case of a summary Event with multiple protocols, in which a specific protocol can not be attributed to specific dwc:Occurrences, the recommended best practice is to separate the values in a list with space vertical bar space (` | `). This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("UV light trap"),
        Literal("mist net"),
        Literal("bottom trawl"),
        Literal("ad hoc observation | point count"),
        Literal("Penguins from space: faecal stains reveal the location of emperor penguin colonies, https://doi.org/10.1111/j.1466-8238.2009.00467.x"),
        Literal("Takats et al. 2001. Guidelines for Nocturnal Owl Monitoring in North America. Beaverhill Bird Observatory and Bird Studies Canada, Edmonton, Alberta. 32 pp., http://www.bsc-eoc.org/download/Owl.pdf"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/samplingProtocol",
    references_s="http://rs.tdwg.org/dwc/terms/version/samplingProtocol-2023-06-28",
)

# NOTE: Check domain, can be more
createDP(
    name="scientificName",
    namespace=DWC,
    graph=g,
    domains=[
        DWC["Identification"],
        DWC["MaterialEntity"],
        DWC["Occurrence"],
    ],
    ranges=XSD["string"],
    pref_label=Literal("Scientific Name"),
    definition=Literal("The full scientific name, with authorship and date information if known. When forming part of a dwc:Identification, this should be the name in lowest level taxonomic rank that can be determined. This term should not contain identification qualifications, which should instead be supplied in the dwc:identificationQualifier term.", lang="en"),
    comments=Literal("This term should not contain identification qualifications, which should instead be supplied in the IdentificationQualifier term. When applied to an Organism or Occurrence, this term should be used to represent the scientific name that was applied to the associated Organism in accordance with the Taxon to which it was or is currently identified. Names should be compliant to the most recent nomenclatural code. For example, names of hybrids for algae, fungi and plants should follow the rules of the International Code of Nomenclature for algae, fungi, and plants (Schenzhen Code Articles H.1, H.2 and H.3). Thus, use the multiplication sign × (Unicode U+00D7, HTML ×) to identify a hybrid, not x or X, if possible.", lang="en"),
    examples=[
        Literal("Coleoptera"),
        Literal("Vespertilionidae"),
        Literal("Manis"),
        Literal("Ctenomys sociabilis"),
        Literal("Ambystoma tigrinum diaboli"),
        Literal("Roptrocerus typographi (Györfi, 1952)"),
        Literal("Quercus agrifolia var. oxyadenia (Torr.) J.T. Howell"),
        Literal("×Agropogon littoralis (Sm.) C. E. Hubb."),
        Literal("Mentha × smithiana R. A. Graham"),
        Literal("Agrostis stolonifera L. × Polypogon monspeliensis (L.) Desf."),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/scientificName",
    references_s="http://rs.tdwg.org/dwc/terms/version/scientificName-2023-06-28",
)

# NOTE: Chose xsd:string because I cannot see any use for rdfs:Literal in this case.
createDP(
    name="sequence",
    namespace=DWC,
    graph=g,
    domains=DWC["NucleotideSequence"],
    ranges=XSD["string"],
    pref_label=Literal("Sequence"),
    definition=Literal("A string representing nucleotide base pairs.", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/sequence",
)

createDP(
    name="sex",
    namespace=DWC,
    graph=g,
    domains=[
        DWC["OccurrenceAssertion"],
        DWC["OrganismAssertion"],
    ],
    ranges=XSD["string"],
    pref_label=Literal("Sex"),
    definition=Literal("The sex of the biological individual(s) represented in the dwc:Occurrence.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("female"),
        Literal("male"),
        Literal("hermaphrodite"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/sex",
    references_s="http://rs.tdwg.org/dwc/terms/version/sex-2023-06-28",
)

# WARN: On purpose left bad triple
# Shows that tests using HermiT can silently fail if the ontology is 
# g.add((DWC["BadEvent"], RDF["type"], DWC["Event"]))
# g.add((DWC["BadEvent"], DWC["startDayOfYear"], Literal("2", datatype=XSD["string"])))

createDP(
    name="startDayOfYear",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["integer"],
    pref_label=Literal("Start Day Of Year"),
    definition=Literal("The earliest integer day of the year on which the dwc:Event occurred (`1` for January 1, `365` for December 31, except in a leap year, in which case it is `366`).", lang="en"),
    examples=[
        Literal("1", datatype=XSD["integer"]),
        Literal("366", datatype=XSD["integer"]),
        Literal("365", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/startDayOfYear",
    references_s="http://rs.tdwg.org/dwc/terms/version/startDayOfYear-2023-06-28",
)

createDP(
    name="stateProvince",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("First Order Division"),
    definition=Literal("The name of the next smaller administrative region than country (state, province, canton, department, region, etc.) in which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names. Recommended best practice is to leave this field blank if the dcterms:Location spans multiple entities at this administrative level or if the dcterms:Location might be in one or another of multiple possible entities at this level. Multiplicity and uncertainty of the geographic entity can be captured either in the term dwc:higherGeography or in the term dwc:locality, or both.", lang="en"),
    examples=[
        Literal("Montana"),
        Literal("Minas Gerais"),
        Literal("Córdoba"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/stateProvince",
    references_s="http://rs.tdwg.org/dwc/terms/version/stateProvince-2023-06-28",
)

# NOTE: Comment in JSON file says dwc:Survey?
createDP(
    name="surveyID",
    namespace=DWC,
    graph=g,
    domains=ECO["Survey"],
    ranges=XSD["string"],
    pref_label=Literal("Survey ID"),
    definition=Literal("An identifier for a [eco:Survey].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/surveyID",
)

# NOTE: Comment in JSON file says dwc:SurveyTarget?
createDP(
    name="surveyTargetID",
    namespace=DWC,
    graph=g,
    domains=ECO["SurveyTarget"],
    ranges=XSD["string"],
    pref_label=Literal("Survey Target ID"),
    definition=Literal("An identifier for a [eco:SurveyTarget].", lang="en"),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/surveyTargetID",
)

createDP(
    name="surveyTargetType",
    namespace=DWC,
    graph=g,
    domains=ECO["SurveyTarget"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Survey Target Type"),
    definition=Literal("A scope a [eco:SurveyTarget] describes.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary.", lang="en"),
    examples=[
        Literal("taxon"),
        Literal("habitat"),
        Literal("establishmentMeans"),
        Literal("growthForm"),
        Literal("sex"),
        Literal("lifeStage"),
        Literal("minimum length"),
    ],
    version_of_s="http://example.com/term-pending/dwc/surveyTargetType",
)

# NOTE: Revoir namespace
createDP(
    name="surveyTargetTypeSource",
    namespace=DWC,
    graph=g,
    domains=ECO["SurveyTarget"],
    ranges=XSD["string"],
    pref_label=Literal("Survey Target Type Source"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [eco:surveyTargetValue] is given.", lang="en"),
    subproperty_list=[DC["source"]],
    version_of_s="http://purl.org/dc/elements/1.1/source",
)

createDP(
    name="totalReadCount",
    namespace=DWC,
    graph=g,
    domains=DWC["NucleotideAnalysis"],
    ranges=XSD["integer"],
    pref_label=Literal("Total Read Count"),
    definition=Literal("A total number of reads in a [dwc:NucleotideAnalysis].", lang="en"),
    version_of_s="http://example.com/term-pending/dwc/totalReadCount",
)

createDP(
    name="usagePolicyID",
    namespace=DWC,
    graph=g,
    domains=DWC["UsagePolicy"],
    ranges=XSD["string"],
    pref_label=Literal("Usage Policy ID"),
    definition=Literal("An identifier for a [dwc:UsagePolicy]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier.", lang="en"),
    subproperty_list=[DCTERMS["identifier"]],
    version_of_s="http://example.com/term-pending/dwc/usagePolicyID",
)

createDP(
    name="verbatimAssertionType",
    namespace=DWC,
    graph=g,
    domains=DWC["Assertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Verbatim Assertion Type"),
    definition=Literal("A string representing the type of [dwc:Assertion] as it appeared in the original record.", lang="en"),
    comments=Literal("This term is meant to allow the capture of an unaltered original name for a [dwc:assertionType]. This term is meant to be used in addition to [dwc:assertionType], not instead of it.", lang="en"),
    examples=[
        Literal("water_temp"),
        Literal("Fish biomass"),
        Literal("sampling net mesh size"),
    ],
    version_of_s="http://example.com/term-pending/dwc/verbatimAssertionType",
)

createDP(
    name="verbatimCoordinates",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Coordinates"),
    definition=Literal("The verbatim original spatial coordinates of the dcterms:Location. The coordinate ellipsoid, geodeticDatum, or full Spatial Reference System (SRS) for these coordinates should be stored in dwc:verbatimSRS and the coordinate system should be stored in dwc:verbatimCoordinateSystem.", lang="en"),
    examples=[
        Literal("41 05 54S 121 05 34W"),
        Literal("17T 630000 4833400"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimCoordinates",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimCoordinates-2023-06-28",
)

createDP(
    name="verbatimCoordinateSystem",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Coordinate System"),
    definition=Literal("The coordinate format for the dwc:verbatimLatitude and dwc:verbatimLongitude or the dwc:verbatimCoordinates of the dcterms:Location.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("decimal degrees"),
        Literal("degrees decimal minutes"),
        Literal("degrees minutes seconds"),
        Literal("UTM"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimCoordinateSystem",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimCoordinateSystem-2023-06-28",
)

createDP(
    name="verbatimDepth",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Depth"),
    definition=Literal("The original description of the depth below the local surface.", lang="en"),
    examples=[
        Literal("100-200 m"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimDepth",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimDepth-2017-10-06",
)

# NOTE: I added dcterms:
createDP(
    name="verbatimElevation",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Elevation"),
    definition=Literal("The original description of the elevation (altitude, usually above sea level) of the dcterms:Location.", lang="en"),
    examples=[
        Literal("100-200 m"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimElevation",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimElevation-2017-10-06",
)

# NOTE: TDWG entry actually has a no space EventDate label
createDP(
    name="verbatimEventDate",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim EventDate"),
    definition=Literal("The verbatim original representation of the date and time information for a dwc:Event.", lang="en"),
    examples=[
        Literal("spring 1910"),
        Literal("Marzo 2002"),
        Literal("1999-03-XX"),
        Literal("17IV1934"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimEventDate",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimEventDate-2023-06-28",
)

createDP(
    name="verbatimIdentification",
    namespace=DWC,
    graph=g,
    domains=DWC["Identification"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Label"),
    definition=Literal("A string representing the taxonomic identification as it appeared in the original record.", lang="en"),
    comments=Literal("This term is meant to allow the capture of an unaltered original identification/determination, including identification qualifiers, hybrid formulas, uncertainties, etc. This term is meant to be used in addition to dwc:scientificName (and dwc:identificationQualifier etc.), not instead of it.", lang="en"),
    examples=[
        Literal("Peromyscus sp."),
        Literal("Ministrymon sp. nov. 1"),
        Literal("Anser anser × Branta canadensis"),
        Literal("Pachyporidae?"),
        Literal("Potentilla × pantotricha Soják"),
        Literal("Aconitum pilipes × A. variegatum"),
        Literal("Lepomis auritus x cyanellus")
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimIdentification",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimIdentification-2023-06-28",
)

createDP(
    name="verbatimLabel",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Label"),
    definition=Literal("The content of this term should include no embellishments, prefixes, headers or other additions made to the text. Abbreviations must not be expanded and supposed misspellings must not be corrected. Lines or breakpoints between blocks of text that could be verified by seeing the original labels or images of them may be used. Examples of material entities include preserved specimens, fossil specimens, and material samples. Best practice is to use UTF-8 for all characters. Best practice is to add comment “verbatimLabel derived from human transcription” in dwc:occurrenceRemarks.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimLabel",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimLabel-2023-09-13",
)

createDP(
    name="verbatimLabel",
    namespace=DWC,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Label"),
    definition=Literal("The content of this term should include no embellishments, prefixes, headers or other additions made to the text. Abbreviations must not be expanded and supposed misspellings must not be corrected. Lines or breakpoints between blocks of text that could be verified by seeing the original labels or images of them may be used. Examples of material entities include preserved specimens, fossil specimens, and material samples. Best practice is to use UTF-8 for all characters. Best practice is to add comment “verbatimLabel derived from human transcription” in dwc:occurrenceRemarks.", lang="en"),
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimLabel",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimLabel-2023-09-13",
)

createDP(
    name="verbatimLatitude",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Latitude"),
    definition=Literal("The verbatim original latitude of the dcterms:Location. The coordinate ellipsoid, geodeticDatum, or full Spatial Reference System (SRS) for these coordinates should be stored in dwc:verbatimSRS and the coordinate system should be stored in dwc:verbatimCoordinateSystem.", lang="en"),
    examples=[
        Literal("41 05 54.03S"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimLatitude",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimLatitude-2023-06-28",
)

createDP(
    name="verbatimLocality",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Locality"),
    definition=Literal("The original textual description of the place.", lang="en"),
    examples=[
        Literal("25 km NNE Bariloche por R. Nac. 237"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimLocality",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimLocality-2021-07-15",
)

createDP(
    name="verbatimLongitude",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim Longitude"),
    definition=Literal("The verbatim original longitude of the dcterms:Location. The coordinate ellipsoid, geodeticDatum, or full Spatial Reference System (SRS) for these coordinates should be stored in dwc:verbatimSRS and the coordinate system should be stored in dwc:verbatimCoordinateSystem.", lang="en"),
    examples=[
        Literal("121d 10' 34\" W"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimLongitude",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimLongitude-2023-06-28",
)

createDP(
    name="verbatimSRS",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Verbatim SRS"),
    definition=Literal("The ellipsoid, geodetic datum, or spatial reference system (SRS) upon which coordinates given in dwc:verbatimLatitude and dwc:verbatimLongitude, or dwc:verbatimCoordinates are based.", lang="en"),
    comments=Literal("Recommended best practice is to use the EPSG code of the SRS, if known. Otherwise use a controlled vocabulary for the name or code of the geodetic datum, if known. Otherwise use a controlled vocabulary for the name or code of the ellipsoid, if known. If none of these is known, use the value `not recorded`. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("EPSG:4326"),
        Literal("WGS84"),
        Literal("NAD27"),
        Literal("Campo Inchauspe"),
        Literal("European 1950"),
        Literal("Clarke 1866"),
        Literal("not recorded"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verbatimSRS",
    references_s="http://rs.tdwg.org/dwc/terms/version/verbatimSRS-2025-06-12",
)

createDP(
    name="verticalDatum",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=XSD["string"],
    pref_label=Literal("Vertical Datum"),
    definition=Literal("The vertical datum used as the reference upon which the values in the elevation terms are based.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("EGM84"),
        Literal("EGM96"),
        Literal("EGM2008"),
        Literal("PGM2000A"),
        Literal("PGM2004"),
        Literal("PGM2006"),
        Literal("PGM2007"),
        Literal("EPSG:7030"),
        Literal("not recorded"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/verticalDatum",
    references_s="http://rs.tdwg.org/dwc/terms/version/verticalDatum-2025-06-12",
)

createDP(
    name="vernacularName",
    namespace=DWC,
    graph=g,
    domains=[
        DWC["Identification"],
        DWC["MaterialEntity"],
        DWC["Occurrence"],
    ],
    ranges=XSD["string"],
    pref_label=Literal("Vernacular Name"),
    definition=Literal("A common or vernacular name.", lang="en"),
    examples=[
        Literal("Andean Condor"),
        Literal("Condor Andino"),
        Literal("American Eagle"),
        Literal("Gänsegeier"),
        Literal("death cap"),
        Literal("rainbow trout"),
        Literal("Smoky Quartz"),
        Literal("Amethyst"),
        Literal("Agate"),
        Literal("Tiger's Eye"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/vernacularName",
    references_s="http://rs.tdwg.org/dwc/terms/version/vernacularName-2023-06-28",
)

createDP(
    name="vitality",
    namespace=DWC,
    graph=g,
    domains=[
        DWC["OccurrenceAssertion"],
        DWC["OrganismAssertion"]
    ],
    ranges=XSD["string"],
    pref_label=Literal("Vitality"),
    definition=Literal("An indication of whether a dwc:Organism was alive or dead at the time of collection or observation.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. Intended to be used with records having a dwc:basisOfRecord of `PreservedSpecimen`, `MaterialEntity`,` MaterialSample`, or `HumanObservation`. This term has an equivalent in the dwciri: namespace that allows only an IRI as a value, whereas this term allows for any string literal value.", lang="en"),
    examples=[
        Literal("alive"),
        Literal("dead"),
        Literal("mixedLot"),
        Literal("uncertain"),
        Literal("notAssessed"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/vitality",
    references_s="http://rs.tdwg.org/dwc/terms/version/vitality-2023-09-13",
)

createDP(
    name="waterBody",
    namespace=DWC,
    graph=g,
    domains=DCTERMS["Location"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Water Body"),
    definition=Literal("The name of the water body in which the dcterms:Location occurs.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary such as the Getty Thesaurus of Geographic Names.", lang="en"),
    examples=[
        Literal("Indian Ocean"),
        Literal("Baltic Sea"),
        Literal("Hudson River"),
        Literal("Lago Nahuel Huapi"),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/waterBody",
    references_s="http://rs.tdwg.org/dwc/terms/version/waterBody-2023-06-28",
)

createDP(
    name="year",
    namespace=DWC,
    graph=g,
    domains=DWC["Event"],
    ranges=XSD["integer"],
    pref_label=Literal("Year"),
    definition=Literal("The four-digit year in which the dwc:Event occurred, according to the Common Era Calendar.", lang="en"),
    examples=[
        Literal("1160", datatype=XSD["integer"]),
        Literal("2008", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.tdwg.org/dwc/terms/year",
    references_s="http://rs.tdwg.org/dwc/terms/version/year-2023-06-28",
)

##############################################################################################################

# WARN: I added the comment to be clearer
createEDP(
    name="includeOrExclude",
    namespace=ECO,
    graph=g,
    domains=ECO["SurveyTarget"],
    one_of=[
        Literal("include"),
        Literal("exclude")
    ],
    pref_label=Literal("Include Or Exclude"),
    definition=Literal("Whether the combination of dwc:surveyTargetType and dwc:surveyTargetValue is included or excluded in a dwc:SurveyTarget.", lang="en"),
    comments=Literal("Combinations of dwc:SurveyTarget records of inclusions and exclusions can define complex scopes such as all flying adult Aves except Passeriformes. Recommended best practice is to use a controlled vocabulary consisting of `include` and `exclude` only.", lang="en"),
    examples=[
        Literal("include"),
        Literal("exclude"),
    ],
    version_of_s="http://rs.tdwg.org/eco/terms/includeOrExclude",
)

# NOTE: Definition uses term dwc:Event, but we want to consider dwc:Survey. Should clarify difference or allow cases where an entity can be both a dwc:Event and a eco:Survey.
createDP(
    name="isSurveyTargetFullyReported",
    namespace=ECO,
    graph=g,
    domains=ECO["Survey"],
    ranges=XSD["boolean"],
    pref_label=Literal("Is Survey Target Fully Reported"),
    definition=Literal("A declaration of whether the counts for an instance of the dwc:SurveyTarget report everything that matches the declared dwc:SurveyTarget.", lang="en"),
    comments=Literal("If true (the survey target is fully reported - nothing was left unreported), then this enables inference of absence of detection for everything in that dwc:SurveyTarget that is included but that does not appear in the counts (absent counts signify absence of detection).", lang="en"),
    examples=[
        Literal("true", datatype=XSD["boolean"]),
        Literal("false", datatype=XSD["boolean"]),
    ],  
    version_of_s="http://rs.tdwg.org/eco/terms/isSurveyTargetFullyReported",
)

createDP(
    name="protocolReferences",
    namespace=ECO,
    graph=g,
    domains=DWC["Protocol"],
    ranges=XSD["string"],
    pref_label=Literal("Protocol References"),
    definition=Literal("A list (concatenated and separated) of dcterms:BibliographicResources used in a dwc:Protocol.", lang="en"),
    comments=Literal("Recommended best practice is to separate multiple values in a list with space vertical bar space (` | `).", lang="en"),
    examples=[
        Literal("Penguins from space: faecal stains reveal the location of emperor penguin colonies, https://doi.org/10.1111/j.1466-8238.2009.00467.x"),
    ],
    version_of_s="http://rs.tdwg.org/eco/terms/protocolReferences",
    references_s="http://rs.tdwg.org/eco/terms/version/protocolReferences-2024-02-28",
)

# NOTE: Definition uses term dwc:Event, but we want to consider dwc:Survey. Should clarify difference or allow cases where an entity can be both a dwc:Event and a eco:Survey.
createDP(
    name="siteCount",
    namespace=ECO,
    graph=g,
    domains=ECO["Survey"],
    ranges=XSD["integer"],
    pref_label=Literal("Site Count"),
    definition=Literal("Total number of sites surveyed during a [dwc:Event].", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy.", lang="en"),
    examples=[
        Literal("1", datatype=XSD["integer"]),
        Literal("15", datatype=XSD["integer"]),
    ],  
    version_of_s="http://rs.tdwg.org/eco/terms/siteCount",
    references_s="http://rs.tdwg.org/eco/terms/version/siteCount-2024-02-28",
)

createDP(
    name="siteNestingDescription",
    namespace=ECO,
    graph=g,
    domains=ECO["Survey"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Site Nesting Description"),
    definition=Literal("Textual description of a hierarchical sampling design.", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy.", lang="en"),
    examples=[
        Literal("5 sampling sites of 3-5 plots each"),
    ],
    version_of_s="http://rs.tdwg.org/eco/terms/siteNestingDescription",
    references_s="http://rs.tdwg.org/eco/terms/version/siteNestingDescription-2024-02-28",
)

createDP(
    name="verbatimSiteDescriptions",
    namespace=ECO,
    graph=g,
    domains=ECO["Survey"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Verbatim Site Description"),
    definition=Literal("Original textual description of site(s).", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy. Recommended best practice is to separate multiple values in a list with space vertical bar space (` | `).", lang="en"),
    examples=[
        Literal("Wet flatwoods | Wet depression surrounded by mesic longleaf pine flatwoods | Ground cover of thick Andropogon spp., Sporobolus floridanus, Vaccinium spp., Rhynchospora spp., Centella erecta, Panicum rigidulum"),
    ],
    version_of_s="http://rs.tdwg.org/eco/terms/verbatimSiteDescriptions",
    references_s="http://rs.tdwg.org/eco/terms/version/verbatimSiteDescriptions-2024-02-28",
)

createDP(
    name="verbatimSiteNames",
    namespace=ECO,
    graph=g,
    domains=ECO["Survey"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Verbatim Site Names"),
    definition=Literal("A list (concatenated and separated) of original site names.", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy. Recommended best practice is to separate multiple values in a list with space vertical bar space (` | `).", lang="en"),
    examples=[
        Literal("East Coastal Fringe | St. Marks Wildlife Management Area"),
        Literal("S1 | S2 | C1 | C2 | R14 | R22 | W1"),
    ],
    version_of_s="http://rs.tdwg.org/eco/terms/verbatimSiteNames",
    references_s="http://rs.tdwg.org/eco/terms/version/verbatimSiteNames-2024-02-28",
)

# NOTE: I do not quite see why this property is here. If we are modeling the sequence as a separate entity dwc:NucleotideSequence, shouldn't this be a property for dwc:NucleotideSequence? Also, the newly proposed term dwc:sequence does that, making this term somewhat useless unless for backwards compatibility with datasets that had the DNA extension.
createDP(
    name="dna_sequence",
    namespace=GBIF,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("DNA Sequence"),
    definition=Literal("The DNA sequence.", lang="en"),
    examples=[
        Literal("TCTATCCTCAATTATAGGTCATAATTCACCATCAGTAGATTTAGGAATTTTCTCTATTCATATTGCAGGTGTATCATCAATTATAGGATCAATTAATTTTATTGTAACAATTTTAAATATACATACAAAAACTCATTCATTAAACTTTTTACCATTATTTTCATGATCAGTTCTAGTTACAGCAATTCTCCTTTTATTATCATTA"),
    ],
    version_of_s="https://rs.gbif/org/terms/dna_sequence",
)


# NOTE: Used xsd:string because I couldn't see a use for rdfs:Literal in this case.
createDP(
    name="pcr_primer_forward",
    namespace=GBIF,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Forward PCR Primer"),
    definition=Literal("Forward PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence]. The primer sequence should be reported in uppercase letters.", lang="en"),
    examples=[
        Literal("GGACTACHVGGGTWTCTAAT"),
    ],
    version_of_s="https://rs.gbif/org/terms/pcr_primer_forward",
)

createDP(
    name="pcr_primer_name_forward",
    namespace=GBIF,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Forward PCR Primer Name"),
    definition=Literal("Name of the forward PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence].", lang="en"),
    examples=[
        Literal("jgLCO1490"),
    ],
    version_of_s="https://rs.gbif/org/terms/pcr_primer_name_forward",
)

createDP(
    name="pcr_primer_name_reverse",
    namespace=GBIF,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Reverse PCR Primer Name"),
    definition=Literal("Name of the reverse PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence].", lang="en"),
    examples=[
        Literal("jgHCO2198"),
    ],
    version_of_s="https://rs.gbif/org/terms/pcr_primer_name_reverse",
)

# NOTE: Revoir range
createDP(
    name="pcr_primer_reference",
    namespace=GBIF,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=[
        RDFS["Literal"],
        XSD["anyURI"]
    ],
    pref_label=Literal("PCR Primer Reference"),
    definition=Literal("Reference for the PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment.", lang="en"),
    examples=[
        Literal("https:doi.org/10.11861742-9994-10-31"),
    ],
    version_of_s="https://rs.gbif/org/terms/pcr_primer_reference",
)

# NOTE: Used xsd:string because I couldn't see a use for rdfs:Literal in this case.
createDP(
    name="pcr_primer_reverse",
    namespace=GBIF,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Reverse PCR Primer"),
    definition=Literal("Reverse PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence]. The primer sequence should be reported in uppercase letters.", lang="en"),
    examples=[
        Literal("GGACTACHVGGGTWTCTAAT"),
    ],
    version_of_s="https://rs.gbif/org/terms/pcr_primer_reverse",
)

# NOTE: Used xsd:string because I couldn't see a use for rdfs:Literal in this case.
createDP(
    name="pcr_primer_reverse",
    namespace=GBIF,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Reverse PCR Primer"),
    definition=Literal("Reverse PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence]. The primer sequence should be reported in uppercase letters.", lang="en"),
    examples=[
        Literal("GGACTACHVGGGTWTCTAAT"),
    ],
    version_of_s="https://rs.gbif/org/terms/pcr_primer_reverse",
)

createDP(
    name="concentration",
    namespace=GGBN,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["decimal"],
    pref_label=Literal("DNA Concentration"),
    definition=Literal("Concentration of DNA (weight ng/volume µL).", lang="en"),
    examples=[
        Literal("67.5", datatype=XSD["decimal"]),
    ],
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/concentration",
)

createDP(
    name="concentrationUnit",
    namespace=GGBN,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("DNA Concentration Unit"),
    definition=Literal("Unit used for [ggbn:concentration] measurement.", lang="en"),
    examples=[
        Literal("ng/µL"),
    ],
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/concentrationUnit",
)

createDP(
    name="methodDeterminationConcentrationAndRatios",
    namespace=GGBN,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Method For Concentration Measurement"),
    definition=Literal("Description of method used for [ggbn:concentration] measurement.", lang="en"),
    examples=[
        Literal("Nanodrop"),
        Literal("Qubit"),
    ],
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/methodDeterminationConcentrationAndRatios",
)

createDP(
    name="ratioOfAbsorbance260_230",
    namespace=GGBN,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["decimal"],
    pref_label=Literal("Ratio Of Absorbance At 260 nm and 230 nm"),
    definition=Literal("Ratio of absorbance at 260 nm and 230 nm assessing DNA purity (mostly secondary measure, indicates mainly EDTA, carbohydrates, phenol), (DNA samples only).", lang="en"),
    examples=[
        Literal("1.89", datatype=XSD["decimal"]),
    ],
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/ratioOfAbsorbance260_230",
)

createDP(
    name="ratioOfAbsorbance260_280",
    namespace=GGBN,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["decimal"],
    pref_label=Literal("Ratio Of Absorbance At 260 nm and 280 nm"),
    definition=Literal("Ratio of absorbance at 260 nm and 280 nm assessing DNA purity (mostly secondary measure, indicates mainly EDTA, carbohydrates, phenol), (DNA samples only).", lang="en"),
    examples=[
        Literal("1.91", datatype=XSD["decimal"]),
    ],
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/ratioOfAbsorbance260_280",
)

createDP(
    name="geoClassificationCode",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=XSD["string"],
    pref_label=Literal("Geo Classification Code"),
    definition=Literal("Alphanumeric pattern that adheres to a defined encoding scheme that identifies a particular term in a classification scheme.", lang="en"),
    comments=Literal("Classification codes are specific to a classification system and conform to a xkos:notationPattern.", lang="en"),
    examples=[
        Literal("71.02.02a.01"),
        Literal("9.AD.25"),
    ],
    version_of_s="http://rs.tdwg.org/mineralogy/terms/classificationCode",
)

# NOTE: Confirm term name
# Also maybe consider rdfs:Literal
createDP(
    name="geoName",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntity"],
    ranges=XSD["string"],
    pref_label=Literal("Geo Name"),
    definition=Literal("A human-readable lexical label assigned to a mineral includes both informal (e.g., variety, synonym) and formal (classification) forms.", lang="en"),
    examples=[
        Literal("Garnet Group"),
        Literal("Almandine"),
        Literal("Plagioclase (Series)"),
        Literal("Fluorite"),
    ],
    version_of_s="http://rs.tdwg.org/mineralogy/terms/name",
)

###############################################################################

createDP(
    name="aggregateForm",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Aggregate Form"),
    definition=Literal("Observable crystal shapes of an assemblage of minerals.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary.", lang="en"),
    examples=[
        Literal("radial"),
        Literal("botryoidal"),
        Literal("oolithic"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/aggregateForm",
)

createDP(
    name="alterationDescription",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Alteration Description"),
    definition=Literal("Observable crystal shapes of an assemblage of minerals.", lang="en"),
    comments=Literal("A description of any observed changes in the composition of a mineral brought about by physical or chemical processes related to changes in the physical or chemical environment.", lang="en"),
    examples=[
        Literal("Dolomitization"),
        Literal("Fenetization"),
        Literal("Rodingitization"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/alterationDescription",
)

createDP(
    name="associatedMinerals",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Associated Minerals"),
    definition=Literal("Observable crystal shapes of an assemblage of minerals.", lang="en"),
    examples=[
        Literal("calcite"),
        Literal("dolomite"),
        Literal("baryte"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/associatedMinerals",
)

createDP(
    name="cleavage",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Cleavage"),
    definition=Literal("Types of breakages along a plane of weakness, especially those parallel to crystal faces.", lang="en"),
    examples=[
        Literal("Extraordinary well developped rectangular cleavage"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/cleavage",
)

createDP(
    name="color",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Color"),
    definition=Literal("The intrinsic color of a mineral under natural light.", lang="en"),
    comments=Literal("Here, color is caused by the absorption, or lack of absorption of different wavelengths of natural light by a particular mineral.", lang="en"),
    examples=[
        Literal("Blue"),
        Literal("green"),
        Literal("red"),
        Literal("iridescent"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/color",
)

createDP(
    name="color",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Color"),
    definition=Literal("The intrinsic color of a mineral under natural light.", lang="en"),
    comments=Literal("Here, color is caused by the absorption, or lack of absorption of different wavelengths of natural light by a particular mineral.", lang="en"),
    examples=[
        Literal("Blue"),
        Literal("green"),
        Literal("red"),
        Literal("iridescent"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/color",
)

createDP(
    name="crystalForm",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Crystal Form"),
    definition=Literal("Geometric shape of a crystal.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary.", lang="en"),
    examples=[
        Literal("cube"),
        Literal("ditrigonal pyramid"),
        Literal("scalenohedron"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/crystalForm",
)

createDP(
    name="crystalHabit",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Crystal Habit"),
    definition=Literal("A general term for describing the outward appearance of a mineral.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. For a given type of crystal, the habit may vary from locality to locality depending on environment of growth.", lang="en"),
    examples=[
        Literal("isometric"),
        Literal("tabular"),
        Literal("fibrous"),
        Literal("dogtooth"),
        Literal("nailhead"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/crystalHabit",
)

createDP(
    name="exsolutionTexture",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Exsolution Texture"),
    definition=Literal("A brief description of textures formed by exsolution.", lang="en"),
    examples=[
        Literal("Ilemenite lamellae in olivine"),
        Literal("Clinopyroxene lamellae around the (100) plane of the orthopyroxene"),
        Literal("Antiperthite exsolution"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/exsolutionTexture",
)

createDP(
    name="inclusions",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Inclusions"),
    definition=Literal("Short description of any inclusions present within a mineral that includes the phase and physical characteristics.", lang="en"),
    examples=[
        Literal("Star-shaped rutile needles in quartz"),
        Literal("Needles of tourmaline in quartz (blue quartz)"),
        Literal("Fluid inclusions (liquid bubble and single crystal) in quartz"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/inclusions",
)

createDP(
    name="luminescence",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Luminescence"),
    definition=Literal("The type and nature of light emitted from the mineral upon receiving energy from an external source.", lang="en"),
    comments=Literal("Includes all types of luminescence including fluorescence (all wavelengths) and phosphorescence. Recommended best practice is to use nomenclature in part based on the source of energy, or the trigger for luminescence.", lang="en"),
    examples=[
        Literal("Green fluorescence"),
        Literal("Pink under short wave UV light"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/luminescence",
)

createDP(
    name="luster",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Luster"),
    definition=Literal("The reflection of light from the surface of a mineral, described by its quality and intensity.", lang="en"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary.", lang="en"),
    examples=[
        Literal("Metallic"),
        Literal("Glassy"),
        Literal("Waxy"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/luster",
)

createDP(
    name="maxCrystalDimensionInMillimiters",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=XSD["decimal"],
    pref_label=Literal("Maximum Crystal Dimension In Millimiters"),
    definition=Literal("Maximum axial dimension of largest crystal measured in millimeters.", lang="en"),
    examples=[
        Literal("30", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/maxCrystalDimensionInMillimiters",
)

createDP(
    name="maxSpecimenDimensionInMillimeters",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=XSD["decimal"],
    pref_label=Literal("Maximum Specimen Dimension In Millimeters"),
    definition=Literal("Maximum axial dimension of specimen measured in millimeters.", lang="en"),
    examples=[
        Literal("100", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/maxSpecimenDimensionInMillimeters",
)

createDP(
    name="measuredMassInGrams",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=XSD["decimal"],
    pref_label=Literal("Measured Mass In Grams"),
    definition=Literal("Mass of specimen measured in grams.", lang="en"),
    examples=[
        Literal("4994", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/measuredMassInGrams",
)

createDP(
    name="mineralDescription",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Mineral Description"),
    definition=Literal("Comments or notes about the mineral instance, especially those that distinguish the mineral from similar items in a collection.", lang="en"),
    comments=Literal("The scope of this term is strictly to a mineral within the context of the specimen. Specimen level descriptions belong in the related term minext:specimenDescription. Sibling concept to [http://rs.tdwg.org/dwc/terms/occurrenceRemarks](http://rs.tdwg.org/dwc/terms/occurrenceRemarks).", lang="en"),
    examples=[
        Literal("Pink fluorite on quartz"),
        Literal("Lengenbachite on sugar-stained dolomite"),
        Literal("Epitaxial growth on kyanite"),
        Literal("Doubly terminated quartz crystals"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/mineralDescription",
)

createDP(
    name="specimenDescription",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Specimen Description"),
    definition=Literal("Comments or notes about the specimen (physical object) especially those that distinguish the specimen from similar materials in a collection.", lang="en"),
    comments=Literal("See broader concept [http://rs.tdwg.org/dwc/terms/occurrenceRemarks](http://rs.tdwg.org/dwc/terms/occurrenceRemarks) for additional usage notes.", lang="en"),
    examples=[
        Literal("Showpiece"),
        Literal("Historically valuable"),
        Literal("Extraordinary composition"),
        Literal("Two generations of quartz"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/specimenDescription",
)

createDP(
    name="twinningLaw",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Twinning Law"),
    definition=Literal("Short description of any physically discernable twining.", lang="en"),
    examples=[
        Literal("Dauphiné twinning/Dauphiné Law"),
        Literal("Japan twinning/Japan Law"),
        Literal("Brazil twinning/Brazil Law"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/twinningLaw",
)

createDP(
    name="verbatimMass",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Verbatim Mass"),
    definition=Literal("The original reported verbatim mass includes original units of measurement.", lang="en"),
    examples=[
        Literal("11.01 Lbs"),
        Literal("105.07 g"),
        Literal("2.45 kg"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/verbatimMass",
)

createDP(
    name="verbatimSize",
    namespace=MINEXT,
    graph=g,
    domains=DWC["MaterialEntityAssertion"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Verbatim Size"),
    definition=Literal("The verbatim size of a specimen as originally described in primary source material.", lang="en"),
    examples=[
        Literal("10 cm x 5 cm X 5 cm"),
        Literal("largest diameter 16 cm"),
        Literal("width 3 inches"),
    ],
    version_of_s="http://rs.tdwg.org/minext/terms/verbatimSize",
)

####################################################################################################


createDP(
    name="ampliconSize",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["integer"],
    pref_label=Literal("Amplicon Size"),
    definition=Literal("The length of the amplicon in basepairs.", lang="en"),
    examples=[
        Literal("83", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/ampliconSize",
)

createDP(
    name="annealingTemp",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["decimal"],
    pref_label=Literal("Annealing Phase Temperature"),
    definition=Literal("The reaction temperature during the annealing phase of PCR.", lang="en"),
    examples=[
        Literal("60", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/annealingTemp",
)

createDP(
    name="annealingTempUnit",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Annealing Phase Temperature Unit"),
    definition=Literal("Measurement Unit of the reaction temperature during the annealing phase of PCR.", lang="en"),
    examples=[
        Literal("Degrees celsius")
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/annealingTempUnit",
)

createDP(
    name="baselineValue",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["integer"],
    pref_label=Literal("Fluorescence Baseline Value"),
    definition=Literal("The number of cycles when fluorescence signal from the target amplification is below background fluorescence not originated from the real target amplification.", lang="en"),
    examples=[
        Literal("15", datatype=XSD["integer"]),
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/baselineValue",
)

createDP(
    name="probeReporter",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Probe Reporter"),
    definition=Literal("Type of fluorophore (reporter) used. Probe anneals within amplified target DNA. Polymerase activity degrades the probe that has annealed to the template, and the probe releases the fluorophore from it and breaks the proximity to the quencher, thus allowing fluorescence in the fluorophore.", lang="en"),
    examples=[
        Literal("FAM"),
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/probeReporter",
)

# NOTE: Think a period was missing in the description.
createDP(
    name="probeQuencher",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Probe Quencher"),
    definition=Literal("Type of quencher used. The quencher molecule quenches the fluorescence emitted by the fluorophore when excited by the cycler's light source. As long as fluorophore and the quencher are in proximity, quenching inhibits any fluorescence signals.", lang="en"),
    examples=[
        Literal("NFQ-MGB"),
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/probeQuencher",
)

createDP(
    name="quantificationCycle",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["decimal"],
    pref_label=Literal("Quantification Cycle Number"),
    definition=Literal("The number of cycles required for the fluorescent signal to cross a given value threshold above the baseline. Quantification cycle (Cq), threshold cycle (Ct), crossing point (Cp), and take-off point (TOP) refer to the same value from the real-time instrument. Use of quantification cycle (Cq), is preferable according to the RDML (Real-Time PCR Data Markup Language) data standard ([http://www.rdml.org]).", lang="en"),
    examples=[
        Literal("37.9450950622558", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/quantificationCycle",
)

createDP(
    name="thresholdQuantificationCycle",
    namespace=MIQE,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["decimal"],
    pref_label=Literal("Fluorescence Cycle Threshold"),
    definition=Literal("Threshold for change in fluorescence signal between cycles.", lang="en"),
    examples=[
        Literal("0.3", datatype=XSD["decimal"]),
    ],
    version_of_s="http://rs.gbif.org/terms/miqe/thresholdQuantificationCycle",
)

createDP(
    name="0000001",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Amount Or Size Of Sample Collected"),
    definition=Literal("The total amount or size (volume (ml), mass (g) or aread (m2)) of sample collected.", lang="en"),
    examples=[
        Literal("5 liter"),
    ],
    version_of_s="https://w3id.org/mixs/00000001",
)

createDP(
    name="0000002",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Sample Collection Device"),
    definition=Literal("The device used to collect an environmental sample. This field accepts terms listed under environmental sampling device ([http://purl.obolibrary.org/obo/ENVO]). This field also accepts terms listed under specimen collection device ([http://purl.obolibrary.org/obo/GENEPIO_0002094]).", lang="en"),
    version_of_s="https://w3id.org/mixs/00000002",
)

createDP(
    name="0000003",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Isolation And Growth Condition"),
    definition=Literal("Publication reference in the form of pubmed ID (pmid), digital object identifier (doi) or url for isolation and growth condition specifications of the organism/material.", lang="en"),
    examples=[
        Literal("doi:10.1016/j.syapm.2018.01.009"),
    ],
    version_of_s="https://w3id.org/mixs/00000003",
)

createEDP(
    name="0000005",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    one_of=[
        Literal("contigs"),
        Literal("reads"),
    ],
    pref_label=Literal("Contamination Screening Input"),
    definition=Literal("The type of sequence data used as input.", lang="en"),
    comments=Literal("This property only takes a finite set of possible literal values. For more details, see: [https://genomicsstandardsconsortium.github.io/mixs/ContamScreenInputEnum/].", lang="en"),
    examples=[
        Literal("contigs"),
    ],
    version_of_s="https://w3id.org/mixs/00000005",
)

createDP(
    name="0000006",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("WGA Amplification Kit"),
    definition=Literal("Kit used to amplify genomic DNA in preparation for sequencing.", lang="en"),
    examples=[
        Literal("qiagen repli-g"),
    ],
    version_of_s="https://w3id.org/mixs/00000006",
)

# NOTE: I felt that the browser comment is better suited for a comment.
createDP(
    name="0000008",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Experimental Factor"),
    definition=Literal("Experimental factors are essentially the the variable aspects of an experiment design which can be used to describe an experiment, or set of experiments, in an increasingly detailed manner. This field accepts ontology terms from Experimental Factor Ontology ([efo:]) and/or Ontology for Biomedical Investigations ([obi:]).", lang="en"),
    comments=Literal("For a browser of [efo:] (v 2.95) terms, please see [http://purl.bioontology.org/ontology/EFO]; for a browser of [obi:] (v 2018-02-12) terms please see [http://purl.bioontology/ontology/OBI].", lang="en"),
    version_of_s="https://w3id.org/mixs/00000008",
)

createDP(
    name="0000012",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Broad-scale Environmental Context"),
    definition=Literal("In this field, report which major environmental system your sample or specimen came from. The systems identified should have a coarse spatial grain, to provide the general environmental context of where the sampling was done (e.g. were you in the desert or a rainforest?). We recommend using subclasses of ENVO’s biome class: [http://purl.obolibrary.org/obo/ENVO_00000428]. Format (one term): termLabel [termID], Format (multiple terms): termLabel [termID]|termLabel [termID]|termLabel [termID]. Example: Annotating a water sample from the photic zone in middle of the Atlantic Ocean, consider: oceanic epipelagic zone biome [ENVO:01000033]. Example: Annotating a sample from the Amazon rainforest consider: tropical moist broadleaf forest biome [ENVO:01000228]. If needed, request new terms on the ENVO tracker, identified here: [http://www.obofoundry.org/ontology/envo.html].", lang="en"),
    examples=[
        Literal("oceanic epipelagic zone biome [ENVO:01000033]"),
        Literal("tropical moist broadleaf forest biome [ENVO:01000228]"),
    ],
    version_of_s="https://w3id.org/mixs/0000012",
)

createDP(
    name="0000013",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Local Environmental Context"),
    definition=Literal("In this field, report the entity or entities which are in your sample or specimen's local vicinity and which you believe have significant causal influences on your sample or specimen. Please use terms that are present in [envo:] and which are of smaller spatial grain than your entry for [mixs:env_broad_scale]. Format (one term): termLabel [termID]; Format (multiple terms): termLabel [termID]|termLabel [termID]|termLabel [termID]. Example: Annotating a pooled sample taken from various vegetation layers in a forest consider: canopy [ENVO:00000047]|herb and fern layer [ENVO:01000337]|litter layer [ENVO:01000338]|understory [01000335]|shrub layer [ENVO:01000336]. If needed, request new terms on the ENVO tracker, identified here: [http://www.obofoundry.org/ontology/envo.html].", lang="en"),
    examples=[
        Literal("canopy [ENVO:00000047]|herb and fern layer [ENVO:01000337]|litter layer [ENVO:01000338]|understory [01000335]|shrub layer [ENVO:01000336]"),
    ],
    version_of_s="https://w3id.org/mixs/0000013",
)

createDP(
    name="0000014",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=[XSD["string"]],
    pref_label=Literal("Environmental Medium"),
    definition=Literal("In this field, report which environmental material or materials (pipe separated) immediately surrounded your sample or specimen prior to sampling, using one or more subclasses of ENVO’s environmental material class: [http://purl.obolibrary.org/obo/ENVO_00010483]. Format (one term): termLabel [termID]; Format (multiple terms): termLabel [termID]|termLabel [termID]|termLabel [termID]. Example: Annotating a fish swimming in the upper 100 m of the Atlantic Ocean, consider: ocean water [ENVO:00002151]. Example: Annotating a duck on a pond consider: pond water [ENVO:00002228]|air ENVO_00002005. If needed, request new terms on the ENVO tracker, identified here: [http://www.obofoundry.org/ontology/envo.html].", lang="en"),
    examples=[
        Literal("ocean water [ENVO:00002151]"),
        Literal("pond water [ENVO:00002228]|air ENVO_00002005"),
    ],
    version_of_s="https://w3id.org/mixs/0000014",
)

# WARN: I added the comment to be clearer
createEDP(
    name="0000015",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    one_of=[
        Literal("aerobe"),
        Literal("anaerobe"),
        Literal("facultative"),
        Literal("microaerophilic"),
        Literal("microanaerobe"),
        Literal("obligate aerobe"),
        Literal("obligate anaerobe")
    ],
    pref_label=Literal("Relation To Oxygen"),
    definition=Literal("Is this organism an aerobe, anaerobe? Please note that aerobic and anaerobic are valid descriptors for microbial environments.", lang="en"),
    comments=Literal("This property only takes a finite set of possible literal values. For more details, see: [https://genomicsstandardsconsortium.github.io/mixs/RelToOxygenEnum/]", lang="en"),
    examples=[
        Literal("aerobe"),
    ],
    version_of_s="https://w3id.org/mixs/0000015",
)

# WARN: MiXS page has no mention of OBI.
createDP(
    name="0000016",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Sample Material Processing"),
    definition=Literal("A brief description of any processing applied to the sample during or after retrieving the sample from environment, or a link to the relevant protocol(s) performed.", lang="en"),
    examples=[
        Literal("filtering of seawater, storing samples in ethanol"),
    ],
    version_of_s="https://w3id.org/mixs/0000016",
)

createDP(
    name="0000017",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Size Fraction Selected"),
    definition=Literal("Filtering pore size used in sample preparation.", lang="en"),
    examples=[
        Literal("0-0.22 micrometer"),
    ],
    version_of_s="https://w3id.org/mixs/0000017",
)

createDP(
    name="0000020",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Subspecific Genetic Lineage"),
    definition=Literal("This should provide further information about the genetic distinctness of the sequenced organism by recording additional information e.g. serovar, serotype, biotype, ecotype, or any relevant genetic typing schemes like Group I plasmid. It can also contain alternative taxonomic information. It should contain both the lineage name, and the lineage rank, i.e. `biovar:abc123`.", lang="en"),
    examples=[
        Literal("serovar:Newport"),
    ],
    version_of_s="https://w3id.org/mixs/0000020",
)






createDP(
    name="0000021",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Ploidy"),
    definition=Literal("The ploidy level of the genome (e.g. `allopolyploid`, `haploid`, `diploid`, `triploid`, `tetraploid`). It has implications for the downstream study of duplicated gene and regions of the genomes (and perhaps for difficulties in assembly). For terms, please select terms listed under class ploidy ([pato:001374]) of Phenotypic Quality Ontology ([pato:]), and for a browser of PATO (v 2018-03-27) please refer to [http://purl.bioontology.org/ontology/PATO].", lang="en"),
    examples=[
        Literal("allopolyploidy [PATO:0001379]"),
    ],
    version_of_s="https://w3id.org/mixs/0000021",
)

createDP(
    name="0000022",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["integer"],
    pref_label=Literal("Number Of Replicons"),
    definition=Literal("Reports the number of replicons in a nuclear genome of eukaryotes, in the genome of a bacterium or archaea or the number of segments in a segmented virus. Always applied to the haploid chromosome count of a eukaryote.", lang="en"),
    examples=[
        Literal("2", datatype=XSD["integer"]),
    ],
    version_of_s="https://w3id.org/mixs/0000022",
)

createDP(
    name="0000023",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["integer"],
    pref_label=Literal("Extrachromosomal Elements"),
    definition=Literal("Do plasmids exist of significant phenotypic consequence (e.g. ones that determine virulence or antibiotic resistance). Megaplasmids? Other plasmids (borrelia has 15+ plasmids).", lang="en"),
    examples=[
        Literal("5", datatype=XSD["integer"]),
    ],
    version_of_s="https://w3id.org/mixs/0000023",
)

createDP(
    name="0000024",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=XSD["string"],
    pref_label=Literal("Estimated size"),
    definition=Literal("The estimated size of the genome prior to sequencing. Of particular importance in the sequencing of (eukaryotic) genome which could remain in draft form for a long or unspecified period.", lang="en"),
    examples=[
        Literal("300000 bp"),
    ],
    version_of_s="https://w3id.org/mixs/0000024",
)








createDP(
    name="0000092",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Project Name"),
    definition=Literal("Name of the project within which the sequencing was organized.", lang="en"),
    version_of_s="https://w3id.org/mixs/0000092",
)

createDP(
    name="0001107",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Sample Name"),
    definition=Literal("Sample Name is a name that you choose for the sample. It can have any format, but we suggest that you make it concise, unique and consistent within your lab, and as informative as possible. Every Sample Name from a single Submitter must be unique.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001107",
)

createDP(
    name="0001320",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Taxonomy ID Of DNA Sample"),
    definition=Literal("NCBI taxon ID of the sample. May be a single taxon or mixed taxa sample. Use \"synthetic metagenome\" for mock community positive controls, or \"blank sample\" for negative controls.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001320",
)

createDP(
    name="0001321",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Negative Control Type"),
    definition=Literal("The substance or equipment used as a negative control in an investigation.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001321",
)

createDP(
    name="0001322",
    namespace=MIXS,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Positive Control Type"),
    definition=Literal("The substance, mixture, product, or apparatus used to verify that a process which is part of an investigation delivers a true positive.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001322",
)

createDP(
    name="CreateDate",
    namespace=XMP,
    graph=g,
    domains=DWC["MolecularProtocol"],
    ranges=RDFS["Literal"],
    pref_label=Literal("Original Date and Time"),
    definition=Literal("The date and time a resource was created. For a digital file, this need not match a file-system creation time. For a freshly created resource, it should be close to that time, modulo the time taken to write the file. Later file transfer, copying, and so on, can make the file-system time arbitrarily different.", lang="en"),
    comments=Literal("The date of the creation of the original resource from which the digital media was derived or created. The date and time MUST comply with the World Wide Web Consortium (W3C) datetime practice, [https://www.w3.org/TR/NOTE-datetime], which requires that date and time representation correspond to ISO 8601:1998, but with year fields always comprising 4 digits. This makes datetime records compliant with 8601:2004, [https://www.iso.org/standard/40874.html]. [ac:] datetime values MAY also follow 8601:2004 for ranges by separating two IS0 8601 datetime fields by a solidus (\"forward slash\", '/'). When applied to a media resource with temporal extent such as audio or video, this property indicates the startTime of the recording. What constitutes \"original\" is determined by the metadata author. Example: Digitization of a photographic slide of a map would normally give the date at which the map was created; however a photographic work of art including the same map as its content may give the date of the original photographic exposure. Imprecise or unknown dates can be represented as ISO dates or ranges. Compare also Date and Time Digitized in the Resource Creation Vocabulary. See also the wikipedia IS0 8601 entry, [https://en.wikipedia.org/wiki/ISO_8601], for further explanation and examples.", lang="en"),
    version_of_s="http://ns.adobe.com/xap/1.0/CreateDate",
)

#####################################################################################################
# BEGIN OWL API USAGE
#####################################################################################################

# Serialize the ontology to xml.
# g.serialize(destination="dwc-owl.owl", format="pretty-xml")
g.serialize(destination="dwc-owl.ttl", format="turtle")

# NOTE: Use ROBOT to use the OWL API directly, better than having to go into Protege everytime.
# Obtained with curl -L -o robot.jar https://github.com/ontodev/robot/releases/download/v1.9.8/robot.jar
# Put in .gitgnore since it is borderline LFS.
#
subprocess.run(["java", "-jar", "jarfiles/robot.jar", "convert", "--input", "dwc-owl.ttl", "--output", "dwc-owl-v2.ttl"])

#####################################################################################################
# BEGIN PYLODE DOCUMENTATION GENERATION
#####################################################################################################

# 
od = OntPub(ontology=g, sort_subjects=True)
#od = OntPub(ontology=g, sort_subjects=False)

# Write html documentation to docs directory
#
od.make_html(destination="docs/index.html", include_css=True)

#####################################################################################################
# BEGIN HERMIT TEST EXECUTION
#####################################################################################################

subprocess.run(["python3", "tests/hermit_tests.py"])
