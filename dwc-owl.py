#####################################################################################################
# BEGIN IMPORTS
#####################################################################################################

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD
#
from utils import createOC, createDP, createOP, create_CTOP, declare_disjoint
#
import subprocess

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
DWCIRI = Namespace("http://rs.tdwg.org/dwc/iri/")
DWCDP = Namespace("http://rs.tdwg.org/dwcdp/terms/")
ECO = Namespace("http://rs.tdwg.org/eco/terms")
EXIF = Namespace("http://ns.adobe.com/exif/1.0/")
GBIF = Namespace("http://rs.gbif.org/terms/")
GGBN = Namespace("http://data.ggbn.org/schemas/ggbn/terms/")
MIQE = Namespace("http://rs.gbif.org/terms/miqe/")
MIXS = Namespace("https://w3id.org/mixs/")
XMP = Namespace("http://ns.adobe.com/xap/1.0/")

g = Graph()
g.bind("ac", AC)
g.bind("adms", ADMS)
g.bind("bibo", BIBO)
g.bind("chrono", CHRONO)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)
g.bind("dwc", DWC)
g.bind("dwciri", DWCIRI)
g.bind("dwcdp", DWCDP)
g.bind("eco", ECO)
g.bind("exif", EXIF)
g.bind("gbif", GBIF)
g.bind("ggbn", GGBN)
g.bind("miqe", MIQE)
g.bind("mixs", MIXS)

# Define ontology URI and basic definitions.
ontology_uri = URIRef("http://bioboum.ca/dwc-owl.owl")
g.add((ontology_uri, RDF.type, OWL.Ontology))
g.add((ontology_uri, OWL.versionInfo, Literal("0.0.2")))
g.add((ontology_uri, DC["title"], Literal("Darwin Core OWL")))
g.add((ontology_uri, DC["description"], Literal("Darwin Core OWL is an attempt to use Darwin Core terms and the newly proposed Darwin Core DataPackage terms and convert them into OWL concepts of classes and properties. Darwin Semantic Web already considered this, considering OWL classes. The purpose here is to consider OWL classes that considers owl:Restrictions. As well as owl:ObjectProperties that can link together the entities, so that we obtain a web of rather than a simple flat RDF representation of biodiversity datasets.", lang="en")))


#####################################################################################################
# BEGIN OWL CLASS DEFINITIONS
#####################################################################################################

# NOTE: RECHECK terms in example.
createOC(
    name="Media",
    namespace=AC,
    graph=g,
    pref_label=Literal("Media"),
    definition=Literal("A [dcmi:MediaType] or other media type with other entities as subject matter.", lang="en"),
    comments=Literal("An instance of digital textual media may be better represented as a [dcterms:BibliographicResource].", lang="en"),
    examples=Literal("`dcmi:Sound`; `dcmi:StillImage`; `dcmi:MovingImage`"),
    # card01_restrictions=[AC["captureDevice"], AC["digitizationDate"], AC["frameRate"], AC["heightFrac"], AC["widthFrac"], XMP["CreateDate"]],
    card0_restrictions=[AC["radius"]],
    version_of_s="http://rs.tdwg.org/ac/terms/Media",
)

# BUG: I put in the error owl:Restriction. HermiT in Protege picks up on it, but not the default settings in owlready2. Though running the HermiT .jar file bundled with owlready2 gives the inconsistency. Beware.
createOC(
    name="Agent",
    namespace=DCTERMS,
    graph=g,
    pref_label=Literal("Agent"),
    definition=Literal("A resource that acts or has the power to act.", lang="en"),
    comments=Literal("A person, group, organization, machine, software or other entity that can act. Membership in the [dcterms:Agent] class is determined by the capacity to act, even if not doing so in a specific context. To act: To participate in an event or process by contributing through behavior, operation, or an effect resulting from active participation — regardless of whether that contribution is intentional, volitional, or conscious.", lang="en"),
    examples=Literal("`Carl Linnaeus`; `The Terra Nova Expedition`; `The National Science Foundation`; `The El Yunque National Forest ARBIMON System`; `ChatGPT`"),
    # card1_restrictions=[DWC["agentID"], DWC["agentType"], DWC["eventID"]],
    card1_restrictions=[DWC["agentID"], DWC["agentType"]],
    card01_restrictions=[DWC["agentRemarks"], DWC["preferredAgentName"]],
    version_of_s="http://purl.org/dc/terms/Agent",
)

# NOTE: REVOIR VERSION
createOC(
    name="Assertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Assertion"),
#    card1_restrictions=[DWCDP.agentType], # WAS A TEST
    card0_restrictions=[DWCDP["assertedBy"]],
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
    examples=Literal("`an age range associated with a specimen derived from an AMS dating assay applied to an oyster shell in the same stratum`; `an age range associated with a specimen derived from a ceramics analysis based on other materials found in the same stratum`; `a maximum age associated with a specimen derived from K-Ar dating applied to a proximal volcanic tuff found stratigraphically below the specimen`; `an age range of a specimen based on its biostratigraphic content`; `an age of a specimen based on what is reported in legacy collections data`"),
    version_of_s="http://rs.tdwg.org/chrono/terms/ChronometricAge",
    references_s="http://rs.tdwg.org/chrono/terms/version/ChronometricAge-2021-02-21",
)

