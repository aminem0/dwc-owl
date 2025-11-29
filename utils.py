from rdflib import BNode, Graph, Literal, Namespace, Node, URIRef
from rdflib.collection import Collection
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

# WARN: Rewriting this function.
# For some reason, card0_restrictions seems like a useless parameter.
# It is something that is already stated by stating that a property has
# a specific domain.
# The only notions that we "should" take into account is:
# owl:cardinality of 1 for properties that NEED to be present
# owl:maxCardinality of 1 for properties that can be absent, but if they
# are present, MUST NOT EXCEED 1
# Other properties should be valid under the OWA
def createOC(
        name: str,
        namespace: Namespace,
        graph: Graph,
        pref_label: Literal,
        version_of_s: str,
        subclass_list: list[Node] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        examples_list: list[Literal] | None = None,
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
    if examples_list:
        for example in examples_list:
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

    if any(restriction is not None for restriction in (card1_restrictions, maxcard1_restrictions)):
        # OWL Restrictions
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
                R1_BNode = BNode()
                graph.add((R1_BNode, RDF["type"], OWL["Restriction"]))
                graph.add((R1_BNode, OWL["onProperty"], property))
                graph.add((R1_BNode, OWL["maxCardinality"], Literal(1, datatype=XSD["nonNegativeInteger"])))
                entity_pylist.append(R1_BNode)

        # rdfs:subclassOf via owl:intersectionOf
        Entity_intersection = BNode()
        Entity_list = BNode()
        Collection(graph, Entity_list, entity_pylist)
        graph.add((Entity_intersection, RDF["type"], OWL["Class"]))
        graph.add((Entity_intersection, OWL["intersectionOf"], Entity_list))
        graph.add((class_uri, RDFS["subClassOf"], Entity_intersection))

def createDP(
        name: str,
        namespace: Namespace,
        graph: Graph,
        domain_list: list[Node],
        range_list: list[Node],
        pref_label: Literal,
        version_of_s: str,
        subproperty_list: list[Node] | None = None,
        additional_list: list[Node] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        # examples: Literal | None = None,
        examples_list: list[Literal] | None = None,
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

    # Optionally add examples.
    # if examples:
    #     graph.add((dp_uri, SKOS["example"], examples))
    if examples_list:
        for example in examples_list:
            graph.add((dp_uri, SKOS["example"], example))

    # Add version info.
    graph.add((dp_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((dp_uri, DCTERMS["references"], URIRef(references_s)))

    # Declare it in the graph
    graph.add((dp_uri, RDF["type"], OWL["DatatypeProperty"]))

    # If just one domain, take it and go.
    if len(domain_list) == 1:
        graph.add((dp_uri, RDFS["domain"], domain_list[0]))
   
    # Otherwise do the blank node process.
    else:
        # Create blank node to contain union list
        domain_bnode = BNode()
   
        # Fill it with
        Collection(graph, domain_bnode, domain_list)

        # Define the union of classes for the domain class
        domain_union_class = BNode()
        graph.add((domain_union_class, RDF["type"], OWL["Class"]))
        graph.add((domain_union_class, OWL["unionOf"], domain_bnode))

        # Define the domain of the owl:DatatypeProperty
        graph.add((dp_uri, RDFS["domain"], domain_union_class))

    # If just one range, take it and go.
    if len(range_list) == 1:
        graph.add((dp_uri, RDFS["range"], range_list[0]))

    # Otherwise do the blank node process.
    else:
        # Create blank node to contain union list
        range_bnode = BNode()

        # Fill it with
        Collection(graph, range_bnode, range_list)

        # Define the union of classes for the range datatype
        # WARN: Verify RDFS term
        range_union_datatype = BNode()
        graph.add((range_union_datatype, RDF["type"], RDFS["Datatype"]))
        graph.add((range_union_datatype, OWL["unionOf"], range_bnode))

        # Define the range of the owl:DatatypeProperty
        graph.add((dp_uri, RDFS["range"], range_union_datatype))

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
        domain_list: list[Node],
        oneOf_list: list[Node],
        pref_label: Literal,
        version_of_s: str,
        subproperty_list: list[Node] | None = None,
        additional_list: list[Node] | None = None,
        definition: Literal | None = None,
        comments: Literal | None = None,
        # examples: Literal | None = None,
        examples_list: list[Literal] | None = None,
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

    # Optionally add examples.
    # if examples:
    #     graph.add((dp_uri, SKOS["example"], examples))
    if examples_list:
        for example in examples_list:
            graph.add((dp_uri, SKOS["example"], example))

    # Add version info.
    graph.add((dp_uri, DCTERMS["isVersionOf"], URIRef(version_of_s)))

    if references_s:
        graph.add((dp_uri, DCTERMS["references"], URIRef(references_s)))

    # Declare it in the graph
    graph.add((dp_uri, RDF["type"], OWL["DatatypeProperty"]))

    # If just one domain, take it and go.
    if len(domain_list) == 1:
        graph.add((dp_uri, RDFS["domain"], domain_list[0]))
   
    # Otherwise do the blank node process.
    else:
        # Create blank node to contain union list
        domain_bnode = BNode()
   
        # Fill it with
        Collection(graph, domain_bnode, domain_list)

        # Define the union of classes for the domain class
        domain_union_class = BNode()
        graph.add((domain_union_class, RDF["type"], OWL["DataRange"]))
        graph.add((domain_union_class, OWL["unionOf"], domain_bnode))

        # Define the domain of the owl:DatatypeProperty
        graph.add((dp_uri, RDFS["domain"], domain_union_class))

    # WARN: Here goes a rewrite to consider an enumeration of all allowed datatypes
    # If enumerated literals are provided, build an OWL datatype with owl:oneOf and
    # a Collection of allowable litterals
    if oneOf_list:
        # Create a blank node for the enumerated datatype
        enum_datatype = BNode()
        graph.add((enum_datatype, RDF["type"], RDFS["Datatype"]))

        # Create RDF list of the enumeration values
        enum_list_bnode = BNode()
        Collection(graph, enum_list_bnode, oneOf_list)

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
    additional_list: list[Node] | None = None,
    definition: Literal | None = None,
    comments: Literal | None = None,
    # examples_list: list[Literal] | None = None,
    examples: URIRef | list[URIRef] | None = None,
) -> None:
    """
    Create an OWL ObjectProperty with proper domain, range, and annotations.
   
    Parameters
    ----------
    name: str
        Name to be used for the property.
    namespace : Namespace
        RDFLib Namespace in which the property URI will be created.
    graph: Graph
        RDFLib Graph where triples will be added.
    domain_list: list[Node]
        A list of one or more domain classes.
    range_list : list[Node]
        A list of one or more range classes.
    additional_list : list[Node], optional
        Other OWL object property types.
    definition: Literal, optional
        Text-based definition of the object property.
    comments: Literal, optional
        Additional comments about the object property.
    examples : Literal, optional
        Example triple about the use of the object property.
       
    Returns
    -------
    Graph
        The updated RDFLib Graph containing the new ObjectProperty definition.
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
    # if examples:
    #     graph.add((op_uri, SKOS["example"], examples))
    # if examples_list:
    #     for example in examples_list:
    #         graph.add((op_uri, SKOS["example"], example))

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


    # If there is only a single element in the list, take it as the range
    # otherwise consider a blank node that is the intersect
    # NOTE: Eventually, it would be best to have the function accept either
    # an Node or a list of Nodes.
    # if len(domain_list) == 1:
    #     graph.add((op_uri, RDFS["domain"], domain_list[0]))
    # else:
    #     domain_bnode = BNode()
    #     Collection(graph, domain_bnode, domain_list)
    #     domain_union_class = BNode()
    #     graph.add((domain_union_class, RDF["type"], OWL["Class"]))
    #     graph.add((domain_union_class, OWL["unionOf"], domain_bnode))
    #     graph.add((op_uri, RDFS["domain"], domain_union_class))

    # if domain_list:
    #     if len(domain_list) == 1:
    #         graph.add((op_uri, RDFS["domain"], domain_list[0]))
    #     else:
    #         domain_bnode = BNode()
    #         Collection(graph, domain_bnode, domain_list)
    #         domain_union_class = BNode()
    #         graph.add((domain_union_class, RDF["type"], OWL["Class"]))
    #         graph.add((domain_union_class, OWL["unionOf"], domain_bnode))
    #         graph.add((op_uri, RDFS["domain"], domain_union_class))

    # TEST: Add all domains with a for loop.
    # for domain in domain_list:
    #     graph.add((op_uri, RDFS["domain"], domain))

    # If there is only a single element in the list, take it as the range
    # otherwise consider a blank node that is the intersect
    # NOTE: Eventually, it would be best to have the function accept either
    # an Node or a list of Nodes.
    # if len(range_list) == 1:
    #     graph.add((op_uri, RDFS["range"], range_list[0]))
    # else:
    #     range_bnode = BNode()
    #     Collection(graph, range_bnode, range_list)
    #     range_union_class = BNode()
    #     graph.add((range_union_class, RDF["type"], OWL["Class"]))
    #     graph.add((range_union_class, OWL["unionOf"], range_bnode))
    #     graph.add((op_uri, RDFS["range"], range_union_class))
    # if range_list:
    #     if len(range_list) == 1:
    #         graph.add((op_uri, RDFS["range"], range_list[0]))
    #     else:
    #         range_bnode = BNode()
    #         Collection(graph, range_bnode, range_list)
    #         range_union_class = BNode()
    #         graph.add((range_union_class, RDF["type"], OWL["Class"]))
    #         graph.add((range_union_class, OWL["unionOf"], range_bnode))
    #         graph.add((op_uri, RDFS["range"], range_union_class))

    if subproperty_list:
        # Technically not a unified list, so can add them all with a for loop
        for property in subproperty_list:
            graph.add((op_uri, RDFS["subPropertyOf"], property))

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
    subclass_list: list[Node] | None = None,
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

    if subclass_list:
        # Technically not a unified list, so can add them all with a for loop.
        for ro_class in subclass_list:
            graph.add((class_uri, RDFS["subClassOf"], ro_class))

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


