namespace {parent_namespace_name} {{
	namespace {namespace_name} {{
		namespace traits {{
			template<typename T>
			class {function_name} {{
			public:
				static decltype(auto) call(T {const}& t{comma} {params}) {noexcept} {{
					{return_} t.{function_name}({args});
				}}
			}};
		}}
		template<typename T>
		decltype(auto) {function_name}(T {const}& t{comma} {params}) {noexcept} {{
			{return_} ::{parent_namespace_name}::{namespace_name}::traits::{function_name}<T>::call(t{comma} {args});
		}}
	}}
}}