# NOTE: Should we allow for several parent events?
createOC(
    name="Event",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Event"),
    definition=Literal("An action, process, or set of circumstances occurring at a [dcterms:Location] during a period of time.", lang="en"),
    examples=Literal("`a material collecting event`; `a bird observation`; `a camera trap image capture`; `an organism occurrence`; `a biotic survey`"),
    card1_restrictions=[DWC["eventID"]],
    card0_restrictions=[DWCDP["happenedDuring"]],
    card01_restrictions=[DWC["preferredEventName"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/Event",
    references_s="http://rs.tdwg.org/dwc/terms/version/Event-2023-09-18",
)

createOC(
    name="GeologicalContext",
    namespace=DWC,
    graph=g,
    pref_label=Literal("GeologicalContext"),
    definition=Literal("A set of geological designations, such as stratigraphy, that qualifies a [dcterms:Location].", lang="en"),
    examples=Literal("`a particular lithostratigraphic layer`; `a specific chronostratigraphic unit`", lang="en"),
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
    examples=Literal("`a subspecies determination of an organism`; `a nomenclatural act designating a specimen as a holotype`"),
    version_of_s="http://rs.tdwg.org/dwc/terms/Identification",
    references_s="http://rs.tdwg.org/dwc/terms/version/Identification-2023-09-18",
)

createOC(
    name="Location",
    namespace=DCTERMS,
    graph=g,
    pref_label=Literal("Location"),
    definition=Literal("A spatial region or named place.", lang="en"),
    examples=Literal("`the municipality of San Carlos de Bariloche, Río Negro, Argentina`; `the place defined by a georeference`"),
    version_of_s="http://purl.org/dc/terms/Location",
)

createOC(
    name="MaterialEntity",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Material Entity"),
    definition=Literal("An entity that can be identified, exist for some period of time, and consist in whole or in part of physical matter while it exists.", lang="en"),
    comments=Literal("The term is defined at the most general level to admit descriptions of any subtype of material entity within the scope of Darwin Core. In particular, any kind of material sample, preserved specimen, fossil, or exemplar from living collections is intended to be subsumed under this term.", lang="en"),
    examples=Literal("`the entire contents of a trawl`; `a subset of the contents of a trawl`; `the body of a fish`; `the stomach contents of a fish`; `a rock containing fossils`; `a fossil within a rock`; `an herbarium sheet with its attached plant speciment`; `a flower on a plant specimen`; `a pollen grain`; `a specific water sample`; `an isolated molecule of DNA`"),
    version_of_s="http://rs.tdwg.org/dwc/terms/MaterialEntity",
    references_s="http://rs.tdwg.org/dwc/terms/version/MaterialEntity-2023-09-13",
)

# WARN: Add triples to express owl:Restriction here then integrate to function

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
    card1_restrictions=[DWC["eventID"], DWC["molecularProtocolID"], DWC["nucleotideAnalysisID"], DWC["nucleotideSequenceID"]],
    card01_restrictions=[DWC["materialEntityID"], DWC["readCount"], DWC["totalReadCount"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/NucleotideAnalysis",
)

createOC(
    name="NucleotideSequence",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Nucleotide Sequence"),
    definition=Literal("A digital representation of a nucleotide sequence.", lang="en"),
    card1_restrictions=[DWC["nucleotideSequenceID"], DWC["sequence"]],
    card0_restrictions=[DWC["nucleotideSequenceRemarks"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/NucleotideSequence",
)

createOC(
    name="Occurrence",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Occurrence"),
    definition=Literal("A state of a [dwc:Organism] in a [dwc:Event].", lang="en"),
    examples=Literal("`a wolf pack on the shore of Kluane Lake in 1988`; `a virus in a plant leaf in the New York Botanical Garden at 15:29 on 2014-10-23`; `a fungus in Central Park in the summer of 1929`"),
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
    examples=Literal("`a specific bird`; `a specific wolf pack`; `a specific instance of a bacterial culture`"),
    card1_restrictions=[DWC["organismID"]],
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
    examples=Literal("`a bee visiting a flower`; `a *Mallophora ruficauda* hunting an *Apis mellifera* in flight`; `a viral infection in a plant`; `a female spider mating with a male spider`; `a lion cub nursing from its mother`; `a mosquito sucking blood from a chimpanzee's arm`; `a slug eating a fungus growing on a decomposing stump` (2 interactions)"),
    card1_restrictions=[DWC["organismInteractionID"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/OrganismInteraction",
)

createOC(
    name="Protocol",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Protocol"),
    definition=Literal("A method used during an action.", lang="en"),
    examples=Literal("`a pitfall method for sampling ground-dwelling arthropods`; `a point-radius georeferencing method`; `a linear regression model to estimate body mass from skeletal measurements`; `a Bayesian phylogenetic inference method`"),
    version_of_s="http://rs.tdwg.org/dwc/terms/Protocol",
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
    examples=Literal("`an instance of a [dwc:Organism] is the mother of another instance of a [dwc:Organism]`; `a uniquely identified [dwc:Occurrence] represents the same [dwc:Occurrence] as another uniquely identified [dwc:Occurrence]`; `a [dwc:MaterialEntity] is a subsample of another [dwc:MaterialEntity]`"),
    version_of_s="http://rs.tdwg.org/dwc/terms/ResourceRelationship",
    references_s="http://rs.tdwg.org/dwc/terms/version/ResourceRelationship-2023-09-13",
)

createOC(
    name="UsagePolicy",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Usage Policy"),
    definition=Literal("Information about rights, usage, and attribution statements applicable to an entity.", lang="en"),
    comments=Literal("This is a convenience class to group related properties.", lang="en"),
    card1_restrictions=[DWC["usagePolicyID"]],
    card01_restrictions=[DC["rights"], DCTERMS["rights"]],
    version_of_s="http://rs.tdwg.org/dwc/terms/UsagePolicy",
)

createOC(
    name="Survey",
    namespace=ECO,
    graph=g,
    pref_label=Literal("Survey"),
    definition=Literal("A biotic survey or inventory.", lang="en"),
    comments=Literal("This class includes properties found in the Humboldt Extension to Darwin Core ([eco:]), except for target scope terms, which can be accomodated in [eco:SurveyTarget].", lang="en"),
    examples=Literal("`a botanical survey of a protected area to assess native and invasive plant species`; `a wetland vegetation mapping`; `a camera trap deployment in a rainforest to monito large mammals`; `a frog call survey in wetlands across breeding seasons`; `a coverboard survey for reptiles in forested environments`; `a pollinator survey in an agricultural landscape`; `a macroinvertebrate sampling in a freshwater stream to assess water quality`; `a habitat- or ecosystem-level survey` (e.g. `coral reef health assessment`, `forest biodiversity assessment`); `an environmental impact assessment` (e.g. `pre-construction baseline survey for a wind farm project`)"),
    card1_restrictions=[DWC["eventID"], DWC["surveyID"]],
    version_of_s="http://rs.tdwg.org/eco/terms/Survey",
)

createOC(
    name="SurveyTarget",
    namespace=ECO,
    graph=g,
    pref_label=Literal("Survey Target"),
    definition=Literal("An intended scope for [dwc:Occurrence]s in a [eco:Survey].", lang="en"),
    examples=Literal("`all bird species`; `all bird species except *Larus* gulls, fulmars and kittiwakes`; reproductive female *Ctenomys sociabilis* (only)`; `*Oncorhynchus mykiss* and *Oncorhynchus clarkii* (only)`; `all total lengths except < 12 inches`"),
    card1_restrictions=[DWC["surveyID"], DWC["surveyTargetID"]],
    version_of_s="http://rs.tdwg.org/eco/terms/SurveyTarget",
)

#####################################################################################################
# BEGIN CLASSES THROUGH OBJECT PROPERTY DEFINITIONS
#####################################################################################################

create_CTOP(
    name="AssertionAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Assertion Agent"),
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["assertedBy"],
    use_inverse=True,
    values_class=DWC["Assertion"],
    definition=Literal("An instance of a [dcterms:Agent] that has made a [dwc:Assertion]."),
    comments=Literal("Due to the directionality of the property [dwcdp:assertedBy], the class is defined in description logic as [dwcdp:AssertionAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:assertedBy]⁻).[dwc:Assertion].")
)

create_CTOP(
    name="AuthorAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Author Agent"),
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["authoredBy"],
    use_inverse=True,
    values_class=DCTERMS["BibliographicResource"],
    definition=Literal("An instance of a [dcterms:Agent] that has authored a [dcterms:BibliographicResource]."),
    comments=Literal("Due to the directionality of the property [dwcdp:authoredBy], the class is defined in description logic as [dwcdp:AuthorAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:authoredBy]⁻).[dcterms:BibliographicResource].")
)

create_CTOP(
    name="CommenterAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Commenter Agent"),
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["commentedBy"],
    use_inverse=True,
    values_class=AC["Media"],
    definition=Literal("An instance of a [dcterms:Agent] that has commented a [dwc:Media]."),
    comments=Literal("Due to the directionality of the property [dwcdp:commentedBy], the class is defined in description logic as [dwcdp:Commenter] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:commentedBy]⁻).[dwc:Media].")
)

create_CTOP(
    name="ConductorAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Conductor Agent"),
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["conductedBy"],
    use_inverse=True,
    values_class=DWC["Event"],
    definition=Literal("An instance of a [dcterms:Agent] that has conducted a [dwc:Event]."),
    comments=Literal("Due to the directionality of the property [dwcdp:conductedBy], the class is defined in description logic as [dwcdp:Conductor] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:conductedBy]⁻).[dwc:Event].")
)

# NOTE: Used bibo: property bibo:editor.
create_CTOP(
    name="EditorAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Editor Agent"),
    subclass_list=[DCTERMS["Agent"]],
    # object_prop=DWCDP.editedBy,
    object_prop=BIBO["editor"],
    use_inverse=True,
    values_class=DCTERMS["BibliographicResource"],
    definition=Literal("An instance of a [dcterms:Agent] that has edited a [dcterms:BibliographicResource]."),
    comments=Literal("Due to the directionality of the property [dwcdp:editedBy], the class is defined in description logic as [dwcdp:EditorAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:editedBy]⁻).[dcterms:BibliographicResource].")
)

create_CTOP(
    name="GeoreferencerAgent",
    namespace=DWC,
    graph=g,
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["georeferencedBy"],
    values_class=DWC["Event"],
    use_inverse=True,
    pref_label=Literal("Georeferencer Agent"),
    definition=Literal("An instance of a [dcterms:Agent] that has georeferenced a [dwc:Event]."),
    comments=Literal("Due to the directionality of the property [dwcdp:georeferencedBy], the class is defined in description logic as [dwcdp:Georeferencer] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:georeferencedBy]⁻).[dwc:Event].")
)

# NOTE: An important one to me (and the origin of the whole group of XYZAgents). Came to me during a discussion with Andre Heughebaert. Someone might want to explicitly exclude all observations where identifications were done by AI.
create_CTOP(
    name="IdentificationAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Identification Agent"),
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["identifiedBy"],
    use_inverse=True,
    values_class=DWC["Identification"],
    definition=Literal("An instance of a [dcterms:Agent] that has published a [dwc:Identification]."),
    comments=Literal("Due to the directionality of the property [dwcdp:identifiedBy], the class is defined in description logic as [dwcdp:IdentificationAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:identifiedBy]⁻).[dwc:Identification].")
)

create_CTOP(
    name="PublisherAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Publisher Agent"),
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["publishedBy"],
    use_inverse=True,
    values_class=DCTERMS["BibliographicResource"],
    definition=Literal("An instance of a [dcterms:Agent] that has published a [dcterms:BibliographicResource]."),
    comments=Literal("Due to the directionality of the property [dwcdp:publishedBy], the class is defined in description logic as [dwcdp:PublisherAgent] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:publishedBy]⁻).[dcterms:BibliographicResource].")
)

create_CTOP(
    name="ReviewerAgent",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Reviewer Agent"),
    subclass_list=[DCTERMS["Agent"]],
    object_prop=DWCDP["reviewedBy"],
    use_inverse=True,
    values_class=AC["Media"],
    definition=Literal("An instance of a [dcterms:Agent] that has reviewed a [dwc:Media]."),
    comments=Literal("Due to the directionality of the property [dwcdp:reviewedBy], the class is defined in description logic as [dwcdp:Reviewer] ≡ [dcterms:Agent] ⊓ ∃([dwcdp:reviewedBy]⁻).[dwc:Media].")
)


###############################################################################################


create_CTOP(
    name="EventAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Event Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=DWC["Event"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:Event]."),
)

create_CTOP(
    name="ChronometricAgeAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Chronometric Age Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=CHRONO["ChronometricAge"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:ChronometricAge]."),
)


create_CTOP(
    name="MaterialEntityAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Material Entity Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=DWC["MaterialEntity"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:MaterialEntity]."),
)

create_CTOP(
    name="MediaAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Media Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=AC["Media"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:Media]."),
)

create_CTOP(
    name="NucleotideAnalysisAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Nucleotide Analysis Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=DWC["NucleotideAnalysis"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:NucleotideAnalysis]."),
)

create_CTOP(
    name="OrganismAssertion",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Nucleotide Analysis Assertion"),
    subclass_list=[DWC["Assertion"]],
    object_prop=DWCDP["about"],
    use_inverse=False,
    values_class=DWC["Organism"],
    definition=Literal("A [dwc:Assertion] made by a [dcterms:Agent] about a [dwc:Organism]."),
)



##########################################################



create_CTOP(
    name="AssertionProtocol",
    namespace=DWCDP,
    graph=g,
    pref_label=Literal("Assertion Protocol"),
    subclass_list=[DWC["Protocol"]],
    object_prop=DWCDP["followed"],
    use_inverse=True,
    values_class=DWC["Assertion"],
    definition=Literal("A [dwc:Protocol] followed by a [dcterms:Agent] for a [dwc:Assertion]."),
    comments=Literal("Due to the directionality of the property [dwcdp:followed], the class is defined in description logic as [dwc:EventProtocol] ≡ [dwc:Protocol] ⊓ ∃([dwcdp:followed]⁻).[dwc:Assertion].")
)

# GOOD COMPLEX EXAMPLE
# BEFORE AFTER ADD
create_CTOP(
    name="EventProtocol",
    namespace=DWCDP,
    graph=g,
    pref_label=Literal("Event Protocol"),
    subclass_list=[DWC["Protocol"]],
    object_prop=DWCDP["followed"],
    use_inverse=True,
    values_class=DWC["Event"],
    definition=Literal("A [dwc:Protocol] followed by a [dcterms:Agent] for a [dwc:NucleotideAnalysis]."),
    comments=Literal("Due to the directionality of the property [dwcdp:followed], the class is defined in description logic as [dwc:EventProtocol] ≡ [dwc:Protocol] ⊓ ∃([dwcdp:followed]⁻).[dwc:Event].")
)

