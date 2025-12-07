from pathlib import Path
import re
import subprocess

# Define URIs for unsatisfiable entities.
#
owl_nothing_uri_s = "http://www.w3.org/2002/07/owl#Nothing"
owl_bottom_object_property_uri_s = "http://www.w3.org/2002/07/owl#bottomObjectProperty"
owl_bottom_data_property_uri_s = "http://www.w3.org/2002/07/owl#bottomDataProperty"

# HermiT expects a URI as input, so get that.
#
ontology_uri = (Path(__file__).parent.parent / "ontology/dwc-owl-v2.ttl").resolve().as_uri()

print(ontology_uri)

# Use HermiT as validation that there are no unsatisfiable things.
#
single_classification = subprocess.run(["java", "-jar", "jarfiles/HermiT.jar", "-cOD", ontology_uri], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# WARN: Add a first test to detect if HermiT detects an inconsistency as a whole and prints out nothing.
# This is the result of (I assume) a global inconsistency between A-Box and T-Box
# Would require manual inspection of the clauses with --dump-clauses=clauses.txt
#
if single_classification.returncode == 1:
    print("+ Ontology is globally inconsistent.")
    print("+ Probably an A-Box and T-Box conflict.")

elif single_classification.returncode == 0:

    # NOTE: There seems to be only a single line since equivalency is concatenated
    # Extract the lines, if any
    #
    owl_nothing_line = next((line for line in single_classification.stdout.splitlines() if owl_nothing_uri_s in line), None)
    owl_bottom_object_property_line = next((line for line in single_classification.stdout.splitlines() if owl_bottom_object_property_uri_s in line), None)
    owl_bottom_data_property_line = next((line for line in single_classification.stdout.splitlines() if owl_bottom_data_property_uri_s in line), None)

    # Find the URIs and print them, if any
    #
    if owl_nothing_line:
        # Extract all URIs
        owl_nothing_uris = re.findall(r"<[^>]+>", owl_nothing_line)
        
        # Print number of URIs equivalent
        print(f"+ Number of URIs equivalent to owl:Nothing: {len(owl_nothing_uris)}")

        # Print out each URI
        for uri in owl_nothing_uris:
            print(f"- {uri}")
    else:
        # Print regular success message
        print(f"+ No URIs in the ontology are equivalent to owl:Nothing")


    if owl_bottom_object_property_line:
        # Extract all URIs
        owl_bottom_object_property_uris = re.findall(r"<[^>]+>", owl_bottom_object_property_line)
        
        # Print number of URIs equivalent
        print(f"\n+ Number of URIs equivalent to owl:bottomObjectProperty: {len(owl_bottom_object_property_uris)}")

        # Print out each URI
        for uri in owl_bottom_object_property_uris:
            print(f"- {uri}")
    else:
        # Print regular success message
        print(f"\n+ No URIs in the ontology are equivalent to owl:bottomObjectProperty")


    if owl_bottom_data_property_line:
        # Extract all URIs
        owl_bottom_data_property_uris = re.findall(r"<[^>]+>", owl_bottom_data_property_line)
        
        # Print number of URIs equivalent
        print(f"\n+ Number of URIs equivalent to owl:bottomDataProperty: {len(owl_bottom_data_property_uris)}")

        # Print out each URI
        for uri in owl_bottom_data_property_uris:
            print(f"- {uri}")
    else:
        # Print regular success message
        print(f"\n+ No URIs in the ontology are equivalent to owl:bottomDataProperty")