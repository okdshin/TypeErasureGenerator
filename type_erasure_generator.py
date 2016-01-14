# coding: utf-8
import sys
import os
import json

def generate_any(params, dest_dir):
    include_headers = params["include_headers"]

    include_headers_template = """#include <{header}>"""
    include_headers_list = []
    for include_header in include_headers:
        include_headers_list.append(
            include_headers_template.format(header=include_header))
    include_headers_list.append("#include <{parent_namespace_name}/{namespace_name}/traits.hpp>".format(parent_namespace_name=params["parent_namespace_name"], namespace_name=params["namespace_name"]))

    functions = params["functions"]

    holder_base_mem_funcs_template = "\t\t\t\tvirtual {return_type} {function_name}({params}) {const} {noexcept} = 0;"
    holder_base_member_function_list = []
    for function in functions:
        holder_base_member_function_list.append(
            holder_base_mem_funcs_template.format(**function))

    holder_mem_funcs_template = "\t\t\t\t{return_type} {function_name}({params}) {const} {noexcept} override {{\n\t\t\t\t\t{return_} ::{parent_namespace_name}::{namespace_name}::{function_name}(t_{comma} {args});\n\t\t\t\t}}"
    holder_member_function_list = []
    for function in functions:
        holder_member_function_list.append(
            holder_mem_funcs_template.format(
                **function,
                comma="," if function["params"] != "" else "",
                return_="" if function["return_type"] == "void" else "return ",
                parent_namespace_name=params["parent_namespace_name"],
                namespace_name=params["namespace_name"]))

    mem_funcs_template = "\t\t\t{return_type} {function_name}({params}) {const} {noexcept} {{\n\t\t\t\t{return_} holder_->{function_name}({args});\n\t\t\t}}"
    member_function_list = []
    for function in functions:
        member_function_list.append(
            mem_funcs_template.format(
                return_="" if function["return_type"] == "void" else "return ",
                **function))

    generated_source = ""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template", "any_template.cpp")) as templatef:
        generated_source = templatef.read().format(
            include_headers="\n".join(include_headers_list),
            name=params["name"],
            parent_namespace_name=params["parent_namespace_name"],
            namespace_name=params["namespace_name"],
            holder_base_member_functions="\n".join(holder_base_member_function_list),
            holder_member_functions="\n".join(holder_member_function_list),
            member_functions="\n".join(member_function_list))

    with open(os.path.join(dest_dir, "{name}.cpp").format(name=params["name"]), "w") as resultf:
        resultf.write(generated_source)

def generate_traits(params, dest_dir):
    include_headers = params["include_headers"]

    include_headers_template = """#include <{header}>"""
    include_headers_list = []
    for include_header in include_headers:
        include_headers_list.append(
            include_headers_template.format(header=include_header))

    traits_source_list = ["\n".join(include_headers_list), ""]
    functions = params["functions"]
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template", "traits_template.cpp")) as templatef:
        template = templatef.read()
        for function in functions:
            traits_source_list.append(template.format(
                comma="," if function["params"] != "" else "",
                return_="" if function["return_type"] == "void" else "return ",
                parent_namespace_name=params["parent_namespace_name"],
                namespace_name=params["namespace_name"],
                **function))

    with open(os.path.join(dest_dir, "traits.cpp"), "w") as resultf:
        resultf.write("\n".join(traits_source_list))

def main():
    jsonf = open(sys.argv[1])
    params = json.load(jsonf)

    dest_dir = sys.argv[2]

    generate_any(params, dest_dir)
    generate_traits(params, dest_dir)

if __name__ == "__main__":
    main()
