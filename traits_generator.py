# coding: utf-8
import sys
import os
import json

def generate_traits(params, dest_dir):
    include_headers = params["include_headers"]

    include_headers_template = "#include <{header}>"
    include_headers_list = []
    for include_header in include_headers:
        include_headers_list.append(
            include_headers_template.format(header=include_header))

    traits_source_list = [
        "#ifndef {capital_parent_namespace_name}_{capital_namespace_name}_TRAITS_HPP\n#define {capital_parent_namespace_name}_{capital_namespace_name}_TRAITS_HPP".format(
            capital_parent_namespace_name=params["parent_namespace_name"].upper(),
            capital_namespace_name=params["namespace_name"].upper()),
        "\n".join(include_headers_list),
        ""
    ]
    functions = params["functions"]
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template", "traits_template.cpp")) as templatef:
        template = templatef.read()
        for function in functions:
            traits_source_list.append(template.format(
                comma="," if function["params"] != "" else "",
                return_="" if function["return_type"] == "void" else "return",
                parent_namespace_name=params["parent_namespace_name"],
                namespace_name=params["namespace_name"],
                **function))
    traits_source_list.append("#endif // {capital_parent_namespace_name}_{capital_namespace_name}_TRAITS_HPP".format(
            capital_parent_namespace_name=params["parent_namespace_name"].upper(),
            capital_namespace_name=params["namespace_name"].upper()
        ))

    with open(os.path.join(dest_dir, params["traits_file_name"]), "w") as resultf:
        resultf.write("\n".join(traits_source_list))

def main():
    jsonf = open(sys.argv[1])
    params = json.load(jsonf)

    dest_dir = sys.argv[2]

    generate_traits(params, dest_dir)

if __name__ == "__main__":
    main()
