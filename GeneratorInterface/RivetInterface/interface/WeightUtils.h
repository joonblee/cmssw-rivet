#ifndef GeneratorInterface_RivetInterface_WeightUtils_h
#define GeneratorInterface_RivetInterface_WeightUtils_h

#include <cmath>
#include <iomanip>
#include <regex>
#include <sstream>
#include <stdexcept>
#include <string>
#include <map>
#include <utility>
#include <vector>

namespace rivetweights {
  inline std::string cleanName(const std::string& name) {
    return std::regex_replace(name, std::regex("[^A-Za-z0-9._=]"), "_");
  }

  inline std::string jsonString(const std::string& value) {
    std::ostringstream out;
    out << '"';
    for (unsigned char c : value) {
      if (c == '"' || c == '\\') out << '\\' << c;
      else if (c < 0x20) out << "\\u" << std::hex << std::setw(4) << std::setfill('0') << int(c) << std::dec;
      else out << c;
    }
    out << '"';
    return out.str();
  }

  inline double lheWeight(double nominal, double variation, double original) {
    if (!std::isfinite(nominal) || !std::isfinite(variation) || !std::isfinite(original) || original == 0.)
      throw std::invalid_argument("Non-finite weight or zero originalXWGTUP in LHE reweighting");
    const double result = nominal * (variation / original);
    if (!std::isfinite(result)) throw std::invalid_argument("Non-finite normalised LHE weight");
    return result;
  }

  inline std::vector<double> orderedLHEWeights(double nominal, double original,
      const std::vector<std::string>& ids, const std::vector<std::pair<std::string, double>>& weights) {
    std::map<std::string, double> byId;
    for (const auto& weight : weights)
      if (!byId.emplace(weight).second) throw std::invalid_argument("Duplicate LHE weight ID " + weight.first);
    if (byId.size() != ids.size()) throw std::invalid_argument("LHE weight ID set changed between events");
    std::vector<double> result;
    for (const auto& id : ids) {
      auto it = byId.find(id);
      if (it == byId.end()) throw std::invalid_argument("Missing LHE weight ID " + id);
      result.push_back(lheWeight(nominal, it->second, original));
    }
    return result;
  }
}
#endif
