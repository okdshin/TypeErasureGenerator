#include <type_traits>
#include <utility>
#include <memory>

{include_headers}

namespace {parent_namespace_name} {{
	namespace {namespace_name} {{
		namespace {name}_impl {{
			class {name}_holder_base {{
			public:
				{name}_holder_base() = default;
				{name}_holder_base({name}_holder_base const&) = default;
				{name}_holder_base& operator=({name}_holder_base const&) = default;
				{name}_holder_base& operator=({name}_holder_base&&) = default;
				virtual ~{name}_holder_base() noexcept = default;

				virtual std::unique_ptr<{name}_holder_base> clone() = 0;

{holder_base_member_functions}
			}};

			template<typename T>
			class {name}_holder : public {name}_holder_base {{
			public:
				{name}_holder() = default;
				{name}_holder({name}_holder const&) = default;
				{name}_holder& operator=({name}_holder const&) = default;
				{name}_holder& operator=({name}_holder&&) = default;
				~{name}_holder() noexcept = default;

				std::unique_ptr<{name}_holder_base> clone() override {{
					return std::make_unique_ptr<{name}_holder>(*this);
				}}

				template<typename U>
				explicit {name}_holder(U&& u) 
					: {name}_holder_base{{}}, t_{{std::forward<U>(u)}} {{}}

{holder_member_functions}

			private:
				T t_;
			}};
		}}

		class {name} {{
		public:
			{name}() = default;
			{name}({name} const& other) : holder_{{other.holder_->clone()}} {{}}
			{name}& operator=({name} const& other) {{
				auto h = other.holder_->clone();
				std::swap(holder_, h);
				return *this;
			}}
			{name}({name}&& other) = default;
			{name}& operator=({name}&& other) = default;
			~{name}() noexcept = default;

			template<
				typename U,
				typename=std::enable_if_t<!std::is_same<{name}, std::decay_t<U>>::value>
			>
			{name}(U&& u)
			: holder_(std::make_unique<{name}_impl::{name}_holder<std::decay_t<U>>>(
				std::forward<U>(u))) {{}}

			explicit operator bool() const noexcept {{
				return static_cast<bool>(holder_);
			}}

			decltype(auto) swap({name}& other) noexcept {{
				holder_.swap(other.holder_);
			}}

{member_functions}

		private:
			std::unique_ptr<{name}_holder_impl::{name}_holder_base> holder_;
		}};

		decltype(auto) swap({name}& lhs, {name}& rhs) {{
			lhs.swap(rhs);
		}}
	}}
}}
