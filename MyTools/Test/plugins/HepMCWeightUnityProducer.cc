#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <memory>
#include <cmath>

#include "SimDataFormats/GeneratorProducts/interface/HepMC3Product.h"
#include "HepMC3/GenEvent.h"

class HepMCWeightUnityProducer : public edm::stream::EDProducer<> {
public:
  explicit HepMCWeightUnityProducer(const edm::ParameterSet& cfg)
    : src_(cfg.getParameter<edm::InputTag>("src"))
  {
    token_ = consumes<edm::HepMC3Product>(src_);
    produces<edm::HepMC3Product>();
  }

  void produce(edm::Event& evt, const edm::EventSetup&) override {
    edm::Handle<edm::HepMC3Product> h;
    evt.getByToken(token_, h);

    HepMC3::GenEvent ev;
    ev.read_data(*h->GetEvent());
    if (ev.weights().empty())
      ev.weights().push_back(1.0);
    else
      ev.weights()[0] = 1.0;
    auto out = std::make_unique<edm::HepMC3Product>(&ev);

    evt.put(std::move(out));
  }

private:
  edm::InputTag src_;
  edm::EDGetTokenT<edm::HepMC3Product> token_;
};

DEFINE_FWK_MODULE(HepMCWeightUnityProducer);

