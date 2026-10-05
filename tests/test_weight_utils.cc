#include "GeneratorInterface/RivetInterface/interface/WeightUtils.h"
#include <cassert>
#include <limits>
#include <iostream>

template <typename F> void rejects(F action) {
  bool failed = false;
  try { action(); } catch (const std::invalid_argument&) { failed = true; }
  assert(failed);
}

int main() {
  using namespace rivetweights;
  // Signed NLO events: LHE ratios retain the showered nominal sign/normalisation.
  assert(lheWeight(-2., -6., -4.) == -3.);
  assert(lheWeight(2., 6., 4.) == 3.);
  auto weights = orderedLHEWeights(-2., -4., {"scale", "pdf"}, {{"pdf", -8.}, {"scale", -6.}});
  assert(weights[0] == -3. && weights[1] == -4.);
  rejects([] { lheWeight(1., 1., 0.); });
  rejects([] { lheWeight(1., std::numeric_limits<double>::infinity(), 1.); });
  rejects([] { orderedLHEWeights(1., 1., {"a", "b"}, {{"a", 1.}, {"a", 2.}}); });
  rejects([] { orderedLHEWeights(1., 1., {"a"}, {{"b", 1.}}); });
  rejects([] { orderedLHEWeights(1., 1., {"a", "b"}, {{"a", 1.}}); });
  assert(jsonString("a\n\"\\\t") == "\"a\\u000a\\\"\\\\\\u0009\"");
  assert(cleanName("isr:muRfac=0.5") == "isr_muRfac=0.5");
  std::cout << "Weight normalisation, reordered IDs and invalid-input checks passed\n";
}
