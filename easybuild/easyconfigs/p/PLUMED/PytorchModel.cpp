/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   Copyright (c) 2011-2018 The plumed team
   (see the PEOPLE file at the root of the distribution for a list of names)

   See http://www.plumed.org for more information.

   This file is part of plumed, version 2.

   plumed is free software: you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   plumed is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with plumed.  If not, see <http://www.gnu.org/licenses/>.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
#include "Function.h"
#include "ActionRegister.h"

#include <torch/torch.h>
#include <torch/script.h>

#include <cmath>

using namespace std;

std::vector<float> tensor_to_vector(const torch::Tensor& x) {
    return std::vector<float>(x.data<float>(), x.data<float>() + x.numel());
}

namespace PLMD {
namespace function {

//+PLUMEDOC FUNCTION PYTORCH MODEL
/*
Load a model trained with Pytorch. The derivatives are set using native backpropagation in Pytorch.

\par Examples
Define a model that takes as inputs two distances d1 and d2 

\plumedfile
model: PYTORCH_MODEL MODEL=model.pt ARG=d1,d2
\endplumedfile

The N nodes of the neural network are saved as "model.node-0", "model.node-1", ..., "model.node-(N-1)".

*/
//+ENDPLUMEDOC


class PytorchModel :
  public Function
{
  unsigned _n_in;
  unsigned _n_out;
  torch::jit::script::Module _model;
public:
  explicit PytorchModel(const ActionOptions&);
  void calculate();
  static void registerKeywords(Keywords& keys);
};


PLUMED_REGISTER_ACTION(PytorchModel,"PYTORCH_MODEL")

void PytorchModel::registerKeywords(Keywords& keys) {
  Function::registerKeywords(keys);
  keys.use("ARG");
  keys.add("optional","MODEL","filename of the trained model"); 
  keys.addOutputComponent("node", "default", "NN outputs"); 
}

PytorchModel::PytorchModel(const ActionOptions&ao):
  Action(ao),
  Function(ao)
{
  //number of inputs of the model
  _n_in=getNumberOfArguments();

  //parse model name
  std::string fname="model.pt";
  parse("MODEL",fname); 
 
  //deserialize the model from file
  try {
    _model = torch::jit::load(fname);
  }
  catch (const c10::Error& e) {
    error("Cannot find Pytorch model.");    
  }

  checkRead();

  //check the dimension of the output
  log.printf("Checking input dimension:\n");
  std::vector<float> input_test (_n_in);
  torch::Tensor single_input = torch::tensor(input_test).view({1,_n_in});  
  std::vector<torch::jit::IValue> inputs;
  inputs.push_back( single_input );
  torch::Tensor output = _model.forward( inputs ).toTensor(); 
  vector<float> cvs = tensor_to_vector (output);
  _n_out=cvs.size();

  //create components
  for(unsigned j=0; j<_n_out; j++){
    string name_comp = "node-"+std::to_string(j);
    addComponentWithDerivatives( name_comp );
    componentIsNotPeriodic( name_comp );
  }
 
  //print log
  //log.printf("Pytorch Model Loaded: %s \n",fname);
  log.printf("Number of input: %d \n",_n_in); 
  log.printf("Number of outputs: %d \n",_n_out); 

}

void PytorchModel::calculate() {

  //retrieve arguments
  vector<float> current_S(_n_in);
  for(unsigned i=0; i<_n_in; i++)
    current_S[i]=getArgument(i);
  //convert to tensor
  torch::Tensor input_S = torch::tensor(current_S).view({1,_n_in});
  input_S.set_requires_grad(true);
  //convert to Ivalue
  std::vector<torch::jit::IValue> inputs;
  inputs.push_back( input_S );
  //calculate output
  torch::Tensor output = _model.forward( inputs ).toTensor();
  //backpropagation
  output.backward();
  //convert to vector
  vector<float> cvs = tensor_to_vector (output);
  vector<float> der = tensor_to_vector (input_S.grad() );
  //set derivatives
  for(unsigned i=0; i<_n_in; i++)
    setDerivative(i,der[i]);
  //set CVs values
  for(unsigned j=0; j<_n_out; j++){
    string name_comp = "node-"+std::to_string(j);
    getPntrToComponent(name_comp)->set(cvs[j]);
  }
}

}
}