# NOTE: Particularly important one. It is the only dwc:Protocol that is the domain of the properties from GBIF, MIQUE, MIXS, et al.
create_CTOP(
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
    card01_restrictions=[DWC["assayType"], MIXS["0000008"], MIXS["0000092"], MIXS["0001107"], MIXS["0001320"]]
)

##############################################


# NOTE: owl:inverseFunction test
create_CTOP(
    name="EventMedia",
    namespace=DWC,
    graph=g,
    pref_label=Literal("Event Media"),
    subclass_list=[AC["Media"]],
    object_prop=DWCDP["isMediaOf"],
    use_inverse=False,
    values_class=DWC["Event"],
    definition=Literal("A [ac:Media] about a [dwc:Event]."),
)

g.add((DWCDP["hasMedia"], OWL["inverseOf"], DWCDP["isMediaOf"]))


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



    # # Optionally add examples.
    # if examples:
    #     graph.add((class_uri, SKOS.example, examples))

    # if use_inverse == True:
    #     # InvBlank
    #     property_node  = BNode()
    #     graph.add((property_node , RDF.type, OWL.ObjectProperty))
    #     graph.add((property_node , OWL.inverseOf, object_prop))
    # else:
    #     property_node = object_prop

    # # OWL Restrictions
    # R_class = BNode()
    # graph.add((R_class, RDF.type, OWL.Restriction))
    # graph.add((R_class, OWL.onProperty, property_node ))
    # graph.add((R_class, OWL.someValuesFrom, values_class))

    # # owl:equivalentClass via owl:intersectionOf
    # #graph.add((class_uri, RDFS.subClassOf, R_class))
    # graph.add((class_uri, OWL.equivalentClass, R_class))




#####################################################################################################
# BEGIN AXIOMS
#####################################################################################################


# NOTE: Can a dwc:Event be a eco:Survey?
# declare_disjoint(
#     classes=[DCTERMS["Agent"], DCTERMS["Location"], AC["Media"], DWC["Assertion"], DWC["Event"], DWC["GeologicalContext"], DWC["MaterialEntity"], DWC["NucleotideAnalysis"], DWC["NucleotideSequence"], DWC["Occurrence"], DWC["Protocol"], DWC["UsagePolicy"], ECO["Survey"], ECO["SurveyTarget"]],
#     graph=g
# )

declare_disjoint(
    classes=[CHRONO["ChronometricAge"], DCTERMS["Agent"], DCTERMS["Location"], AC["Media"], DWC["Assertion"], DWC["Event"], DWC["GeologicalContext"], DWC["MaterialEntity"], DWC["NucleotideAnalysis"], DWC["NucleotideSequence"], DWC["Occurrence"], DWC["Organism"], DWC["OrganismInteraction"], DWC["Protocol"], DWC["ResourceRelationship"], DWC["UsagePolicy"], ECO["Survey"], ECO["SurveyTarget"]],
    graph=g
)
#####################################################################################################
# BEGIN OBJECT PROPERTY DEFINITIONS
#####################################################################################################

createOP(
    name="about",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[AC["Media"], CHRONO["ChronometricAge"], DWC["Event"], DWC["MaterialEntity"], DWC["NucleotideAnalysis"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Assertion] to the object it is about. This object can be a [chrono:ChronometricAge], [dwc:Event], [dwc:MaterialEntity], [dwc:Media], [dwc:NucleotideAnalysis]."),
    examples=Literal("bb:assertion123 dwcdp:about bb:event456 .")
)

createOP(
    name="assertedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Assertion] to the [dcterms:Agent] that asserted it."),
    examples=Literal("bb:assertion123 dwcdp:assertedBy bb:agent456 ."),
)

createOP(
    name="authoredBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DCTERMS["BibliographicResource"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that authored it."),
    examples=Literal("bb:bibliographicResource123 dwcdp:authoredBy bb:agent456 .")
)

# NOTE: Can an dwc:Identification be dwcdp:basedOn a dwc:NucleotideAnalysis? I thought it was logically possible through the dwc:NucleotideSequence it produced? If so, why not have the same for dwc:Event and dwc:Occurrence?
createOP(
    name="basedOn",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Identification"]],
    range_list=[AC["Media"], DWC["MaterialEntity"], DWC["NucleotideAnalysis"], DWC["NucleotideSequence"], DWC["Occurrence"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Identification] to the entity on which it is based. These entities include [ac:Media], [dwc:MaterialEntity], [dwc:NucleotideAnalysis], [dwc:NucleotideSequence] and [dwc:Occurrence]."),
    examples=Literal("bb:identification123 dwcdp:basedOn bb:nucleotideSequence456 ."),
)


createOP(
    name="commentedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Media] to the [dcterms:Agent] that commented it."),
    examples=Literal("bb:event123 dwcdp:commentedBy bb:agent456 .")
)

createOP(
    name="conductedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Event"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Event] to the [dcterms:Agent] that conducted it."),
    examples=Literal("bb:event123 dwcdp:conductedBy bb:agent456 .")
)

