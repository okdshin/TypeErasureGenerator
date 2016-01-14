namespace {parent_namespace_name} {{
	namespace {namespace_name} {{
		namespace traits {{
			template<typename T>
			class {function_name} {{
				static decltype(auto) call(T {const}& t, {params}) {noexcept} {{
					t.{function_name}({args});
				}}
			}};
		}}
		template<typename T>
		decltype(auto) {function_name}(T {const}& t, {params}) {noexcept} {{
			::{parent_namespace_name}::{namespace_name}::traits::{function_name}<T>::call(t, {args});
		}}
	}}
}}
