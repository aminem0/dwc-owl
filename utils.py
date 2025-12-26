from rdflib import BNode, Graph, Literal, Namespace, Node, URIRef
from rdflib.collection import Collection
from rdflib.namespace import DC, DCTERMS, OWL, RDF, RDFS, SKOS, XSD


# WARN:
# Technically examples should be list[URIRef] but left list[Literal]
# to accomodate textual definitons of examples
#
# WARN: Rewriting this function.
# Included universal restrictions into the function definition.
def createOC(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        version_of_s: str,
        subclass_list: list[Node] | None = None,
        equivalent_class: Node | None = None,
        exist_rest_filler: list[tuple[Node, Node]] | None = None,
        univ_rest_filler: list[tuple[Node, Node]] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        examples: Literal | list[URIRef] | list[Literal] | None = None,
        card1_restrictions: list[Node] | None = None,
        maxcard1_restrictions: list[Node] | None = None,
        references_s: str | None = None,
) -> None:
    """
    Define an OWL class
    """

    # Define class uri
    class_uri = namespace[name]

    # Add DEFINEDBY
    graph.add((class_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))
    graph.add((class_uri, SKOS["prefLabel"], pref_label))

    if definition:
        graph.add((class_uri, SKOS["definition"], definition))
    if comments:
        graph.add((class_uri, RDFS["comment"], comments))

    # Add examples if provided
    if examples:
        if isinstance(examples, URIRef):
            graph.add((class_uri, SKOS["example"], examples))
        elif isinstance(examples, list):
            for example in examples:
                graph.add((class_uri, SKOS["example"], example))

    # Add version info.
    graph.add((class_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((class_uri, DCTERMS["references"], URIRef(references_s)))

    # Declare the owl:Class explicitly.
    graph.add((class_uri, RDF["type"], OWL["Class"]))

    if subclass_list:
        # Technically not a unified list, so can add them all with a for loop
        for ro_class in subclass_list:
            graph.add((class_uri, RDFS["subClassOf"], ro_class))

    # Declare any equivalent classes.
    if equivalent_class:
        graph.add((class_uri, OWL["equivalentClass"], equivalent_class))

    # OWL Restrictions
    entity_pylist = []

    if exist_rest_filler:
        for pair in exist_rest_filler:
            ER_class = BNode()
            graph.add((ER_class, RDF["type"], OWL["Restriction"]))
            graph.add((ER_class, OWL["onProperty"], pair[0]))
            graph.add((ER_class, OWL["someValuesFrom"], pair[1]))
            entity_pylist.append(ER_class)

    if univ_rest_filler:
        for pair in univ_rest_filler:
            UR_class = BNode()
            graph.add((UR_class, RDF["type"], OWL["Restriction"]))
            graph.add((UR_class, OWL["onProperty"], pair[0]))
            graph.add((UR_class, OWL["allValuesFrom"], pair[1]))
            entity_pylist.append(UR_class)

    if card1_restrictions:
        for property in card1_restrictions:
            R1_BNode = BNode()
            graph.add((R1_BNode, RDF["type"], OWL["Restriction"]))
            graph.add((R1_BNode, OWL["onProperty"], property))
            graph.add((R1_BNode, OWL["cardinality"], Literal(1, datatype=XSD["nonNegativeInteger"])))
            entity_pylist.append(R1_BNode)

    if maxcard1_restrictions:
        for property in maxcard1_restrictions:
            RM1_BNode = BNode()
            graph.add((RM1_BNode, RDF["type"], OWL["Restriction"]))
            graph.add((RM1_BNode, OWL["onProperty"], property))
            graph.add((RM1_BNode, OWL["maxCardinality"], Literal(1, datatype=XSD["nonNegativeInteger"])))
            entity_pylist.append(RM1_BNode)


    for entity in entity_pylist:
        graph.add((class_uri, RDFS["subClassOf"], entity))

        # Entity_intersection = BNode()
        # Entity_list = BNode()
        # Collection(graph, Entity_list, entity_pylist)
        # graph.add((Entity_intersection, RDF["type"], OWL["Class"]))
        # graph.add((Entity_intersection, OWL["intersectionOf"], Entity_list))
        # graph.add((class_uri, RDFS["subClassOf"], Entity_intersection))

def createDP(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        domains: Node | list[Node] | None = None,
        ranges: Node | list[Node] | None = None,
        version_of_s: str | None = None,
        subproperty_list: list[Node] | None = None,
        additional_list: list[Node] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        examples: Literal | list[Literal] | None = None,
        references_s: str | None = None,
        ) -> None:

    # Create the owl:DatatypeProperty URI
    dp_uri = namespace[name]

    # Add DEFINEDBY
    graph.add((dp_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((dp_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((dp_uri, SKOS["definition"], definition))

    # Optionally add comments.
    if comments:
        graph.add((dp_uri, RDFS["comment"], comments))

    # Add examples if provided
    if examples:
        if isinstance(examples, URIRef):
            graph.add((dp_uri, SKOS["example"], examples))
        elif isinstance(examples, list):
            for example in examples:
                graph.add((dp_uri, SKOS["example"], example))

    # Add version info.
    graph.add((dp_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((dp_uri, DCTERMS["references"], URIRef(references_s)))

    # Declare it in the graph
    graph.add((dp_uri, RDF["type"], OWL["DatatypeProperty"]))

    # NOTE: New version using domain
    if domains:
        if isinstance(domains, URIRef):
            graph.add((dp_uri, RDFS["domain"], domains))
        elif isinstance(domains, list):
            domain_bnode = BNode()
            Collection(graph, domain_bnode, domains)
            domain_union_class = BNode()
            graph.add((domain_union_class, RDF["type"], OWL["Class"]))
            graph.add((domain_union_class, OWL["unionOf"], domain_bnode))
            graph.add((dp_uri, RDFS["domain"], domain_union_class))

    # NOTE: New version using range
    if ranges:
        if isinstance(ranges, URIRef):
            graph.add((dp_uri, RDFS["range"], ranges))
        elif isinstance(ranges, list):
            range_bnode = BNode()
            Collection(graph, range_bnode, ranges)
            range_union_class = BNode()
            graph.add((range_union_class, RDF["type"], RDFS["Datatype"]))
            graph.add((range_union_class, OWL["unionOf"], range_bnode))
            graph.add((dp_uri, RDFS["range"], range_union_class))

    if subproperty_list:
        # Technically not a unified list, so can add them all with a for loop
        for property in subproperty_list:
            graph.add((dp_uri, RDFS["subPropertyOf"], property))

    # Optionally add other types of properties??
    if additional_list:
        for prop_type in additional_list:
            graph.add((dp_uri, RDF["type"], prop_type))


# TEST: Function that creates an owl:DatatypeProperty but allows only a finite set of possibilities
def createEDP(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        one_of: list[Node],
        domains: Node | list[Node] | None = None,        
        version_of_s: str | None = None,
        subproperty_list: list[Node] | None = None,
        additional_list: list[Node] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        examples: Literal | list[Literal] | None = None,
        references_s: str | None = None,
        ) -> None:
    # Create the owl:DatatypeProperty URI
    dp_uri = namespace[name]

    # Add DEFINEDBY
    graph.add((dp_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((dp_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((dp_uri, SKOS["definition"], definition))

    # Optionally add comments.
    if comments:
        graph.add((dp_uri, RDFS["comment"], comments))

    # Add examples if provided
    if examples:
        if isinstance(examples, URIRef):
            graph.add((dp_uri, SKOS["example"], examples))
        elif isinstance(examples, list):
            for example in examples:
                graph.add((dp_uri, SKOS["example"], example))

    # Add version info.
    graph.add((dp_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((dp_uri, DCTERMS["references"], URIRef(references_s)))

    # Declare it in the graph
    graph.add((dp_uri, RDF["type"], OWL["DatatypeProperty"]))

    # NOTE: New version using domain
    if domains:
        if isinstance(domains, URIRef):
            graph.add((dp_uri, RDFS["domain"], domains))
        elif isinstance(domains, list):
            domain_bnode = BNode()
            Collection(graph, domain_bnode, domains)
            domain_union_class = BNode()
            graph.add((domain_union_class, RDF["type"], OWL["Class"]))
            graph.add((domain_union_class, OWL["unionOf"], domain_bnode))
            graph.add((dp_uri, RDFS["domain"], domain_union_class))
    
    # WARN: Here goes a rewrite to consider an enumeration of all allowed datatypes
    # If enumerated literals are provided, build an OWL datatype with owl:oneOf and
    # a Collection of allowable litterals
    if one_of:
        # Create a blank node for the enumerated datatype
        enum_datatype = BNode()
        graph.add((enum_datatype, RDF["type"], RDFS["Datatype"]))

        # Create RDF list of the enumeration values
        enum_list_bnode = BNode()
        Collection(graph, enum_list_bnode, one_of)

        # Attach owl:oneOf list to the datatype node
        graph.add((enum_datatype, OWL["oneOf"], enum_list_bnode))

        # Set this enumerated datatype as the rdfs:range
        graph.add((dp_uri, RDFS["range"], enum_datatype))
        
    if subproperty_list:
        # Technically not a unified list, so can add them all with a for loop
        for property in subproperty_list:
            graph.add((dp_uri, RDFS["subPropertyOf"], property))

    # Optionally add other types of properties??
    if additional_list:
        for prop_type in additional_list:
            graph.add((dp_uri, RDF["type"], prop_type))

# TEST: Function that creates an owl:DatatypeProperty but with a numeric range restriction
# NOTE: Maybe later consider tuples, but for now, lists do the job
def createRDP(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        range_n: Node,
        restrictions: list[list[Node, float, str]],
        domains: Node | list[Node] | None = None,        
        version_of_s: str | None = None,
        subproperty_list: list[Node] | None = None,
        additional_list: list[Node] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        examples: Literal | list[Literal] | None = None,
        references_s: str | None = None,
        ) -> None:
    # Create the owl:DatatypeProperty URI
    dp_uri = namespace[name]

    # Add DEFINEDBY
    graph.add((dp_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((dp_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((dp_uri, SKOS["definition"], definition))

    # Optionally add comments.
    if comments:
        graph.add((dp_uri, RDFS["comment"], comments))

    # Add examples if provided
    if examples:
        if isinstance(examples, URIRef):
            graph.add((dp_uri, SKOS["example"], examples))
        elif isinstance(examples, list):
            for example in examples:
                graph.add((dp_uri, SKOS["example"], example))

    # Add version info.
    graph.add((dp_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((dp_uri, DCTERMS["references"], URIRef(references_s)))

    # Declare it in the graph
    graph.add((dp_uri, RDF["type"], OWL["DatatypeProperty"]))

    # NOTE: New version using domain
    if domains:
        if isinstance(domains, URIRef):
            graph.add((dp_uri, RDFS["domain"], domains))
        elif isinstance(domains, list):
            domain_bnode = BNode()
            Collection(graph, domain_bnode, domains)
            domain_union_class = BNode()
            graph.add((domain_union_class, RDF["type"], OWL["Class"]))
            graph.add((domain_union_class, OWL["unionOf"], domain_bnode))
            graph.add((dp_uri, RDFS["domain"], domain_union_class))
    
    # WARN: Here goes a rewrite to consider a numeric variable with OWL restrictions
    # on the values that can be taken.

    # Create owl:withRestrictions list
    restriction_list = BNode()
    restriction_pylist = []

    # Add all restrictions from the list with a loop
    for restriction in restrictions:

        # Create a BlankNode
        restriction_bnode = BNode()

        # Build it with template
        graph.add((restriction_bnode, restriction[0], Literal(f"{restriction[1]}", datatype=restriction[2])))

        # Add it to the Python list
        restriction_pylist.append(restriction_bnode)

    # Create a BlankNode for the datatype and declare it
    datatype_bnode = BNode()
    graph.add((datatype_bnode, RDF["type"], RDFS["Datatype"]))

    # Create an rdf:List from the Python list of BlankNodes of restrictions
    Collection(graph, restriction_list, restriction_pylist)
 
    # Attach the list to the datatype node
    graph.add((dp_uri, RDFS["range"], datatype_bnode))
    graph.add((datatype_bnode, OWL["onDatatype"], range_n))
    graph.add((datatype_bnode, OWL["withRestrictions"], restriction_list))

    if subproperty_list:
        # Technically not a unified list, so can add them all with a for loop
        for property in subproperty_list:
            graph.add((dp_uri, RDFS["subPropertyOf"], property))

    # Optionally add other types of properties??
    if additional_list:
        for prop_type in additional_list:
            graph.add((dp_uri, RDF["type"], prop_type))

def createOP(
    name: str,
    namespace: Namespace,
    pref_label: Literal,
    graph: Graph,
    domains: Node | list[Node] | None = None,
    ranges: Node | list[Node] | None = None,
    version_of_s: str | None = None,
    references_s: str | None = None,
    subproperty_list: list[Node] | None = None,
    equivalent_property_list: list[Node] | None = None,
    additional_list: list[Node] | None = None,
    definition: Literal | None = None,
    comments: Literal | None = None,
    examples: URIRef | list[URIRef] | None = None,
) -> None:
    """
    Create an OWL ObjectProperty with proper domain, range, and annotations.
   
    Parameters
    ----------
    name: str
        Name to be used for the object property.
    namespace : Namespace
        RDFLib Namespace in which the property URI will be created.
    graph: Graph
        RDFLib Graph where triples will be added.
    domains: Node | list[Node], optional
        A class or a list of one or more domain classes.
    ranges : Node | list[Node], optional
        A class list of one or more range classes.
    additional_list : list[Node], optional
        Other OWL object property types.
    definition: Literal, optional
        Text-based definition of the object property.
    comments: Literal, optional
        Additional comments about the object property.
    examples: Literal, optional
        Example triple about the use of the object property.
    """

    # Create the owl:ObjectProperty URI
    op_uri = namespace[name]

    # Declare the property type (no surprise owl:ObjectProperty)
    graph.add((op_uri, RDF["type"], OWL["ObjectProperty"]))
    graph.add((op_uri, SKOS["prefLabel"], pref_label))

    # Begin with basic annotation properties.
    if definition:
        graph.add((op_uri, SKOS["definition"], definition))
    if comments:
        graph.add((op_uri, RDFS["comment"], comments))

    # Add examples if provided
    if examples:
        if isinstance(examples, URIRef):
            graph.add((op_uri, SKOS["example"], examples))
        elif isinstance(examples, list):
            for example in examples:
                graph.add((op_uri, SKOS["example"], example))

    # Add isDefinedBy
    graph.add((op_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add version info.
    if version_of_s:
        graph.add((op_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((op_uri, DCTERMS["references"], URIRef(references_s)))

    # NOTE: New version using domain
    if domains:
        if isinstance(domains, URIRef):
            graph.add((op_uri, RDFS["domain"], domains))
        elif isinstance(domains, list):
            domain_bnode = BNode()
            Collection(graph, domain_bnode, domains)
            domain_union_class = BNode()
            graph.add((domain_union_class, RDF["type"], OWL["Class"]))
            graph.add((domain_union_class, OWL["unionOf"], domain_bnode))
            graph.add((op_uri, RDFS["domain"], domain_union_class))

    # NOTE: New version using range
    if ranges:
        if isinstance(ranges, URIRef):
            graph.add((op_uri, RDFS["range"], ranges))
        elif isinstance(ranges, list):
            range_bnode = BNode()
            Collection(graph, range_bnode, ranges)
            range_union_class = BNode()
            graph.add((range_union_class, RDF["type"], OWL["Class"]))
            graph.add((range_union_class, OWL["unionOf"], range_bnode))
            graph.add((op_uri, RDFS["range"], range_union_class))

    if subproperty_list:
        # Technically not a unified list, so can add them all with a for loop
        for property in subproperty_list:
            graph.add((op_uri, RDFS["subPropertyOf"], property))

    if equivalent_property_list:
        # Technically not a unified list, so can add them all with a for loop
        for property in equivalent_property_list:
            graph.add((op_uri, OWL["equivalentProperty"], property))

    # Add any additional property types.
    if additional_list:
        for prop_type in additional_list:
            graph.add((op_uri, RDF["type"], prop_type))

def create_CTOP0(
    name: str,
    namespace: Namespace,
    pref_label: Literal,
    graph: Graph,
    object_prop: Node,
    values_list: list[Node],
    use_inverse: bool = False,
    subclass_list: list[Node] | None = None,
    definition: Literal | None = None,
    comments: Literal | None = None,
    examples: Literal | None = None,
    card1_restrictions: list[Node] | None = None,
    card0_restrictions: list[Node] | None = None,
    card01_restrictions: list[Node] | None = None,
) -> None:
    # Create the owl:Class URI
    class_uri = namespace[name]

    # Class declaration
    graph.add((class_uri, RDF["type"], OWL["Class"]))

    if subclass_list:
        # Technically not a unified list, so can add them all with a for loop
        for ro_class in subclass_list:
            graph.add((class_uri, RDFS["subClassOf"], ro_class))

    # Add DEFINEDBY
    graph.add((class_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((class_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((class_uri, SKOS["definition"], definition))

    # Optionally add comments.
    if comments:
        graph.add((class_uri, RDFS["comment"], comments))

    # Optionally add examples.
    if examples:
        graph.add((class_uri, SKOS["example"], examples))

    if use_inverse == True:
        # InvBlank.
        property_node  = BNode()
        graph.add((property_node , RDF["type"], OWL["ObjectProperty"]))
        graph.add((property_node , OWL["inverseOf"], object_prop))
    else:
        property_node = object_prop

    if len(values_list) == 1:
        values_class = values_list[0]
    else:
        values_class = BNode()
        Collection(graph, values_class, values_list)
        range_union_class = BNode()
        graph.add((range_union_class, RDF["type"], OWL["Class"]))
        graph.add((range_union_class, OWL["unionOf"], values_class))

    # OWL Restrictions
    R_class = BNode()
    graph.add((R_class, RDF["type"], OWL["Restriction"]))
    graph.add((R_class, OWL["onProperty"], property_node ))
    graph.add((R_class, OWL["someValuesFrom"], values_class))

    # owl:equivalentClass via owl:intersectionOf.
    #graph.add((class_uri, RDFS["subClassOf"], R_class))
    graph.add((class_uri, OWL["equivalentClass"], R_class))

    if any(restriction is not None for restriction in (card1_restrictions, card0_restrictions, card01_restrictions)):
        # OWL Restrictions.
        entity_pylist = []

        if card1_restrictions:
            for property in card1_restrictions:
                R_BNode = BNode()
                graph.add((R_BNode, RDF["type"], OWL["Restriction"]))
                graph.add((R_BNode, OWL["onProperty"], property))
                graph.add((R_BNode, OWL["cardinality"], Literal(1, datatype=XSD["nonNegativeInteger"])))
                entity_pylist.append(R_BNode)

        if card0_restrictions:
            for property in card0_restrictions:
                R_BNode = BNode()
                graph.add((R_BNode, RDF["type"], OWL["Restriction"]))
                graph.add((R_BNode, OWL["onProperty"], property))
                graph.add((R_BNode, OWL["minCardinality"], Literal(0, datatype=XSD["nonNegativeInteger"])))
                entity_pylist.append(R_BNode)

        if card01_restrictions:
            for property in card01_restrictions:
                R0_BNode = BNode()
                graph.add((R0_BNode, RDF["type"], OWL["Restriction"]))
                graph.add((R0_BNode, OWL["onProperty"], property))
                graph.add((R0_BNode, OWL["minCardinality"], Literal(0, datatype=XSD["nonNegativeInteger"])))
                entity_pylist.append(R0_BNode)

                R1_BNode = BNode()
                graph.add((R1_BNode, RDF["type"], OWL["Restriction"]))
                graph.add((R1_BNode, OWL["onProperty"], property))
                graph.add((R1_BNode, OWL["maxCardinality"], Literal(1, datatype=XSD["nonNegativeInteger"])))
                entity_pylist.append(R1_BNode)

        # rdfs:subclassOf via owl:intersectionOf.
        Entity_intersection = BNode()
        Entity_list = BNode()
        Collection(graph, Entity_list, entity_pylist)
        graph.add((Entity_intersection, RDF["type"], OWL["Class"]))
        graph.add((Entity_intersection, OWL["intersectionOf"], Entity_list))
        graph.add((class_uri, RDFS["subClassOf"], Entity_intersection))

# NOTE: Through the use of rdfs:range, I can get by with just owl:someValuesFrom (i.e. an existential constraint).
# WARN: Apply the same logic regarding restrictions to createCTOP
def createCTOP(
    name: str,
    namespace: Namespace,
    pref_label: Literal,
    graph: Graph,
    object_prop: Node,
    values_class: Node,
    use_inverse: bool = False,
    subclass_of: Node | list[Node] | None = None,
    definition: Literal | None = None,
    comments: Literal | None = None,
    examples: Literal | None = None,
    card1_restrictions: list[Node] | None = None,
    maxcard1_restrictions: list[Node] | None = None,
) -> None:
    # Create the owl:Class URI.
    class_uri = namespace[name]

    # Class declaration.
    graph.add((class_uri, RDF["type"], OWL["Class"]))

    if subclass_of:
        if isinstance(subclass_of, Node):
            graph.add((class_uri, RDFS["subClassOf"], subclass_of))
        # Technically not a unified list, so can add them all with a for loop.
        elif isinstance(subclass_of, list) and all(isinstance(x, Node) for x in subclass_of):
            for ro_class in subclass_of:
                graph.add((class_uri, RDFS["subClassOf"], ro_class))
        # NOTE: Maybe add myself a message if not a Node or a list of Nodes

    # Add rdfs:isDefinedBy
    graph.add((class_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((class_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((class_uri, SKOS["definition"], definition))

    # Optionally add comments.
    if comments:
        graph.add((class_uri, RDFS["comment"], comments))

    # Optionally add examples.
    if examples:
        graph.add((class_uri, SKOS["example"], examples))

    if use_inverse == True:
        # InvBlank.
        property_node  = BNode()
        graph.add((property_node , RDF["type"], OWL["ObjectProperty"]))
        graph.add((property_node , OWL["inverseOf"], object_prop))
    else:
        property_node = object_prop

    # OWL Restrictions
    R_class = BNode()
    graph.add((R_class, RDF["type"], OWL["Restriction"]))
    graph.add((R_class, OWL["onProperty"], property_node ))
    graph.add((R_class, OWL["someValuesFrom"], values_class))

    # owl:equivalentClass via owl:intersectionOf.
    #graph.add((class_uri, RDFS["subClassOf"], R_class))
    graph.add((class_uri, OWL["equivalentClass"], R_class))

    if any(restriction is not None for restriction in (card1_restrictions, maxcard1_restrictions)):
        # OWL Restrictions.
        entity_pylist = []

        if card1_restrictions:
            for property in card1_restrictions:
                R_BNode = BNode()
                graph.add((R_BNode, RDF["type"], OWL["Restriction"]))
                graph.add((R_BNode, OWL["onProperty"], property))
                graph.add((R_BNode, OWL["cardinality"], Literal(1, datatype=XSD["nonNegativeInteger"])))
                entity_pylist.append(R_BNode)

        if maxcard1_restrictions:
            for property in maxcard1_restrictions:
                R_BNode = BNode()
                graph.add((R_BNode, RDF["type"], OWL["Restriction"]))
                graph.add((R_BNode, OWL["onProperty"], property))
                graph.add((R_BNode, OWL["maxCardinality"], Literal(1, datatype=XSD["nonNegativeInteger"])))
                entity_pylist.append(R_BNode)

        # rdfs:subclassOf via owl:intersectionOf.
        Entity_intersection = BNode()
        Entity_list = BNode()
        Collection(graph, Entity_list, entity_pylist)
        graph.add((Entity_intersection, RDF["type"], OWL["Class"]))
        graph.add((Entity_intersection, OWL["intersectionOf"], Entity_list))
        graph.add((class_uri, RDFS["subClassOf"], Entity_intersection))

def declare_disjoint(
        classes: list[Node],
        graph: Graph
) -> None:
    # Create a blank node for the disjointness axiom.
    disjoint_node = BNode()

    # Declare it as an owl:AllDisjointClasses.
    graph.add((disjoint_node, RDF["type"], OWL["AllDisjointClasses"]))

    # Create a blank node for the RDF list of members.
    members_list = BNode()
    Collection(graph, members_list, classes)

    # Link the list to the disjoint axiom.
    graph.add((disjoint_node, OWL["members"], members_list))



# TEST: Function that creates an owl:Class but allows only a finite set of possibilities
# These possibilities are owl:NamedIndividuals
def createEOC(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        one_of: list[Node],
        version_of_s: str | None = None,
        subclass_list: list[Node] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        examples: Literal | list[Literal] | None = None,
        references_s: str | None = None,
        ) -> None:
    # Create the owl:Class URI
    oc_uri = namespace[name]
    
    # NOTE: This declaration might be obsolete due to the use of owl:equivalentClass below
    # Class declaration.
    graph.add((oc_uri, RDF["type"], OWL["Class"]))

    # Declaration as a subclass of skos:Concept.
    graph.add((oc_uri, RDFS["subClassOf"], SKOS["Concept"]))

    # Add DEFINEDBY
    graph.add((oc_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((oc_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((oc_uri, SKOS["definition"], definition))

    # Optionally add comments.
    if comments:
        graph.add((oc_uri, RDFS["comment"], comments))

    # Add examples if provided
    if examples:
        if isinstance(examples, URIRef):
            graph.add((oc_uri, SKOS["example"], examples))
        elif isinstance(examples, list):
            for example in examples:
                graph.add((oc_uri, SKOS["example"], example))

    # Add version info.
    if version_of_s:
        graph.add((oc_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((oc_uri, DCTERMS["references"], URIRef(references_s)))

    # Declare it in the graph
    graph.add((oc_uri, RDF["type"], OWL["Class"]))
    
    # WARN: If a list of URIs is provided, these will form the finite
    # set of possible values the owl:Class can take
    if one_of:
        # Create RDF list of the enumeration values
        enum_list_bnode = BNode()
        Collection(graph, enum_list_bnode, one_of)

        # Attach owl:oneOf list to the owl:Class
        graph.add((oc_uri, OWL["oneOf"], enum_list_bnode))
        
    if subclass_list:
        # Technically not a unified list, so can add them all with a for loop
        for class_ in subclass_list:
            graph.add((oc_uri, RDFS["subClassOf"], class_))

    # Declare each individual as an instance of the created class
    # NOTE: This is just making it explicit, either way the reasoner
    # would find it
    for one in one_of:
        graph.add((one, RDF["type"], oc_uri))

# TEST: Function that defines a skos:Concept with pertinent information
def createSC(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        definition: Literal | None = None,
        comments: Literal | None = None,
        broader: URIRef | None = None,
        in_scheme: Node | None = None,
        version_of_s: str | None = None,
        references_s: str | None = None,
        ) -> None:
    # Create the skos:Concept URI
    sc_uri = namespace[name]

    # Add DEFINEDBY
    graph.add((sc_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((sc_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((sc_uri, SKOS["definition"], definition))
        # graph.add((sc_uri, DC["description"], definition))

    # Optionally add comments.
    if comments:
        graph.add((sc_uri, RDFS["comment"], comments))

    # Add version info.
    graph.add((sc_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((sc_uri, DCTERMS["references"], URIRef(references_s)))

    # Possibly add broader relationships
    if broader:
        graph.add((sc_uri, SKOS["broader"], broader))

    if in_scheme:
        graph.add((sc_uri, SKOS["inScheme"], in_scheme))

    # Declare it in the graph
    # graph.add((sc_uri, RDF["type"], SKOS["Concept"]))
   
# TEST: Function that defines a skos:Concept with pertinent information
def createSCS(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        definition: Literal | None = None,
        comments: Literal | None = None,
        version_of_s: str | None = None,
        references_s: str | None = None,
        ) -> None:
    # Create the skos:ConceptScheme URI
    scs_uri = namespace[name]

    # Declare it in the graph
    # graph.add((scs_uri, RDF["type"], SKOS["ConceptScheme"]))
 
    # Add DEFINEDBY
    graph.add((scs_uri, RDFS["isDefinedBy"], URIRef(str(namespace))))

    # Add preferred label.
    graph.add((scs_uri, SKOS["prefLabel"], pref_label))

    # Optionally add definition.
    if definition:
        graph.add((scs_uri, SKOS["definition"], definition))

    # Optionally add comments.
    if comments:
        graph.add((scs_uri, RDFS["comment"], comments))

    # Add version info.
    graph.add((scs_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((scs_uri, DCTERMS["references"], URIRef(references_s)))

  


def createNI(
        uri_s: str,
        class_of: Node,
        graph: Graph,
        pref_label: Literal,
        version_of_s: str,
        definition: Literal | None = None,
        comments: Literal | None = None,
        references_s: str | None = None,
) -> None:
    """
    Define an OWL named individual
    """

    # Define named individual URI
    named_individual_uri = URIRef(uri_s)

    # Add DEFINEDBY
    graph.add((named_individual_uri, RDF["type"], class_of))
    graph.add((named_individual_uri, SKOS["prefLabel"], pref_label))

    if definition:
        graph.add((named_individual_uri, SKOS["definition"], definition))
    if comments:
        graph.add((named_individual_uri, RDFS["comment"], comments))

    # Add version info.
    graph.add((named_individual_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((named_individual_uri, DCTERMS["references"], URIRef(references_s)))