# NOTE: Could be redundant to bibo:editor, but bibo:editor has a domain of bibo:Document, not dcterms:BibliographicResource, so resources would need to be declared as both.
# NOTE: I imagine this is related to the OWA.
# createOP(
#     name="editedBy",
#     namespace=DWCDP,
#     graph=g,
#     domain_list=[DCTERMS["BibliographicResource"]],
#     range_list=[DCTERMS["Agent"]],
#     definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that edited it."),
#     examples=Literal("bb:bibliographicResource123 dwcdp:editedBy bb:agent456 .")
# )
#
createOP(
    name="editor",
    namespace=BIBO,
    graph=g,
    domain_list=[DCTERMS["BibliographicResource"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that edited it.", lang="en"),
    comments=Literal("A person having managerial and sometimes policy-making responsibility for the editorial part of a publishing firm or of a newspaper, magazine, or other publication.", lang="en"),
    examples=Literal("bb:bibliographicResource123 bibo:editor bb:agent456 .")
)


createOP(
    name="followed",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Assertion"], DWC["Event"], DWC["NucleotideAnalysis"]],
    range_list=[DWC["Protocol"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a resource to the [dwc:Protocol] it followed. These resources can be varied and include [dwc:Event], [dwc:NucleotideAnalysis]"),
    examples=Literal("bb:event123 dwcdp:followed bb:protocol456 ."),
)

# WARN: Later link to subclasses of dwc:Protocol to avoid cross-class usage of the term.
g.add((DWCDP["usedFor"], OWL["inverseOf"], DWCDP["followed"]))


createOP(
    name="georeferencedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Event"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Event] to the [dwc:Agent] that georeferenced it."),
    examples=Literal("bb:event123 dwcdp:georeferencedBy bb:agent456 ."),
)

# WARN: Change definition.
createOP(
    name="happenedDuring",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Event"], DWC["Occurrence"], DWC["OrganismInteraction"], ECO["Survey"]],
    range_list=[DWC["Event"]],
    additional_list=[OWL["TransitiveProperty"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Event] to its parent [dwc:Event]."),
    comments=Literal("This property is also an [owl:TransitiveProperty], which allows reasoners to infer hierarchical sampling patterns."),
    examples=Literal("bb:event123 dwcdp:happenedDuring bb:event456 ."),
)

createOP(
    name="hasMedia",
    namespace=DWCDP,
    graph=g,
    domain_list=[CHRONO["ChronometricAge"], DCTERMS["Agent"], DWC["Event"], DWC["GeologicalContext"], DWC["MaterialEntity"], DWC["Occurrence"], DWC["OrganismInteraction"]],
    range_list=[AC["Media"]],
    definition=Literal("An [owl:ObjectProperty] used to relate an entity to an instance of [ac:Media]. These entities can be [chrono:ChronometricAge], [dcterms:Agent], [dwc:Event], [dwc:GeologicalContext], [dwc:MaterialEntity], [dwc:Occurrence], [dwc:OrganismInteraction]"),
    comments=Literal("This property also has a [owl:InverseProperty], [dwcdp:isMediaOf], which allows reasoners queries to go through different ways."),
    examples=Literal("bb:event123 dwcdp:hasMedia bb:media456 ."),
)

createOP(
    name="identifiedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Identification"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Identification] to the [dwc:Agent] that identified it."),
    examples=Literal("bb:identification123 dwcdp:identifiedBy bb:agent456 ."),
)

createOP(
    name="involves",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["Occurrence"]],
    range_list=[DWC["Organism"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Occurrence] to the [dwc:Organism] it involves."),
    examples=Literal("bb:occurrence123 dwcdp:involves bb:occurrence456 ."),
)

# NOTE: Recheck transitivity.
createOP(
    name="isDerivedFrom",
    namespace=DWCDP,
    graph=g,
    domain_list=[AC["Media"], DWC["MaterialEntity"]],
    range_list=[AC["Media"], DWC["MaterialEntity"]],
    additional_list=[OWL["TransitiveProperty"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a subject entity to the entity from which it was derived."),
    comments=Literal("Though the [rdf:domain] and [rdf:range] of this property are varied, [owl:Restriction]s on the classes prevent cross-class use of the term."),
    examples=Literal("bb:material123 dwcdp:isDerivedFrom bb:material456 ."),
)

createOP(
    name="isPartOf",
    namespace=DWCDP,
    graph=g,
    domain_list=[AC["Media"], DCTERMS["BibliographicResource"], DWC["MaterialEntity"]],
    range_list=[AC["Media"], DCTERMS["BibliographicResource"], DWC["MaterialEntity"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a subject entity to the entity from which it was derived."),
    comments=Literal("Though the [rdf:domain] and [rdf:range] of this property are varied, [owl:Restriction]s on the classes prevent cross-class use of the term."),
    examples=Literal("bb:material123 dwcdp:isPartOf bb:material456 ."),
)

createOP(
    name="materialCollectedDuring",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["NucleotideAnalysis"]],
    range_list=[DWC["Event"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:NucleotideAnalysis] to the [dwc:Event] from which the material was collected."),
    examples=Literal("bb:nucleotideAnalysis123 dwcdp:materialCollectedDuring bb:event456 ."),
)

createOP(
    name="ownedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["MaterialEntity"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:MaterialEntity] to the [dcterms:Agent] which owns it."),
    examples=Literal("bb:materialEntity123 dwcdp:ownedBy bb:agent456 .")
)

createOP(
    name="produced",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["NucleotideAnalysis"]],
    range_list=[DWC["NucleotideSequence"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:NucleotideSequence] to the [dwc:NucleotideAnalysis] that produced it."),
    examples=Literal("bb:nucleotideAnalysis123 dwcdp:basedOn bb:nucleotideSequence456 ."),
)

createOP(
    name="publishedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DCTERMS["BibliographicResource"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dcterms:BibliographicResource] to the [dcterms:Agent] that published it."),
    examples=Literal("bb:bibliographicResource123 dwcdp:publishedBy bb:agent456 .")
)

createOP(
    name="reviewedBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Media] to the [dcterms:Agent] that reviewed it."),
    examples=Literal("bb:event123 dwcdp:reviewedBy bb:agent456 .")
)

createOP(
    name="storedIn",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["MaterialEntity"]],
    range_list=[DCTERMS["Agent"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:MaterialEntity] to the [dcterms:Agent] in which it is stored."),
    examples=Literal("bb:materialEntity123 dwcdp:storedIn bb:agent456 .")
)


# NOTE: For the dwc:OrganismInteraction, preferably consider longer names and avoid reserved keywords.
createOP(
    name="interactionBy",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["OrganismInteraction"]],
    range_list=[DWC["Occurrence"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:OrganismInteraction] to the [dwc:Occurrence] it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the [dwc:Occurrence] considered by this property should be the subject of the statement.", lang="en"),
    examples=Literal("bb:RobberflyHuntingBee dwcdp:interactionBy bb:Robberfly123 ."),
)

# NOTE: For the dwc:OrganismInteraction, preferably consider longer names and avoid reserved keywords.
createOP(
    name="interactionWith",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["OrganismInteraction"]],
    range_list=[DWC["Occurrence"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:OrganismInteraction] to the [dwc:Occurrence] it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the [dwc:Occurrence] considered by this property should be the object of the statement.", lang="en"),
    examples=Literal("bb:RobberflyHuntingBee dwcdp:interactionWith bb:Bee456 ."),
)

# NOTE: For the dwc:ResourceRelationship, preferably consider longer names and avoid reserved keywords.
createOP(
    name="relationshipOf",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["ResourceRelationship"]],
    range_list=[DWC["Occurrence"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:OrganismInteraction] to the [dwc:Occurrence] it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the [dwc:Occurrence] considered by this property should be the subject of the statement.", lang="en"),
    examples=Literal("bb:RobberflyHuntingBee dwcdp:interactionBy bb:Robberfly123 ."),
)

# NOTE: For the dwc:ResourceRelationship, preferably consider longer names and avoid reserved keywords.
createOP(
    name="relationshipTo",
    namespace=DWCDP,
    graph=g,
    domain_list=[DWC["ResourceRelationship"]],
    range_list=[DWC["Occurrence"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:OrganismInteraction] to the [dwc:Occurrence] it involves.", lang="en"),
    comments=Literal("To keep the interaction terms semantically correct and in order, the [dwc:Occurrence] considered by this property should be the object of the statement.", lang="en"),
    examples=Literal("bb:RobberflyHuntingBee dwcdp:interactionWith bb:Bee456 ."),
)

# NOTE: Seems like an important one, could be worthwhile to just use the dcterms: version of the property rather than invent a new one.
createOP(
    name="spatial",
    namespace=DCTERMS,
    graph=g,
    domain_list=[DWC["Event"]],
    range_list=[DCTERMS["Location"]],
    definition=Literal("An [owl:ObjectProperty] used to relate a [dwc:Event] to the [dcterms:Location] it spatially occurred in."),
    examples=Literal("bb:event123 dcterms:spatial bb:location456 .")
)

#####################################################################################################
# BEGIN DATATYPE PROPERTY DEFINITIONS
#####################################################################################################

createDP(
    name="caption",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Caption"),
    definition=Literal("Free-form text to be displayed together with (rather than instead of) a resource that is suitable for captions (especially images)."),
    comments=Literal("If both [dcterms:description] and [ac:caption] are present in the metadata, a [dcterms:description] is typically displayed instead of the resource, a [ac:caption] together with the resource. Thus, in HTML it would be appropriate to use [ac:caption] values in figcaption elements. Often only one of the [dcterms:description] or [ac:caption] is present; choose the term most appropriate for your metadata."),
    version_of_s="http://rs.tdwg.org/ac/terms/caption",
    references_s="http://rs.tdwg.org/ac/terms/version/caption-2021-10-05",
)

createDP(
    name="freqHigh",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Upper frequency bound"),
    definition=Literal("The highest frequency of the phenomena reflected in the multimedia item or Region of Interest."),
    comments=Literal("Numeric value in hertz (Hz). This term refers to the sound events depicted and not to the constraints of the recording medium, so are in principle independent from sampleRate. If [dwc:scientificName] is specified and if applied to the entire multimedia item, these frequency bounds refer to the sounds of the species given in the [dwc:scientificName] throughout the whole recording. Although many users will specify both [ac:freqLow] and [ac:freqHigh], it is permitted to specify just one or the other, for example if only one of the bounds is discernible."),
    examples=Literal("`60`"),
    version_of_s="http://rs.tdwg.org/ac/terms/freqHigh",
    references_s="http://rs.tdwg.org/ac/terms/version/freqHigh-2021-10-05",
)

createDP(
    name="freqLow",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Lower frequency bound"),
    definition=Literal("The lowest frequency of the phenomena reflected in the multimedia item or Region of Interest."),
    comments=Literal("Numeric value in hertz (Hz). This term refers to the sound events depicted and not to the constraints of the recording medium, so are in principle independent from sampleRate. If [dwc:scientificName] is specified and if applied to the entire multimedia item, these frequency bounds refer to the sounds of the species given in the [dwc:scientificName] throughout the whole recording. Although many users will specify both [ac:freqLow] and [ac:freqHigh], it is permitted to specify just one or the other, for example if only one of the bounds is discernible."),
    examples=Literal("`60`"),
    version_of_s="http://rs.tdwg.org/ac/terms/freqLow",
    references_s="http://rs.tdwg.org/ac/terms/version/freqLow-2021-10-05",
)

createDP(
    name="heightFrac",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Fractional Height"),
    definition=Literal("The height of the bounding rectangle, expressed as a decimal fraction of the height of a [dwc:Media] resource."),
    comments=Literal("The sum of a valid value plus [ac:yFrac] MUST be greater than zero and less than or equal to one. The precision of this value SHOULD be great enough that when [ac:heightFrac] and [ac:yFrac] are used with the [exif:PixelYDimension] of the Best Quality variant of the Service Access point to calculate the lower right corner of the rectangle, rounding to the nearest integer results in the same vertical pixel originally used to define the point. This term MUST NOT be used with [ac:radius] to define a region of interest. Zero-sized bounding rectangles are not allowed. To designate a point, use the radius option with a zero value."),
    examples=Literal("`0.5`; `1`"),
    version_of_s="http://rs.tdwg.org/ac/terms/heightFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/heightFrac-2021-10-05",
)

# NOTE: RECHECK naming
createDP(
    name="isROIOf",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Is Part Of Media ID"),
    definition=Literal("An identifier for an [ac:Media] resource of which this [ac:Media] resource is a part."),
    comments=Literal("This term can be used to define an [ac:RegionOfInterest] within an [ac:Media] resource. Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://rs.tdwg.org/ac/terms/isROIOf",
    references_s="http://rs.tdwg.org/ac/terms/version/isROIOf-2021-10-05",
)

createDP(
    name="radius",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[XSD["integer"]],
    pref_label=Literal("Radius"),
    definition=Literal("The radius of a bounding circle or arc, expressed as a fraction of the width of a [dwc:Media] resource."),
    comments=Literal("A valid value MUST be greater than or equal to zero. A valid value MAY cause the designated circle to extend beyond the bounds of a [dwc:Media] resource. In that case, the arc within a [dwc:Media] resource plus the bounds of a [dwc:Media] resource specify the region of interest. This term MUST NOT be used with [ac:widthFrac] or [ac:heightFrac] to define a region of interest. This term may be used with [ac:xFrac] and [ac:yFrac] to define a point. In that case, the implication is that the point falls on some object of interest within a [dwc:Media] resource, but nothing more can be assumed about the bounds of that object."),
    examples=Literal("`100`"),
    version_of_s="http://rs.tdwg.org/ac/terms/radius",
    references_s="http://rs.tdwg.org/ac/terms/version/radius-2021-10-05",
)

createDP(
    name="widthFrac",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Fractional Width"),
    definition=Literal("The width of the bounding rectangle, expressed as a decimal fraction of the width of a [dwc:Media] resource."),
    comments=Literal("The sum of a valid value plus [ac:xFrac] MUST be greater than zero and less than or equal to one. The precision of this value SHOULD be great enough that when [ac:widthFrac] and [ac:xFrac] are used with the [exif:PixelXDimension] of the Best Quality variant of the Service Access point to calculate the lower right corner of the rectangle, rounding to the nearest integer results in the same horizontal pixel originally used to define the point. This term MUST NOT be used with [ac:radius] to define a region of interest. Zero-sized bounding rectangles are not allowed. To designate a point, use the radius option with a zero value."),
    examples=Literal("`0.5`; `1`"),
    version_of_s="http://rs.tdwg.org/ac/terms/widthFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/widthFrac-2021-10-05",
)

createDP(
    name="xFrac",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Fractional X"),
    definition=Literal("The horizontal position of a reference point, measured from the left side of a [dwc:Media] resource and expressed as a decimal fraction of the width of a [dwc:Media] resource."),
    comments=Literal("A valid value MUST be greater than or equal to zero and less than or equal to one. The precision of this value SHOULD be great enough that when the [ac:xFrac] value is multiplied by the [exif:PixelXDimension] of the Best Quality variant of the Service Access point, rounding to the nearest integer results in the same horizontal pixel location originally used to define the point. This point can serve as the horizontal position of the upper left corner of a bounding rectangle, or as the center of a circle."),
    examples=Literal("`0.5`; `1`"),
    version_of_s="http://rs.tdwg.org/ac/terms/xFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/xFrac-2021-10-05",
)

createDP(
    name="yFrac",
    namespace=AC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Fractional Y"),
    definition=Literal("The vertical position of a reference point, measured from the top of a [dwc:Media] resource and expressed as a decimal fraction of the height of a [dwc:Media] resource."),
    comments=Literal("A valid value MUST be greater than or equal to zero and less than or equal to one. The precision of this value SHOULD be great enough that when the [ac:yFrac] value is multiplied by the [exif:PixelYDimension] of the Best Quality variant of the Service Access point, rounding to the nearest integer results in the same vertical pixel originally used to define the point. This point can serve as the vertical position of the upper left corner of a bounding rectangle, or as the center of a circle."),
    examples=Literal("`0.5`; `1`"),
    version_of_s="http://rs.tdwg.org/ac/terms/yFrac",
    references_s="http://rs.tdwg.org/ac/terms/version/yFrac-2021-10-05",
)

createDP(
    name="description",
    namespace=DCTERMS,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Description"),
    definition=Literal("An account of the resource."),
    comments=Literal("Description of collection or individual resource, containing the Who, What, When, Where and Why as free-form text. This property optionally allows the presentation of detailed information and will in most cases be show together with the resource title. If both a [dcterms:description] and a [ac:caption] are present in the metadata, a [dcterms:description] is typically displayed instead of the resource, whereas a [ac:caption] is displayed together with the resource. The [dcterms:description] should aim to be a good proxy for the underlying media resource in cases where only text can be shown, whereas the [ac:caption] may only make sense when shown together with the media. Thus, in HTML it would e appropriate to use [dcterms:description] values for alt attributes in img elements. Often only one of description or caption is present; choose the term most appropriate for your metadata. It is the role of implementers of an [ac:] concrete representation (e.g. an XML Schema, an RDF representation, etc.) to decide and document how formatting advice will be represented in descriptions serialized according to such representations."),
    version_of_s="http://purl.org/dc/terms/description",
)

# NOTE: REVOIR COMMENTS. THIS DOCUMENT? ALSO, ACCEPT BOTH A STRING OR A URI?
createDP(
    name="rights",
    namespace=DC,
    graph=g,
    domain_list=[DWC["UsagePolicy"]],
    range_list=[XSD["anyURI"], XSD["string"]],
    pref_label=Literal("Rights (DC)"),
    definition=Literal("Information about rights held in and over the resource. A full-text, readable copyright statement, as rquired by the national legislation of the copyright holder. On collections, this applies to all contained objects, unless the object itself has a different statement. Do not place just the name of the copyright holder(s) here! That belongs in a list in the [xmpRights:Owner] field, which should be supplied only if [dc:rights] is not `Public Domain`, which is appropriate only if the resource is known to be not under copyright. See also the entry for [dcterms:rights] in this document and see the DMCI FAQ on [dc:] and [dcterms:] Namespaces for discussion of the rationale for terms in two namespaces. Normal practice is to use the same Label if both are provided. Labels have no effect on information discovery and are only suggestions."),
    examples=Literal("`Copyright 2014 Ron Thomas`; `http://creativecommons.org/licenses/by/3.0/legalcode`"),
    version_of_s="http://purl.org/dc/elements/1.1/rights",
)

# WARN: Verify domain
createDP(
    name="source",
    namespace=DC,
    graph=g,
    domain_list=[DWC["UsagePolicy"]],
    range_list=[XSD["anyURI"], XSD["string"]],
    pref_label=Literal("Source (DC)"),
    definition=Literal("A related resource from which the described resource is derived", lang="en"),
    comments=Literal("The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system.", lang="en"),
    version_of_s="http://purl.org/dc/elements/1.1/source",
)


# NOTE: Felt that the second part was more apt of a comment.
createDP(
    name="rights",
    namespace=DCTERMS,
    graph=g,
    domain_list=[DWC["UsagePolicy"]],
    range_list=[XSD["anyURI"]],
    pref_label=Literal("Rights (DCTERMS)"),
    definition=Literal("A URI pointing to structured information about rights held in and over the resource."),
    comments=Literal("At least one of [dcterms:rights] and [dc:rights] must be supplied but, when feasible, supplying both may make the metadata more widely useful. They must specify the same rights. In case of ambiguity, [dcterms:rights] prevails."),
    examples=Literal("`http://creativecommons.org/licenses/by/3.0/legalcode`; `http://creativecommons.org/publicdomain/zero/1.0`"),
    version_of_s="http://purl.org/dc/terms/rights",
)

# WARN: Verify domain
createDP(
    name="source",
    namespace=DCTERMS,
    graph=g,
    domain_list=[DWC["UsagePolicy"]],
    range_list=[XSD["anyURI"], XSD["string"]],
    pref_label=Literal("Source (DCTERMS)"),
    definition=Literal("A related resource from which the described resource is derived", lang="en"),
    comments=Literal("This property is intended to be used with non-literal values. The described resource may be derived from the related resource in whole or in part. Best practice is to identify the related resource by means of a URI or string conforming to a formal identification system.", lang="en"),
    version_of_s="http://purl.org/dc/terms/source",
)

createDP(
    name="title",
    namespace=DCTERMS,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Title"),
    definition=Literal("A name given to a resource."),
    comments=Literal("Concise title, name, or brief descriptive label of institution, resource collection, or individual resource. This field SHOULD include the complete title with all the subtitles, if any. It is strongly suggested to provide a title. The title facilitates interactions with humans: e.g, it could be used as display text of hyperlinks or to provide a choice of images in a pick list. The title is therefore highly useful and an effort should be made to provide it where it is not already available. When the resource is a collection without an institutional or official name, but with a thematic content, a descriptive title, e.g. \"Urban Ants of New England\", would be suitable. In individual media resources depicting taxa, the scientific name or names of taxa are often a good title. Common names, in addition to or instead of scientific names are also acceptable. Indications of action or roles captured by the media resource, such as predatory acts, are desireable (\"Rattlesnake eating deer mouse\", \"Pollinators of California Native Plants\")."),
    version_of_s="http://purl.org/dc/terms/title",
)

# NOTE: REVOIR COMMENTS. SHOULD READ CONTROLLED VOCABULARY
createDP(
    name="type",
    namespace=DCTERMS,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Media Type"),
    definition=Literal("A category that best matches the nature of an [ac:Media] resource."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    examples=Literal("`Sound`; `StillImage`; `MovingImage`; `InteractiveResource`; `Text`"),
    version_of_s="http://purl.org/dc/terms/type",
)

createDP(
    name="agentID",
    namespace=DWC,
    graph=g,
    domain_list=[DCTERMS["Agent"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Agent ID"),
    definition=Literal("An identifier for a [dcterms:Agent]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/agentID"
)

createDP(
    name="agentRemarks",
    namespace=DWC,
    graph=g,
    domain_list=[DCTERMS["Agent"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Agent Remarks"),
    definition=Literal("Comments or notes about a [dcterms:Agent]."),
    version_of_s="http://example.com/term-pending/dwc/agentRemarks"
)

createDP(
    name="agentType",
    namespace=DWC,
    graph=g,
    domain_list=[DCTERMS["Agent"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Agent Type"),
    definition=Literal("A category that best matches the nature of a [dcterms:Agent]."),
    comments=Literal("Recommended best practice is to use a controlled vocabulary."),
    examples=Literal("`person`; `group`; `organization`; `camera`"),
    version_of_s="http://example.com/term-pending/dwc/agentType",
)

createDP(
    name="assayType",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assay Type"),
    definition=Literal("A method used in the study to detect taxon/taxa of interest in the sample"),
    comments=Literal("Recommended best practice is to use a controlled vocabulary."),
    examples=Literal("`targeted`; `metabarcoding`; `other`"),
    version_of_s="http://example.com/term-pending/dwc/assayType",
)

# NOTE: I would have liked an xsd:date like datatype, but non-ISO 8601 and / make it difficult.
createDP(
    name="assertionEffectiveDate",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assertion Effective Date"),
    definition=Literal("A date on which a state or measurement of a [dwc:Assertion] was deemed to first be in effect."),
    comments=Literal("Recommended best practice is to use a date that conforms to ISO 8601-1:2019."),
    examples=Literal("`1963-04-08T14:07-06:00` (8 Mar 1963 at or after 2:07pm and before 2:08pm in the time zone six hours earlier than UTC); `2009-02-20T08:40Z` (20 February 2009 at or after 8:40am and before 8:41 UTC); `2018-08-29T15:19` (29 August 2018 at or after 3:19pm and before 3:20pm local time); `1809-02-12` (within the day 12 February 1809); `1906-06` (in the month of June 1906); `1971` (in the year 1971); `2007-03-01T13:00:00Z/2008-05-11T15:30:00Z` (some time within the interval beginning 1 March 2007 at 1pm UTC and before 11 May 2008 at 3:30pm UTC); `1900/1909` (some time within the interval between the beginning of the year 1900 and before the year 1909); `2007-11-13/15` (some time in the interval between the beginning of 13 November 2007 and before 15 November 2007)"),
    version_of_s="http://example.com/term-pending/dwc/assertionEffectiveDate",
)

createDP(
    name="assertionID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assertion ID"),
    definition=Literal("An identifier for a [dwc:Assertion]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/assertionID"
)

# NOTE: I would have liked an xsd:date like datatype, but non-ISO 8601 and / make it difficult.
createDP(
    name="assertionMadeDate",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assertion Made Date"),
    definition=Literal("A date on which a [dwc:Assertion] was created."),
    comments=Literal("Recommended best practice is to use a date that conforms to ISO 8601-1:2019."),
    examples=Literal("`1963-04-08T14:07-06:00` (8 Mar 1963 at or after 2:07pm and before 2:08pm in the time zone six hours earlier than UTC); `2009-02-20T08:40Z` (20 February 2009 at or after 8:40am and before 8:41 UTC); `2018-08-29T15:19` (29 August 2018 at or after 3:19pm and before 3:20pm local time); `1809-02-12` (within the day 12 February 1809); `1906-06` (in the month of June 1906); `1971` (in the year 1971); `2007-03-01T13:00:00Z/2008-05-11T15:30:00Z` (some time within the interval beginning 1 March 2007 at 1pm UTC and before 11 May 2008 at 3:30pm UTC); `1900/1909` (some time within the interval between the beginning of the year 1900 and before the year 1909); `2007-11-13/15` (some time in the interval between the beginning of 13 November 2007 and before 15 November 2007)"),
    version_of_s="http://example.com/term-pending/dwc/assertionMadeDate",
)

createDP(
    name="assertionType",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assertion Type"),
    definition=Literal("A category that best matches the nature of a [dwc:Assertion]."),
    comments=Literal("Recommended best practice is to use a controlled vocabulary. This term has an equivalent in the [dwciri:] namespace that allows only an IRI as a value, whereas this term allows for any string literal value."),
    examples=Literal("`tail length`; `temperature`; `trap line length`; `survey area`; `trap type`"),
    version_of_s="http://example.com/term-pending/dwc/assertionType",
)

# NOTE: Personally, I think a dwc:assertionTypeSourceIRI being a subproperty of dcterms:source would be a better fit.
createDP(
    name="assertionTypeSource",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assertion Type Source"),
    definition=Literal("A reference to the controlled vocabulary in which the definition of a value in [dwc:assertionType] is given."),
    version_of_s="http://purl.org/dc/elements/1.1/source",
    subproperty_list=[DC["source"]],
)

createDP(
    name="assertionValue",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assertion Value"),
    definition=Literal("An asserted value, if it is not numeric."),
    version_of_s="http://example.com/term-pending/dwc/assertionValue",
)

# NOTE: xsd:decimal should be able to handle all real numbers (i.e. including integers).
createDP(
    name="assertionValueNumeric",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Assertion Value Numeric"),
    definition=Literal("An asserted value, if it is numeric."),
    version_of_s="http://example.com/term-pending/dwc/assertionValueNumeric",
)

# NOTE: Personally, I think a dwc:assertionValueSourceIRI being a subproperty of dcterms:source would be a better fit.
createDP(
    name="assertionValueSource",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Assertion Value Source"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [dwc:assertionValue] is given."),
    version_of_s="http://purl.org/dc/elements/1.1/source",
    subproperty_list=[DC["source"]],
)

createDP(
    name="derivedFromMediaID",
    namespace=DWC,
    graph=g,
    domain_list=[AC.Media],
    range_list=[RDFS.Literal],
    pref_label=Literal("Derived From Media ID"),
    definition=Literal("An identifier for an [ac:Media] resource of which this [ac:Media] resource is a part."),
    comments=Literal("This term can be used when an [ac:Media] resource has been separated from its source [ac:Media] resource. Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/derivedFromMediaID",
)

createDP(
    name="eventID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Event"], DWC["EventAssertion"], DWC["NucleotideAnalysis"], ECO["Survey"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Event ID"),
    definition=Literal("An identifier for a [dwc:Event]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://rs.tdwg.org/dwc/terms/eventID",
    references_s="http://rs.tdwg.org/dwc/terms/version/eventID-2023-06-28"
)

createDP(
    name="geologicalContextID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["GeologicalContext"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Geological Context ID"),
    definition=Literal("An identifier for a [dwc:GeologicalContext]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://rs.tdwg.org/dwc/terms/geologicalContextID",
    references_s="http://rs.tdwg.org/dwc/terms/version/geologicalContextID-2023-06-28"
)

createDP(
    name="materialEntityID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["MaterialEntity"], DWC["NucleotideAnalysis"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Material Entity ID"),
    definition=Literal("An identifier for a [dwc:MaterialEntity]."),
    comments=Literal("Values of [dwc:materialEntityID] are intended to uniquely and persistently identify a particular [dwc:MaterialEntity] within some context. Examples of context include a particular sample collection, an organization, or the worldwide scale. Recommended best practice is to use a persistent, globally unique identifier. The identifier is bound to a physical object (a [dwc:MaterialEntity]) as opposed to a particular digital record (representation) of that physical object."),
    version_of_s="http://rs.tdwg.org/dwc/terms/materialEntityID",
    references_s="http://rs.tdwg.org/dwc/terms/version/materialEntityID-2023-09-13"
)

# NOTE: Confirm namespace dwc: or ac:
createDP(
    name="mediaID",
    namespace=DWC,
    graph=g,
    domain_list=[AC["Media"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Media ID"),
    definition=Literal("An identifier for an [ac:Media] resource."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/mediaID",
)

createDP(
    name="molecularProtocolID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["MolecularProtocol"], DWC["NucleotideAnalysis"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Molecular Protocol ID"),
    definition=Literal("An identifier for a [dwc:MolecularProtocol]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/molecularProtocolID",
)

createDP(
    name="nucleotideAnalysisID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["NucleotideAnalysis"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Nucleotide Analysis ID"),
    definition=Literal("An identifier for a [dwc:NucleotideAnalysis]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/nucleotideAnalysisID",
)

createDP(
    name="nucleotideSequenceID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["NucleotideAnalysis"], DWC["NucleotideSequence"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Nucleotide Sequence ID"),
    definition=Literal("An identifier for a [dwc:NucleotideSequence]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/molecularProtocolID",
)

createDP(
    name="nucleotideSequenceRemarks",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["NucleotideSequence"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Nucleotide Sequence Remarks"),
    definition=Literal("Comments or notes about a [dwc:NucleotideSequence]."),
    version_of_s="http://example.com/term-pending/dwc/nucleotideSequenceRemarks",
)

createDP(
    name="organismID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Organism"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Organism ID"),
    definition=Literal("An identifier for a [dwc:Organism]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://rs.tdwg.org/dwc/terms/organismID",
    references_s="http://rs.tdwg.org/dwc/terms/version/organismID-2023-06-28"
)

createDP(
    name="organismInteractionID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Organism"], DWC["OrganismInteraction"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Organism Interaction ID"),
    definition=Literal("An identifier for a [dwc:OrganismInteraction]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://rs.tdwg.org/dwc/terms/organismID",
)

createDP(
    name="preferredAgentName",
    namespace=DWC,
    graph=g,
    domain_list=[DCTERMS["Agent"]],
    range_list=[RDFS["Literal"]],
    subproperty_list=[DCTERMS["title"]],
    pref_label=Literal("Preferred Agent Name"),
    definition=Literal("A name of a [dcterms:Agent] preferred in searches and results."),
    version_of_s="http://purl.org/dc/terms/title",
)

createDP(
    name="preferredEventName",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Event"]],
    range_list=[RDFS["Literal"]],
    subproperty_list=[DCTERMS["title"]],
    pref_label=Literal("Preferred Event Name"),
    definition=Literal("The name of a [dwc:Event] preferred in searches and results."),
    version_of_s="http://purl.org/dc/terms/title",
)

createDP(
    name="readCount",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["NucleotideAnalysis"]],
    range_list=[XSD["integer"]],
    pref_label=Literal("Read Count"),
    definition=Literal("A number of reads for a [dwc:NucleotideSequence] in a [dwc:NucleotideAnalysis]."),
    version_of_s="http://example.com/term-pending/dwc/readCount",
)

# NOTE: Chose xsd:string because I cannot see any use for rdfs:Literal in this case.
createDP(
    name="sequence",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["NucleotideSequence"]],
    range_list=[XSD["string"]],
    pref_label=Literal("Sequence"),
    definition=Literal("A string representing nucleotide base pairs."),
    version_of_s="http://example.com/term-pending/dwc/sequence",
)

# NOTE: Comment in JSON file says dwc:Survey?
createDP(
    name="surveyID",
    namespace=DWC,
    graph=g,
    domain_list=[ECO["Survey"], ECO["SurveyTarget"]],
    range_list=[XSD["string"]],
    pref_label=Literal("Survey ID"),
    definition=Literal("An identifier for a [eco:Survey]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/surveyID",
)

# NOTE: Comment in JSON file says dwc:SurveyTarget?
createDP(
    name="surveyTargetID",
    namespace=DWC,
    graph=g,
    domain_list=[ECO["SurveyTarget"]],
    range_list=[XSD["string"]],
    pref_label=Literal("Survey Target ID"),
    definition=Literal("An identifier for a [eco:SurveyTarget]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/surveyTargetID",
)

createDP(
    name="surveyTargetType",
    namespace=DWC,
    graph=g,
    domain_list=[ECO["SurveyTarget"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Survey Target Type"),
    definition=Literal("A scope a [eco:SurveyTarget] describes."),
    comments=Literal("Recommended best practice is to use a controlled vocabulary."),
    examples=Literal("`taxon`; `habitat`; `establishmentMeans`; `growthForm`; `sex`; `lifeStage`; `minimum length`"),
    version_of_s="http://example.com/term-pending/dwc/surveyTargetType",
)

createDP(
    name="surveyTargetTypeSource",
    namespace=DWC,
    graph=g,
    domain_list=[ECO["SurveyTarget"]],
    range_list=[XSD["string"]],
    pref_label=Literal("Survey Target Type Source"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [eco:surveyTargetValue] is given."),
    subproperty_list=[DC["source"]],
    version_of_s="http://purl.org/dc/elements/1.1/source",
)

createDP(
    name="totalReadCount",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["NucleotideAnalysis"]],
    range_list=[XSD["integer"]],
    pref_label=Literal("Total Read Count"),
    definition=Literal("A total number of reads in a [dwc:NucleotideAnalysis]."),
    version_of_s="http://example.com/term-pending/dwc/totalReadCount",
)

createDP(
    name="usagePolicyID",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["UsagePolicy"]],
    range_list=[XSD["string"]],
    pref_label=Literal("Usage Policy ID"),
    definition=Literal("An identifier for a [dwc:UsagePolicy]."),
    comments=Literal("Recommended best practice is to use a globally unique identifier."),
    version_of_s="http://example.com/term-pending/dwc/usagePolicyID",
)

createDP(
    name="verbatimAssertionType",
    namespace=DWC,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Verbatim Assertion Type"),
    definition=Literal("A string representing the type of [dwc:Assertion] as it appeared in the original record.", lang="en"),
    comments=Literal("This term is meant to allow the capture of an unaltered original name for a [dwc:assertionType]. This term is meant to be used in addition to [dwc:assertionType], not instead of it.", lang="en"),
    examples=Literal("`water_temp`; `Fish biomass`; `sampling net mesh size`"),
    version_of_s="http://example.com/term-pending/dwc/verbatimAssertionType",
)

createDP(
    name="assertionTypeIRI",
    namespace=DWCIRI,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[XSD["anyURI"]],
    pref_label=Literal("Assertion Type (IRI)"),
    definition=Literal("An IRI of a controlled vocabulary value for a type of [dwc:Assertion].", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for a term in a controlled vocabulary.", lang="en"),
    version_of_s="http://example.com/term-pending/dwciri/assertionTypeIRI",
)

# NOTE: I added the example IRI
createDP(
    name="assertionValueIRI",
    namespace=DWCIRI,
    graph=g,
    domain_list=[DWC["Assertion"]],
    range_list=[XSD["anyURI"]],
    pref_label=Literal("Assertion Value (IRI)"),
    definition=Literal("An IRI of the controlled vocabulary value for a value of a [dwc:Assertion].", lang="en"),
    examples=Literal("`http://purl.obolibrary/obo/UBERON_0014860`"),
    version_of_s="http://example.com/term-pending/dwciri/assertionValueIRI",
)

# NOTE: Comment in JSON file says dwc:SurveyTargetType?
createDP(
    name="surveyTargetTypeIRI",
    namespace=DWCIRI,
    graph=g,
    domain_list=[ECO["SurveyTarget"]],
    range_list=[XSD["anyURI"]],
    pref_label=Literal("Survey Target Type IRI"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [eco:SurveyTargetType] is given.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for a term in a controlled vocabulary.", lang="en"),
    subproperty_list=[DCTERMS["type"]],
    version_of_s="http://purl.org/dc/terms/type",
)

# NOTE: Property I created. I do not see why there is not a DWCIRI analogue of dwc:surveyTargetTypeSource. I would like to be able to give the URI of something like the NERC vocabulary from which my term was taken (e.g. `http://vocab/nerc.ac.uk/collection/S11/current/`).
createDP(
    name="surveyTargetTypeSourceIRI",
    namespace=DWCIRI,
    graph=g,
    domain_list=[ECO["SurveyTarget"]],
    range_list=[XSD["anyURI"]],
    pref_label=Literal("Survey Target Type Source IRI"),
    definition=Literal("A reference to a controlled vocabulary in which the definition of a value in [eco:surveyTargetValue] is given.", lang="en"),
    comments=Literal("Recommended best practice is to use an IRI for a controlled vocabulary.", lang="en"),
    subproperty_list=[DCTERMS["source"]],
    version_of_s="http://purl.org/dc/elements/terms/source",
)

# NOTE: Definition uses term dwc:Event, but we want to consider dwc:Survey. Should clarify difference or allow cases where an entity can be both a dwc:Event and a eco:Survey.
createDP(
    name="siteCount",
    namespace=ECO,
    graph=g,
    domain_list=[ECO["Survey"]],
    range_list=[XSD["integer"]],
    pref_label=Literal("Site Count"),
    definition=Literal("Total number of sites surveyed during a [dwc:Event].", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy.", lang="en"),
    examples=Literal("`1`; `15`"),
    version_of_s="http://rs.tdwg.org/eco/terms/siteCount",
    references_s="http://rs.tdwg.org/eco/terms/version/siteCount-2024-02-28",
)

createDP(
    name="siteNestingDescription",
    namespace=ECO,
    graph=g,
    domain_list=[ECO["Survey"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Site Nesting Description"),
    definition=Literal("Textual description of a hierarchical sampling design.", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy.", lang="en"),
    examples=Literal("`5 sampling sites of 3-5 plots each`"),
    version_of_s="http://rs.tdwg.org/eco/terms/siteNestingDescription",
    references_s="http://rs.tdwg.org/eco/terms/version/siteNestingDescription-2024-02-28",
)

createDP(
    name="verbatimSiteDescriptions",
    namespace=ECO,
    graph=g,
    domain_list=[ECO["Survey"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Verbatim Site Description"),
    definition=Literal("Original textual description of site(s).", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy. Recommended best practice is to separate multiple values in a list with space vertical bar space (` | `).", lang="en"),
    examples=Literal("`Wet flatwoods | Wet depression surrounded by mesic longleaf pine flatwoods | Ground cover of thick *Andropogon* spp., *Sporobolus floridanus*, *Vaccinium* spp., *Rhynchospora* spp., *Centella erecta*, *Panicum rigidulum*`"),
    version_of_s="http://rs.tdwg.org/eco/terms/verbatimSiteDescriptions",
    references_s="http://rs.tdwg.org/eco/terms/version/verbatimSiteDescriptions-2024-02-28",
)

createDP(
    name="verbatimSiteNames",
    namespace=ECO,
    graph=g,
    domain_list=[ECO["Survey"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Verbatim Site Names"),
    definition=Literal("A list (concatenated and separated) of original site names.", lang="en"),
    comments=Literal("Site refers to the location at which observations are made or samples/measurements are taken. The site can be at any level of hierarchy. Recommended best practice is to separate multiple values in a list with space vertical bar space (` | `).", lang="en"),
    examples=Literal("`East Coastal Fringe | St. Marks Wildlife Management Area`; `S1 | S2 | C1 | C2 | R14 | R22 | W1`"),
    version_of_s="http://rs.tdwg.org/eco/terms/verbatimSiteNames",
    references_s="http://rs.tdwg.org/eco/terms/version/verbatimSiteNames-2024-02-28",
)

# NOTE: I do not quite see why this property is here. If we are modeling the sequence as a separate entity dwc:NucleotideSequence, shouldn't this be a property for dwc:NucleotideSequence? Also, the newly proposed term dwc:sequence does that, making this term somewhat useless unless for backwards compatibility with datasets that had the DNA extension.
createDP(
    name="dna_sequence",
    namespace=GBIF,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["string"]],
    pref_label=Literal("DNA Sequence"),
    definition=Literal("The DNA sequence.", lang="en"),
    version_of_s="https://rs.gbif/org/terms/dna_sequence",
)


# NOTE: Used xsd:string because I couldn't see a use for rdfs:Literal in this case.
createDP(
    name="pcr_primer_forward",
    namespace=GBIF,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["string"]],
    pref_label=Literal("Forward PCR Primer"),
    definition=Literal("Forward PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence]. The primer sequence should be reported in uppercase letters.", lang="en"),
    examples=Literal("`GGACTACHVGGGTWTCTAAT`"),
    version_of_s="https://rs.gbif/org/terms/pcr_primer_forward",
)

createDP(
    name="pcr_primer_name_forward",
    namespace=GBIF,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Forward PCR Primer Name"),
    definition=Literal("Name of the forward PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence].", lang="en"),
    examples=Literal("`jgLCO1490`"),
    version_of_s="https://rs.gbif/org/terms/pcr_primer_name_forward",
)

createDP(
    name="pcr_primer_name_reverse",
    namespace=GBIF,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Reverse PCR Primer Name"),
    definition=Literal("Name of the reverse PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence].", lang="en"),
    examples=Literal("`jgHCO2198`"),
    version_of_s="https://rs.gbif/org/terms/pcr_primer_name_reverse",
)

createDP(
    name="pcr_primer_reference",
    namespace=GBIF,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"], XSD["anyURI"]],
    pref_label=Literal("Reverse PCR Primer Name"),
    definition=Literal("Reference for the PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment.", lang="en"),
    examples=Literal("`https:doi.org/10.11861742-9994-10-31`"),
    version_of_s="https://rs.gbif/org/terms/pcr_primer_reference",
)

# NOTE: Used xsd:string because I couldn't see a use for rdfs:Literal in this case.
createDP(
    name="pcr_primer_reverse",
    namespace=GBIF,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["string"]],
    pref_label=Literal("Reverse PCR Primer"),
    definition=Literal("Reverse PCR primer that were used to amplify the sequence of the targeted gene, locus or subfragment. If multiple forward or reverse primers are present in a single PCR reaction, there should be a full row for each of these linked to the same [dwc:Occurrence]. The primer sequence should be reported in uppercase letters.", lang="en"),
    examples=Literal("`GGACTACHVGGGTWTCTAAT`"),
    version_of_s="https://rs.gbif/org/terms/pcr_primer_reverse",
)

createDP(
    name="concentration",
    namespace=GGBN,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("DNA Concentration"),
    definition=Literal("Concentration of DNA (weight ng/volume µL).", lang="en"),
    examples=Literal("`67.5`"),
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/concentration",
)

createDP(
    name="concentrationUnit",
    namespace=GGBN,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("DNA Concentration Unit"),
    definition=Literal("Unit used for [ggbn:concentration] measurement.", lang="en"),
    examples=Literal("`ng/µL`"),
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/concentrationUnit",
)

createDP(
    name="methodDeterminationConcentrationAndRatios",
    namespace=GGBN,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Method For Concentration Measurement"),
    definition=Literal("Description of method used for [ggbn:concentration] measurement.", lang="en"),
    examples=Literal("`Nanodrop`; `Qubit`"),
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/methodDeterminationConcentrationAndRatios",
)

createDP(
    name="ratioOfAbsorbance260_230",
    namespace=GGBN,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Ratio Of Absorbance At 260 nm and 230 nm"),
    definition=Literal("Ratio of absorbance at 260 nm and 230 nm assessing DNA purity (mostly secondary measure, indicates mainly EDTA, carbohydrates, phenol), (DNA samples only).", lang="en"),
    examples=Literal("`1.89`"),
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/ratioOfAbsorbance260_230",
)

createDP(
    name="ratioOfAbsorbance260_280",
    namespace=GGBN,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Ratio Of Absorbance At 260 nm and 280 nm"),
    definition=Literal("Ratio of absorbance at 260 nm and 280 nm assessing DNA purity (mostly secondary measure, indicates mainly EDTA, carbohydrates, phenol), (DNA samples only).", lang="en"),
    examples=Literal("`1.91`"),
    version_of_s="http://data.ggbn.org/schemas/ggbn/terms/ratioOfAbsorbance260_280",
)

createDP(
    name="ampliconSize",
    namespace=MIQE,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["integer"]],
    pref_label=Literal("Amplicon Size"),
    definition=Literal("The length of the amplicon in basepairs.", lang="en"),
    examples=Literal("`83`"),
    version_of_s="http://rs.gbif.org/terms/miqe/ampliconSize",
)

createDP(
    name="annealingTemp",
    namespace=MIQE,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Annealing Phase Temperature"),
    definition=Literal("The reaction temperature during the annealing phase of PCR.", lang="en"),
    examples=Literal("`60`"),
    version_of_s="http://rs.gbif.org/terms/miqe/annealingTemp",
)

createDP(
    name="annealingTempUnit",
    namespace=MIQE,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Annealing Phase Temperature Unit"),
    definition=Literal("Measurement Unit of the reaction temperature during the annealing phase of PCR.", lang="en"),
    examples=Literal("`60`"),
    version_of_s="http://rs.gbif.org/terms/miqe/annealingTempUnit",
)

createDP(
    name="probeReporter",
    namespace=MIQE,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Probe Reporter"),
    definition=Literal("Type of fluorophore (reporter) used. Probe anneals within amplified target DNA. Polymerase activity degrades the probe that has annealed to the template, and the probe releases the fluorophore from it and breaks the proximity to the quencher, thus allowing fluorescence in the fluorophore.", lang="en"),
    examples=Literal("`FAM`"),
    version_of_s="http://rs.gbif.org/terms/miqe/probeReporter",
)

# NOTE: Think a period was missing in the description.
createDP(
    name="probeQuencher",
    namespace=MIQE,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Probe Quencher"),
    definition=Literal("Type of quencher used. The quencher molecule quenches the fluorescence emitted by the fluorophore when excited by the cycler's light source. As long as fluorophore and the quencher are in proximity, quenching inhibits any fluorescence signals.", lang="en"),
    examples=Literal("`NFQ-MGB`"),
    version_of_s="http://rs.gbif.org/terms/miqe/probeQuencher",
)

createDP(
    name="thresholdQuantificationCycle",
    namespace=MIQE,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["decimal"]],
    pref_label=Literal("Fluorescence Cycle Threshold"),
    definition=Literal("Threshold for change in fluorescence signal between cycles.", lang="en"),
    examples=Literal("`0.3`"),
    version_of_s="http://rs.gbif.org/terms/miqe/thresholdQuantificationCycle",
)

createDP(
    name="baselineValue",
    namespace=MIQE,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[XSD["integer"]],
    pref_label=Literal("Fluorescence Background Value"),
    definition=Literal("The number of cycles when fluorescence signal from the target amplification is below background fluorescence not originated from the real target amplification.", lang="en"),
    examples=Literal("`15`"),
    version_of_s="http://rs.gbif.org/terms/miqe/baselineValue",
)

# NOTE: Double check if accepts Literal or not.
# NOTE: I felt that the browser comment is better suited for a comment.
createDP(
    name="0000008",
    namespace=MIXS,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Experimental Factor"),
    definition=Literal("Experimental factors are essentially the the variable aspects of an experiment design which can be used to describe an experiment, or set of experiments, in an increasingly detailed manner. This field accepts ontology terms from Experimental Factor Ontology ([efo:]) and/or Ontology for Biomedical Investigations ([obi:]).", lang="en"),
    comments=Literal("For a browser of [efo:] (v 2.95) terms, please see [http://purl.bioontology.org/ontology/EFO]; for a browser of [obi:] (v 2018-02-12) terms please see [http://purl.bioontology/ontology/OBI].", lang="en"),
    version_of_s="https://w3id.org/mixs/00000008",
)

createDP(
    name="0000092",
    namespace=MIXS,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Project Name"),
    definition=Literal("Name of the project within which the sequencing was organized.", lang="en"),
    version_of_s="https://w3id.org/mixs/0000092",
)

createDP(
    name="0001107",
    namespace=MIXS,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Sample Name"),
    definition=Literal("Sample Name is a name that you choose for the sample. It can have any format, but we suggest that you make it concise, unique and consistent within your lab, and as informative as possible. Every Sample Name from a single Submitter must be unique.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001107",
)

createDP(
    name="0001320",
    namespace=MIXS,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Sample Taxon ID"),
    definition=Literal("NCBI taxon ID of the sample. May be a single taxon or mixed taxa sample. Use \"synthetic metagenome\" for mock community positive controls, or \"blank sample\" for negative controls.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001320",
)

createDP(
    name="0001321",
    namespace=MIXS,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Negative Control Type"),
    definition=Literal("The substance or equipment used as a negative control in an investigation.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001321",
)

createDP(
    name="0001322",
    namespace=MIXS,
    graph=g,
    domain_list=[DWC["MolecularProtocol"]],
    range_list=[RDFS["Literal"]],
    pref_label=Literal("Positive Control Type"),
    definition=Literal("The substance, mixture, product, or apparatus used to verify that a process which is part of an investigation delivers a true positive.", lang="en"),
    version_of_s="https://w3id.org/mixs/0001322",
)


#####################################################################################################
# BEGIN INDIVIDUALS DEFINITIONS FOR REASONER TEST CASES
#####################################################################################################

# TEST: The reasoner will correctly infer that bb:Agnes is a dwcdp:AuthorAgent
g.add((BB["Bibi"], RDF["type"], DCTERMS["BibliographicResource"]))
g.add((BB["Bibi"], DWCDP["authoredBy"], BB["Agnes"]))
# g.add((DWCDP["Agnes"], RDF["type"], DCTERMS["Agent"]))


# TEST: The reasoner will not be able to state anything regarding bb:Bobo, as we declared it a blank node.
# However, it will flag any illogical statement as an inconsistency.
g.add((BB["Idi"], RDF["type"], DWC["Identification"]))
g.add((BB["Idi"], DWCDP["basedOn"], BB["Bobo"]))
# g.add((BB["Bobo"], RDF["type"], DWC["NucleotideSequence"]))
# g.add((BB["Bobo"], RDF["type"], DWC["GeologicalContext"]))

# TEST: bb:Sourco is correctly inferred to be a dwc:MaterialEntity
g.add((BB["Mato"], RDF["type"], DWC["MaterialEntity"]))
g.add((BB["Mato"], DWCDP["isDerivedFrom"], BB["Sourco"]))
# g.add((BB["Mato"], RDF["type"], DWC["MaterialEntity"]))

# TEST: The chain of derivations will be inferred by the reasoner.
g.add((BB["Mato1"], RDF["type"], DWC["MaterialEntity"]))
g.add((BB["Mato1"], DWCDP["isDerivedFrom"], BB["Mato2"]))
g.add((BB["Mato2"], DWCDP["isDerivedFrom"], BB["Mato3"]))
g.add((BB["Mato3"], DWCDP["isDerivedFrom"], BB["Mato4"]))


# TEST: bb:Midio is inferred to be an instance of ac:Media.
# Also, the inverse triple statement is inferred:
# bb:Occurro dwcdp:hasMedia bb:Midio
# g.add((BB["Midio"], RDF["type"], DWC["EventMedia"]))
g.add((BB["Midio"], DWCDP["isMediaOf"], BB["Occurro"]))

# TEST: Test case where the object property dwcdp:happenedDuring is used twice.
# The first time to link bb:BeeVisitingFlower to bb:Site123, and the second
# time to link bb:Site123 to its parent event bb:ParentSite456.
# Note that only bb:BeeVisitingFlowerBeeVisitingFlower is declared as an
# instance of dwc:OrganismInteraction.
# The reasoner correctly infers that both bb:Site123 and bb:ParentSite456
# are instances of dwc:Event.
#g.add((BB["BeeVisitingFlower"], RDF["type"], DWC["OrganismInteraction"]))
g.add((BB["BeeVisitingFlower"], DWCDP["happenedDuring"], BB["Site123"]))
g.add((BB["Site123"], DWCDP["happenedDuring"], BB["ParentSite456"]))
# NOTE: Note declaring bb:BeeVisitingFlower as a dwc:OrganismInteraction
# still gives an inference that both infers that both bb:Site123 and
# bb:ParentSite456 are instances of dwc:Event, but nothing can be inferred
# for bb:BeeVisitingFlower, due to the wide domain that dwcdp:happenedDuring
# has (i.e. the union of dwc:Event, dwc:Occurrence, dwc:OrganismInteraction and
# eco:Survey).

# g.add((BB["Sometho"], RDF["type"], DWC["Assertion"]))
# g.add((BB["Sometho"], DWCDP["hasMedia"], BB["MidioNo"]))

# g.add((BB["MidioNo"], DWCDP["isMediaOf"], BB["Sometho"]))
# g.add((BB["Sometho"], RDF["type"], DWC["Assertion"]))

#####################################################################################################
# BEGIN OWL API USAGE
#####################################################################################################

# NOTE: Use ROBOT to use the OWL API directly, better than having to go into Protege everytime.
# Obtained with curl -L -o robot.jar https://github.com/ontodev/robot/releases/download/v1.9.8/robot.jar
# Put in .gitgnore since it is borderline LFS.
subprocess.run(["java", "-jar", "robot.jar", "convert", "--input", "dwcdp_owl.owl", "--output", "ontology.ttl"])
