mkdir ./my
mkdir ./my/functor
python ../type_erasure_generator.py ./any_functor.json ./my/functor
python ../traits_generator.py ./any_functor.json ./my/functor
