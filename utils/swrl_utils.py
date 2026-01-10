from rdflib import Graph, BNode, Namespace, Node
from rdflib.namespace import RDF
from rdflib.collection import Collection

SWRL = Namespace("http://www.w3.org/2003/11/swrl#")

# Needs to return something since you are not just adding but are going to reuse it
def create_swrl_variable(
    graph: Graph,
) -> BNode:
    variable_node = BNode()

    graph.add((variable_node, RDF["type"], SWRL["Variable"]))

    return variable_node


# Needs to return something since you are not just adding but are going to reuse it
def swrl_class_atom(
    graph: Graph,
    class_: Node,
    swrl_arg: Node,
) -> BNode:
    class_atom = BNode()

    graph.add((class_atom, RDF["type"], SWRL["ClassAtom"]))
    graph.add((class_atom, SWRL["classPredicate"], class_))
    graph.add((class_atom, SWRL["argument1"], swrl_arg))

    return class_atom

# Same thing here, you need to return it to use it in a list
def swrl_property_atom(
    graph: Graph,
    property_: Node,
    swrl_arg1: Node,
    swrl_arg2: Node,
) -> BNode:
    property_atom = BNode()

    graph.add((property_atom, RDF["type"], SWRL["IndividualPropertyAtom"]))
    graph.add((property_atom, SWRL["propertyPredicate"], property_))
    graph.add((property_atom, SWRL["argument1"], swrl_arg1))
    graph.add((property_atom, SWRL["argument2"], swrl_arg2))

    return property_atom

def add_swrl_rule(
    graph: Graph,
    body_atoms: list[Node],
    head_atoms: list[Node],
) -> None:

    swrl_rule = BNode()
    graph.add((swrl_rule, RDF["type"], SWRL["Imp"]))

    # Body (antecedent)
    body = BNode()
    graph.add((body, RDF["type"], SWRL["AtomList"]))
    Collection(graph, body, body_atoms)
    graph.add((swrl_rule, SWRL["body"], body))

    # Head (consequent)
    head = BNode()
    graph.add((head, RDF["type"], SWRL["AtomList"]))
    Collection(graph, head, head_atoms)
    graph.add((swrl_rule, SWRL["head"], head))

















