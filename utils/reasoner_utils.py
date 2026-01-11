from pathlib import Path
import subprocess
import tempfile
from rdflib import Graph, URIRef

def call_reasoner(
    graph: Graph,
    reasoner: str = "hermit",
    axiom_generators: list[str] = ["ClassAssertion", "PropertyAssertion"]
) -> Graph:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        tmp_path_pre = tmpdir / "input.ttl"
        tmp_path_post = tmpdir / "output.ttl"

        graph.serialize(destination=tmp_path_pre, format="turtle")

        subprocess.run(
            [
                "java",
                "-jar",
                "jarfiles/robot.jar",
                "reason",
                "--reasoner",
                reasoner,
                "--axiom-generators",
                " ".join(ax for ax in axiom_generators),
                "--input",
                tmp_path_pre,
                "--output",
                tmp_path_post,
            ],
            stderr=subprocess.DEVNULL,
        )

        g_post = Graph()
        g_post.parse(source=tmp_path_post)

    return g_post


def reason_with_ontology(
    graph: Graph,
    ontology_url: str,
) -> Graph:

    # res_set = {x for s, _, o in graph for x in (s, o) if isinstance(x, URIRef)}

    res_set = {
        x
        for subj, _, obj in graph
        for x in (subj, obj)
        if isinstance(x, URIRef)
    }

    uri_block = " ".join(f"<{subj}>" for subj in res_set)

    graph_pre = Graph()

    for triple in graph:
        graph_pre.add(triple)

    # for prefix, namespace in graph.namespaces():
        # graph_pre.bind(prefix, namespace)

    graph_pre.parse(source=ontology_url)

    graph_post = call_reasoner(graph_pre)

    sparql_result = graph_post.query(
        f"""
        DESCRIBE {uri_block}
        """
    )

    out = sparql_result.graph

    for prefix, namespace in graph.namespaces():
        out.bind(prefix, namespace)

    return out


from rdflib.namespace import RDF

def reason_with_ontology2(
    graph: Graph,
    ontology_url: str,
) -> Graph:

    # res_set = {x for s, _, o in graph for x in (s, o) if isinstance(x, URIRef)}

    resource_set = {
        x
        for subj, _, obj in graph
        for x in (subj, obj)
        if isinstance(x, URIRef)
    }

    type_set = {
        obj
        for _, _, obj
        in graph.triples((None, RDF["type"], None))
    }

    print(resource_set)
    print(type_set)

    resource_set = resource_set - type_set

    uri_block = " ".join(f"<{subj}>" for subj in resource_set)

    graph_pre = Graph()

    for triple in graph:
        graph_pre.add(triple)

    # for prefix, namespace in graph.namespaces():
        # graph_pre.bind(prefix, namespace)

    graph_pre.parse(source=ontology_url)

    graph_post = call_reasoner(graph_pre)

    sparql_result = graph_post.query(
        f"""
        DESCRIBE {uri_block}
        """
    )

    out = sparql_result.graph

    for prefix, namespace in graph.namespaces():
        out.bind(prefix, namespace)

    return out


def reason_with_ontology3(
    graph: Graph,
    ontology_url: str,
) -> Graph:

    # res_set = {x for s, _, o in graph for x in (s, o) if isinstance(x, URIRef)}

    resource_set = {
        x
        for subj, _, obj in graph
        for x in (subj, obj)
        if isinstance(x, URIRef)
    }

    type_set = {
        obj
        for _, _, obj
        in graph.triples((None, RDF["type"], None))
    }

    print(resource_set)
    print(type_set)

    # resource_set = resource_set - type_set

    uri_block = " ".join(f"<{subj}>" for subj in resource_set)

    graph_pre = Graph()

    for triple in graph:
        graph_pre.add(triple)

    # for prefix, namespace in graph.namespaces():
        # graph_pre.bind(prefix, namespace)

    graph_pre.parse(source=ontology_url)

    graph_post = call_reasoner(graph_pre)

    sparql_query = f"""
        SELECT ?subj ?pred ?obj
        WHERE {{
        VALUES ?obj {{ {uri_block} }}
        ?subj ?pred ?obj .
        }}
        """

    print(sparql_query)

    sparql_result = graph_post.query(
        sparql_query
            )

    out = sparql_result.graph

    for prefix, namespace in graph.namespaces():
        out.bind(prefix, namespace)

    return out


